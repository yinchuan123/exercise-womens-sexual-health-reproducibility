args <- commandArgs(trailingOnly=FALSE)
self <- sub('^--file=','',args[grep('^--file=',args)])
taskdir <- dirname(normalizePath(self))
library(jsonlite)
suppressPackageStartupMessages(library(metafor))
inputs <- fromJSON(file.path(taskdir,'AGGREGATE_INPUTS_THREE_RESTRICTED_COMPARISONS.json'),simplifyVector=FALSE)
expected <- fromJSON(file.path(taskdir,'EXPECTED_SIX_EXISTING_CLINICAL_FITS.json'),simplifyVector=FALSE)
stopifnot(length(inputs$cases)==3,length(expected$cases)==3)
checks <- list(); answer <- list(); warns <- character()
assertclose <- function(label,a,b,tol=1e-7) {
  ok <- length(a)==length(b) && all(is.finite(a)) && all(is.finite(b)) && max(abs(a-b))<=tol
  checks[[length(checks)+1]] <<- list(check=label,pass=ok,tolerance=tol,maximum_absolute_delta=max(abs(a-b)))
  if(!ok)stop(label)
}
for(i in seq_along(inputs$cases)) {
  item <- inputs$cases[[i]]; exp <- expected$cases[[i]]
  stopifnot(item$id==exp$id,length(item$source_rows)==2,item$K_as_previously_fitted==2)
  rows <- item$source_rows
  y <- vapply(rows,function(r)r$yi,numeric(1));v <- vapply(rows,function(r)r$vi,numeric(1))
  family <- vapply(rows,function(r)r$candidate_family_id,character(1))
  stopifnot(length(unique(family))==2,all(is.finite(y)),all(v>0))
  for(j in seq_along(rows)) {
    r <- rows[[j]]
    if(r$variance_input_type=='NATIVE_REPORTED_SE_SQUARED') {
      assertclose(paste(item$id,j,'vi=nativeSE^2'),v[j],r$native_SE^2,1e-12)
    } else {
      assertclose(paste(item$id,j,'yi=arm endpoint MD'),y[j],r$mean_I-r$mean_C,1e-12)
      assertclose(paste(item$id,j,'vi=source SD2/N'),v[j],r$sd_I^2/r$n_I+r$sd_C^2/r$n_C,1e-12)
    }
  }
  # A verification refit of the pre-existing frozen target. No new scientific
  # fit count, result selection, endpoint transformation or clinical model gate.
  capture <- function(expr)withCallingHandlers(expr,warning=function(w){warns<<-c(warns,conditionMessage(w));invokeRestart('muffleWarning')})
  re <- if(grepl('OAB',item$id)) capture(rma.uni(yi=y,vi=v,method='REML',test='adhoc',control=list(threshold=1e-12))) else capture(rma.uni(yi=y,vi=v,method='REML',test='adhoc'))
  ce <- capture(rma.uni(yi=y,vi=v,method='EE',test='z'))
  models <- list(re,ce); summaries <- list()
  # Independent two-source intercept REML closed form: the likelihood depends
  # on v1+v2+2*tau2, hence constrained tau2=max(0,((y1-y2)^2-v1-v2)/2).
  # This validates metafor, rather than repeating the historical R script.
  closed_tau <- max(0,((y[1]-y[2])^2-sum(v))/2)
  assertclose(paste(item$id,'closed-form two-source REML tau2'),re$tau2,closed_tau)
  for(k in 1:2) {
    fit <- models[[k]];e <- exp$models[[k]]
    w <- 1/(v+if(k==1)closed_tau else 0);mu <- sum(w*y)/sum(w)
    q <- sum(w*(y-mu)^2)
    se <- sqrt((if(k==1)max(1,q) else 1)/sum(w))
    critical <- if(k==1)qt(.975,1) else qnorm(.975)
    ci <- mu+c(-1,1)*critical*se
    p <- if(k==1)2*pt(-abs(mu/se),df=1) else 2*pnorm(-abs(mu/se))
    tag <- paste(item$id,e$id)
    assertclose(paste(tag,'manual centre'),as.numeric(fit$b),mu)
    assertclose(paste(tag,'manual modifiedKH-or-normal SE'),fit$se,se)
    assertclose(paste(tag,'manual CI'),c(fit$ci.lb,fit$ci.ub),ci)
    assertclose(paste(tag,'manual p'),fit$pval,p)
    assertclose(paste(tag,'frozen estimate'),as.numeric(fit$b),e$estimate)
    assertclose(paste(tag,'frozen CI'),c(fit$ci.lb,fit$ci.ub),unlist(e$CI95))
    assertclose(paste(tag,'frozen SE'),fit$se,e$SE)
    if(!is.null(e$tau2))assertclose(paste(tag,'frozen tau2'),fit$tau2,e$tau2)
    if(!is.null(e$Q))assertclose(paste(tag,'frozen Q'),fit$QE,e$Q)
    if(!is.null(e$I2))assertclose(paste(tag,'frozen I2'),fit$I2,e$I2,1e-6)
    if(!is.null(e$p))assertclose(paste(tag,'frozen p'),fit$pval,e$p)
    summaries[[k]] <- list(id=e$id,estimate=as.numeric(fit$b),CI95=c(fit$ci.lb,fit$ci.ub),SE=fit$se,tau2=fit$tau2,Q=fit$QE,I2=fit$I2,p=fit$pval,model_entry_K=2,effective_pooled_N=NULL,technical_verification_only=TRUE)
  }
  answer[[i]] <- list(id=item$id,closed_form_REML_tau2=closed_tau,models=summaries,scope=item$scope,restrictions=item$restrictions)
}
out <- list(status='PASS_TECHNICAL_REPRODUCTION_ALL_SIX_EXISTING_CLINICAL_FITS',pre_existing_clinical_comparison_sets=3,verification_model_evaluations=6,new_scientific_fits=0,new_primary_pools=0,new_K_N_or_GRADE=0,separate_diagnostic_fits_not_refitted=22,checks=checks,check_count=length(checks),results=answer,warnings=unique(warns),limits='Reproduces aggregate endpoint or native-coefficient inverse-variance models only. Does not reproduce original trial ANCOVA, multiple imputation, bootstrap, IPD, all22diagnostics, or a whole-review primary pooled effect.',software=list(R=R.version.string,metafor=as.character(packageVersion('metafor')),jsonlite=as.character(packageVersion('jsonlite'))))
write_json(out,file.path(taskdir,'VERIFICATION_SIX_EXISTING_CLINICAL_FITS.json'),auto_unbox=TRUE,pretty=TRUE,digits=17,null='null')
capture.output(sessionInfo(),file=file.path(taskdir,'VERIFICATION_SESSION_INFO.txt'))
cat(toJSON(list(status=out$status,checks=length(checks),existing_models_reproduced=6,new_scientific_models=0),auto_unbox=TRUE),'\n')
