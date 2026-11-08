suppressPackageStartupMessages(library(metafor))
suppressPackageStartupMessages(library(jsonlite))
args <- commandArgs(trailingOnly=TRUE)
out <- if(length(args)>0) normalizePath(args[[1]], mustWork=TRUE) else normalizePath(getwd(), mustWork=TRUE)
dir.create(file.path(out,'replay'), recursive=TRUE, showWarnings=FALSE)
plan <- fromJSON(file.path(out,'data/IMPACT_AUDIT_PLAN.json'),simplifyVector=FALSE)
input <- fromJSON(file.path(out,'data/PUBLISHED_FIGURE_ROWS_REUSED.json'))$rows
results <- list(); all_inputs <- list()
for(s in plan$scenarios){
  d <- input[!input$label %in% unlist(s$drop),]
  for(nm in names(s$N_updates)){
    d$displayed_N_I[d$label==nm] <- s$N_updates[[nm]]$I
    d$displayed_N_C[d$label==nm] <- s$N_updates[[nm]]$C
  }
  for(nm in names(s$SD_updates)){
    d$SD_I[d$label==nm] <- s$SD_updates[[nm]]$I
    d$SD_C[d$label==nm] <- s$SD_updates[[nm]]$C
  }
  d$yi <- d$mean_I-d$mean_C
  d$vi <- d$SD_I^2/d$displayed_N_I+d$SD_C^2/d$displayed_N_C
  m <- nrow(d)
  all_inputs[[s$id]] <- d
  fit_f <- rma.uni(yi=d$yi,vi=d$vi,method='FE')
  fit_r <- rma.uni(yi=d$yi,vi=d$vi,method='REML',test='knha')
  w_re <- 1/(d$vi+as.numeric(fit_r$tau2))
  q_hk_raw <- sum(w_re*(d$yi-as.numeric(fit_r$b))^2)/(m-1)
  q_hk <- max(1,q_hk_raw)
  stopifnot(abs(sqrt(q_hk_raw/sum(w_re))-as.numeric(fit_r$se))<1e-9)
  se_mhk <- sqrt(q_hk/sum(w_re))
  crit <- qt(.975,df=m-1)
  mu <- as.numeric(fit_r$b)
  pi_half <- qt(.975,df=m-2)*sqrt(as.numeric(fit_r$tau2)+se_mhk^2)
  results[[s$id]] <- list(scenario_id=s$id,name=s$name,source_effect_rows=m,independent_trial_k=NULL,
    fixed=list(estimate=as.numeric(fit_f$b),se=as.numeric(fit_f$se),ci=c(as.numeric(fit_f$ci.lb),as.numeric(fit_f$ci.ub)),Q=as.numeric(fit_f$QE),I2=as.numeric(fit_f$I2)),
    random_REML_modified_HK=list(estimate=mu,se=se_mhk,ci=c(mu-crit*se_mhk,mu+crit*se_mhk),tau2=as.numeric(fit_r$tau2),I2=as.numeric(fit_r$I2),q_modified_HK=q_hk,df=m-1,diagnostic_prediction_interval=c(mu-pi_half,mu+pi_half)),
    valid_clinical_pool=FALSE,project_primary_model=FALSE,interpretation=s$purpose)
}
stopifnot(round(results$S0$fixed$estimate,2)==5.31,all(round(results$S0$fixed$ci,2)==c(4.87,5.75)))
output <- list(mode='published-input single-factor diagnostic audit; not corrected clinical synthesis',
  software=list(R=R.version.string,metafor=as.character(packageVersion('metafor')),jsonlite=as.character(packageVersion('jsonlite'))),
  plan_path='data/IMPACT_AUDIT_PLAN.json',results=results,scenario_inputs=all_inputs,
  project_models_modified=FALSE,formal_human_eligibility=NULL,whole_SR_final_K=NULL,formal_GRADE=NULL)
write_json(output,file.path(out,'replay/PUBLISHED_INPUT_IMPACT_AUDIT.json'),auto_unbox=TRUE,pretty=TRUE,null='null',digits=15)
writeLines(capture.output(sessionInfo()),file.path(out,'replay/R_SESSION_INFO.txt'))
cat(toJSON(lapply(results,function(x)list(id=x$scenario_id,rows=x$source_effect_rows,fixed=x$fixed[c('estimate','ci')],random=x$random_REML_modified_HK[c('estimate','ci','tau2')])),auto_unbox=TRUE,pretty=TRUE,digits=6))
