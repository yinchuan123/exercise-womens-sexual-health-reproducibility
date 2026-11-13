# Portable derivation of the actually executed R221 R/rstan workflow.
# Uses the published actual Stan text instead of a private compiled RDS.
suppressPackageStartupMessages({library(jsonlite);library(rstan);library(posterior)})
script<-sub('^--file=','',commandArgs()[grepl('^--file=',commandArgs())][1]);HERE<-normalizePath(file.path(dirname(script),'..'))
args<-commandArgs(TRUE);OUT<-if(length(args))args[1] else 'out-r222';dir.create(OUT,recursive=TRUE,showWarnings=FALSE)
L<-fromJSON(file.path(HERE,'inputs/pool_sets39.json'),simplifyVector=FALSE);options(mc.cores=4)
m<-stan_model(file=file.path(HERE,'analysis/actual_normal_random_effects.stan'));bay<-list();diag<-list()
for(p in L$pools)for(plan in p$bayesian_replay_plan){
 if(plan$computation!='MCMC')next
 y<-vapply(p$rows,function(r)r$yi,numeric(1));v<-vapply(p$rows,function(r)r$vi,numeric(1));warns<-character()
 fit<-withCallingHandlers(sampling(m,data=list(K=p$K,y=y,se=sqrt(v),mu_sd=plan$mu_normal_SD,tau_sd=plan$tau_half_normal_SD),chains=4,iter=10000,warmup=2500,seed=as.integer(plan$seed),refresh=0,control=list(adapt_delta=.99,max_treedepth=15)),warning=function(w){warns<<-c(warns,conditionMessage(w));invokeRestart('muffleWarning')})
 ar<-as.array(fit,pars=c('mu','tau','theta_new'))
 ps<-do.call(rbind,lapply(seq_len(dim(ar)[3]),function(k){a<-ar[,,k];data.frame(parameter=dimnames(ar)[[3]][k],mean=mean(a),SD=sd(as.numeric(a)),Rhat=posterior::rhat(a),ESS_bulk=posterior::ess_bulk(a),ESS_tail=posterior::ess_tail(a),MCSE_mean=posterior::mcse_mean(a))}))
 sm<-get_sampler_params(fit,inc_warmup=FALSE);div<-sum(vapply(sm,function(z)sum(z[,'divergent__']),numeric(1)));td<-sum(vapply(sm,function(z)sum(z[,'treedepth__']>=15),numeric(1)));bf<-vapply(sm,function(z)mean(diff(z[,'energy__'])^2)/var(z[,'energy__']),numeric(1))
 pass<-all(ps$Rhat<=1.01)&all(ps$ESS_bulk>=1000)&all(ps$ESS_tail>=1000)&all(ps$MCSE_mean/ps$SD<.05)&div==0&td==0&all(bf>.3)
 z<-rstan::extract(fit,pars=c('mu','tau','theta_new','y_rep'));z$mu<-as.numeric(z$mu);z$tau<-as.numeric(z$tau);z$theta_new<-as.numeric(z$theta_new);qu<-function(x)unname(quantile(x,c(.025,.5,.975)))
 vari<-matrix(v,nrow=length(z$mu),ncol=p$K,byrow=TRUE)+as.numeric(z$tau)^2;obs<-matrix(y,nrow=length(z$mu),ncol=p$K,byrow=TRUE)
 bay[[length(bay)+1]]<-list(pool_id=p$pool_id,K=p$K,method='BAYES_NORMAL_RANDOM_EFFECTS_FRESH_FOUR_CHAIN_MCMC',tau_prior_half_normal_SD=plan$tau_half_normal_SD,mu_prior_normal_SD=plan$mu_normal_SD,posterior_mean=mean(z$mu),posterior_mu_025_50_975=qu(z$mu),posterior_tau_mean=mean(z$tau),posterior_tau_025_50_975=qu(z$tau),new_setting_true_effect_025_50_975=qu(z$theta_new),Pr_mean_MD_gt0=mean(z$mu>0),Pr_new_setting_true_MD_gt0=mean(z$theta_new>0),posterior_predictive_discrepancy_p=mean(rowSums((z$y_rep-z$mu)^2/vari)>=rowSums((obs-z$mu)^2/vari)),diagnostics_pass=pass,seed=plan$seed,members=p$member_input_ids,probabilities_not_individual_response=TRUE)
 diag[[length(diag)+1]]<-list(pool_id=p$pool_id,tau_prior_SD=plan$tau_half_normal_SD,chains=4,iterations_per_chain=10000,warmup_per_chain=2500,parameters=ps,divergences=div,treedepth_hits=td,E_BFMI=bf,warnings=unique(warns),pass=pass)
 write_json(bay,file.path(OUT,'fresh_MCMC_replayed51.json'),auto_unbox=TRUE,pretty=TRUE,null='null',digits=16);write_json(diag,file.path(OUT,'fresh_MCMC_diagnostics51.json'),auto_unbox=TRUE,pretty=TRUE,null='null',digits=16)
 cat(p$pool_id,'tauSD',plan$tau_half_normal_SD,'pass',pass,'\n');rm(fit,z,ar);gc(verbose=FALSE)
}
stopifnot(length(bay)==51);write_json(list(views=length(bay),all_diagnostics_pass=all(vapply(diag,function(d)d$pass,logical(1))),compiler_dependent_not_bitwise_replay=TRUE),file.path(OUT,'fresh_MCMC_replay_summary.json'),auto_unbox=TRUE,pretty=TRUE)
