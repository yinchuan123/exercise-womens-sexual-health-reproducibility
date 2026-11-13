suppressPackageStartupMessages({library(jsonlite);library(metafor)})
script<-sub('^--file=','',commandArgs()[grepl('^--file=',commandArgs())][1]);HERE<-normalizePath(file.path(dirname(script),'..'))
args<-commandArgs(TRUE);OUT<-if(length(args))args[1] else 'out-r222';dir.create(OUT,recursive=TRUE,showWarnings=FALSE)
L<-fromJSON(file.path(HERE,'inputs/pool_sets39.json'),simplifyVector=FALSE)
expected<-fromJSON(file.path(HERE,'data/frequentist_results78.json'),simplifyVector=FALSE)$rows
expectedLOO<-fromJSON(file.path(HERE,'data/leave_one_family_out45.json'),simplifyVector=FALSE)$rows
fitone<-function(p,common=FALSE){
 y<-vapply(p$rows,function(r)r$yi,numeric(1));v<-vapply(p$rows,function(r)r$vi,numeric(1))
 stopifnot(length(y)==p$K,!anyDuplicated(vapply(p$rows,function(r)r$family_id,character(1))),all(v>0))
 ctl<-if(p$source_lock_id=='r221-inclusive14')list(threshold=1e-10,maxiter=10000) else list()
 z<-rma.uni(yi=y,vi=v,method=if(common)'FE' else 'REML',test=if(common)'z' else 'adhoc',control=ctl);pr<-predict(z)
 list(pool_id=p$pool_id,K=p$K,method=if(common)'COMMON_EFFECT_NORMAL' else 'REML_modified_Hartung_Knapp_q_ge1',estimate=as.numeric(coef(z)),CI95=unname(c(z$ci.lb,z$ci.ub)),SE=as.numeric(z$se),tau2=as.numeric(z$tau2),I2=as.numeric(z$I2),Q=as.numeric(z$QE),Q_p=as.numeric(z$QEp),prediction95=if(common)NULL else unname(c(pr$pi.lb,pr$pi.ub)),weights_percent=unname(as.numeric(weights(z))),members=p$member_input_ids)
}
freq<-list();loo<-list();checks<-list()
compare<-function(a,b,label){
 for(k in c('estimate','CI95','SE','tau2','I2','Q','weights_percent'))stopifnot(isTRUE(all.equal(unlist(a[[k]]),unlist(b[[k]]),tolerance=2e-4)))
 checks[[length(checks)+1]]<<-label
}
for(p in L$pools){
 for(common in c(FALSE,TRUE)){
  z<-fitone(p,common);e<-Filter(function(x)x$pool_id==z$pool_id&&x$method==z$method,expected)[[1]];compare(z,e,paste(z$pool_id,z$method));freq[[length(freq)+1]]<-z
 }
 ee<-Filter(function(x)x$pool_id==p$pool_id,expectedLOO)
 for(e in ee){
  q<-p;q$rows<-Filter(function(x)x$input_id!=e$omitted_input,p$rows);q$K<-length(q$rows);q$member_input_ids<-lapply(q$rows,function(r)r$input_id);z<-fitone(q);z$omitted_input<-e$omitted_input;compare(z,e,paste(z$pool_id,'omit',e$omitted_input));loo[[length(loo)+1]]<-z
 }
}
stopifnot(length(freq)==78,length(loo)==45)
write_json(list(rows=freq),file.path(OUT,'frequentist_replayed78.json'),auto_unbox=TRUE,pretty=TRUE,null='null',digits=16)
write_json(list(rows=loo),file.path(OUT,'leave_one_family_out_replayed45.json'),auto_unbox=TRUE,pretty=TRUE,null='null',digits=16)
write_json(list(status='PASS',comparisons=length(checks),frequentist_views=78,leave_one_family_out_views=45,metafor_version=as.character(packageVersion('metafor')),validation_not_new_clinical_input=TRUE),file.path(OUT,'frequentist_replay_QA.json'),auto_unbox=TRUE,pretty=TRUE)
cat('PASS:78frequentist views and45LOO views; overlapping K/N are not summed.\n')
