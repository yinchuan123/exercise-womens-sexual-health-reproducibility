data {
  int<lower=2> K;
  vector[K] y;
  vector<lower=0>[K] se;
  real<lower=0> mu_sd;
  real<lower=0> tau_sd;
}
parameters {
  real mu;
  real<lower=0> tau;
}
model {
  mu ~ normal(0, mu_sd);
  tau ~ normal(0, tau_sd);
  y ~ normal(mu, sqrt(square(se) + rep_vector(square(tau), K)));
}
generated quantities {
  vector[K] y_rep;
  real theta_new;
  theta_new = normal_rng(mu, tau);
  for (k in 1:K)
    y_rep[k] = normal_rng(mu, sqrt(square(se[k]) + square(tau)));
}
