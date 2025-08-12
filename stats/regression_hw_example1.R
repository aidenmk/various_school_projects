library(MASS)

GetFCrit <- function(df_num, df_denom, alpha){
  f_crit <- qf(1-alpha, df_num, df_denom)
  print(f_crit)
}

CompareFTest <-  function(f_stat, alpha, df_num, df_denom){
  if (f_stat > GetFCrit(df_num, df_denom, alpha)){
    print("reject null")
  } else {
    print("fail to reject null")
  }
}

GetYBarJ <- function(X_map){
  Yi_mean_map <- list()
  for (X in names(X_map)){
    Yi_tot <- 0
    ni <- 0
    for (Yij in X_map[[X]]){
      Yi_tot <- Yi_tot + Yij
      ni <- ni + 1
    }
    Yi_mean_map[[X]] <- Yi_tot / ni
  }
  return(Yi_mean_map)
}

#can do this in a simpler way like GetSSERed
GetSSEFull <- function(X_map, Yi_mean_map){
  sse_full <- 0
  for (X in names(X_map)){
    for (Yij in X_map[[X]]){
      Yij_minus_Yjbar <- Yij - Yi_mean_map[[X]]
      sse_full <-  sse_full + Yij_minus_Yjbar^2
    }
  }
  return(sse_full)
}

GetSSERed <- function(fit){
  i <- 1
  sse_red <- 0
  while(i <= length(fit$model$X)){
    Yij_minus_Yhat <- fit$model[i, 1] - fit$fitted.values[i]
    sse_red <- sse_red + Yij_minus_Yhat^2
    i <- i + 1
  }
  return(sse_red)
}

GetFLackOfFit <- function(obs_data, n, predicted_beta_count, alpha){
  fit <-lm(Y ~ X, data = obs_data)   
  # Dict with key as X, 1 or more values as Y 
  X_map <- split(obs_data$Y, obs_data$X)
  c <- length(names(X_map))
  X_mean <- mean(obs_data$X)
  Y_bar_j_map <- GetYBarJ(X_map)
  
  # To calculate SSE reduced, we are assuming only 2 betas (beta0 and beta1)
  sse_red <- GetSSERed(fit) 
  sse_full <- GetSSEFull(X_map, Y_bar_j_map)
  df_sse_full <- n - c
  df_sse_red <- n - predicted_beta_count
  sspe <- sse_full
  sslf <- sse_red - sse_full
  mspe <- sspe / df_sse_full
  mslf <- sslf/ (df_sse_red - df_sse_full)
  f_stat <- mslf/mspe
  df_num <- df_sse_red - df_sse_full
  df_denom <- df_sse_full
  CompareFTest(f_stat, alpha, df_num, df_denom)
  
  table <- data.frame(
    Source = c('Regression', 'Residual Error Full','Residual Error Reduced',
               'Lack of Fit', 'Pure Error', 'Total'),
    DF     = c('', '','', df_num, df_denom, ''),
    SS     = c('', sse_full,sse_red, sslf, sspe, ''),
    MS     = c('', '', '',mslf, mspe, ''),
    F      = c('', '','', f_stat, '', ''),
    P      = c('', '', '','', '', '')
  )
  print(table)
}

CompareCorCoef <- function(obs_coef, coef_crit){
  if (obs_coef < coef_crit) {
    print("Reject normality")
  } else {
    print("Normal")
  }
}

hard_data <- read.table(text = "
                        Y X
                        199.0 16.0
                        205.0 16.0
                        196.0 16.0
                        200.0 16.0
                        218.0 24.0
                        220.0 24.0
                        215.0 24.0
                        223.0 24.0
                        237.0 32.0
                        234.0 32.0
                        235.0 32.0
                        230.0 32.0
                        250.0 40.0
                        248.0 40.0
                        253.0 40.0
                        246.0 40.0", header = TRUE)

#if running this with other data make sure it is sorted for other functions to work
hard_data <- hard_data[order(hard_data$X), ]
n <- 16
fit <-lm(Y ~ X, data = hard_data)                       
#summary(fit)
anova(fit)

#3.6a
boxplot(fit$residuals, main = '3.6A Boxplot of residuals')

#3.6b
plot(fit, which = 1, main = '3.6B')

#3.6c
qqnorm(fit$residuals,  main = '3.6c Normal Q-Q Plot of Residuals')
qqline(fit$residuals)
#plot(qnorm(ppoints(n)))
correlation_coef <- cor(sort(fit$residuals), qnorm(ppoints(n)))
CompareCorCoef(correlation_coef, .941)

#3.14a Aiden Way
#Nullhypothesis = meanj = beta zero + b1*Xj for all j
#Alternative = mean j's do not lie on straight line
alpha <- 0.01
predicted_beta_count <- 2
GetFLackOfFit(hard_data, n, predicted_beta_count, alpha)
# We fail to reject null meaning that this linear regression model is adequate.
# In other words, there is no lack of fit

# Easy way 3.14a
# Fit a linear model
# fit_linear <- lm(hard_data$Y ~ hard_data$X, data=hard_data)
# 
# # Fit a model with x as a factor (saturated model)
# fit_factor <- lm(hard_data$Y ~ factor(hard_data$X), data=hard_data)
# 
# # Compare the two models using anova()
# anova(fit_linear, fit_factor)

#3.14b
# Advantages are that each X value would have equal weight of Y input. This
# would generally mean that the test has stability. On a technical note,
# the pure error value would be consistent due to balanced residuals in the SSE 
# full value. The only disadvantage would be a lack of realism in finding data
# that has consistent nj counts across X values/bins.

#3.14c To my knowledge the lack of fit F test does not suggest a new appropiate
# regression function. Perform diagnostics such as plotting residuals against X 
# variable, against fitted Y values etc... You can do Box Cox transformation or 
# other remedies

# 3.16a
sol_data <- read.csv('sta108/315_data.csv', skip = 1, header = FALSE, 
                     col.names = c("Y", "X"))
plot(sol_data$X, sol_data$Y)
#I would try Y transformation via log or 1 divided by Y


# 3.16b
fit <- lm(sol_data$Y ~ sol_data$X, data=sol_data)
boxcox(fit, lambda = seq(-1, 1, 0.1))
plot(sol_data$X, (sol_data$Y)^.001)

#3.16c
fit <- lm(log10(sol_data$Y) ~ sol_data$X, data=sol_data)
fit$coefficients

#3.16d
plot(sol_data$X, log10(sol_data$Y))
abline(fit, col = "red", lwd = 1)

#3.16e
plot(fit, which=1)
plot(fit, which=2)

#Y =antilog10(0.6548798 − -0.1954003X) = 4.517309 + (0.6376755)X
antilog10 <- function(x) 10^x
antilog10(0.6548798)
antilog10(-0.1954003)
