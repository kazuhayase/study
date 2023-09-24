###########Initialization##########
rm(list = ls())
required <- c(
  "aglm", "catdata", "glmnetUtils", "mgcv", 
  "pdp", "randomForest", "ranger", "rpart")
required <- setdiff(required, library()$results[, 1])
if (!length(required) == 0)
  install.packages(required)
rm(required)

##########Version check##########
# Random Number Generator
RNGkind()
# kind = "Mersenne-Twister", 
# normal.kind = "Inversion", 
# sample.kind = "Rejection")

########################################

##########Preprocessing##########
###For reproducibility###
# Seed
SEED <- 2020

###Data###
data("rent", package = "catdata")
#hist(rent$rentm)
y <- rent$rentm
xnames <- setdiff(colnames(rent), c("rent", "rentm"))
x <- rent[, colnames(rent) %in% xnames]
x$area <- as.factor(x$area)
xy <- cbind(x, y)
n <- nrow(xy)

###Holdout###
set.seed(SEED)
test.id <- sample(n, round(n / 4))
test <- xy[test.id, ]
train <- xy[-test.id, ]
#str(train)
#str(test)

###Loss function: RMS###
rms <- function(act, pred) {sqrt(mean((act - pred) ^ 2))}

##########EDA##########
###Summary###
?catdata::rent
summary(train)

###Scatter Plots###
p <- ncol(xy) - 1
frame() #If RGui, check "Recording" in "History".
for(i in 1:p){
  plot(train[, i], pch =".", xlab = colnames(train)[i])
}

# size, rooms, year with lowess curves
for(i in ###){
  plot(##########)
  ###(lowess(###, ###))
}

###EDA via RandomForest###
library(randomForest)
library(pdp)

##Modeling##
set.seed(SEED)
rndmFrst <- randomForest(y ~ ., data = train, ### = TRUE)

# yhat
yhat <- predict(rndmFrst, newdata = test)

# RMSE
cat(" RMSE(rf) =", result_rf <- rms(test$y, yhat)) #2.01246 

##EDA##
# Importance
imp <- ##########
barplot(imp, names.arg = rownames(imp))

# PDP
for (i in 1:3) {
  ##########
  ##########
  ##########
  ##########
}

##########Modeling##########
###LM without interactions###
##textbook#p.18#p.136##
linear <- model <- lm(###, data = train)
# yhat
yhat <- ###(model, newdata = test)
# RMSE
cat(" RMSE(linear) =", result_linear <- rms(test$y,
yhat)) #2.088066
###Decision Tree###
library(rpart)
##Simple tree##
##textbook#p.126##
tree <- model <- rpart(###, data = train)
# Plot
par(xpd = NA)
plot(model)
text(model, use.n = TRUE)
par(xpd = FALSE)
# yhat
yhat <- predict(model, newdata = test)
# RMSE
cat(" RMSE(tree) =", result_tree <- rms(test$y, yhat))
#2.153924
##Tuned tree##
set.seed(SEED)
maxTree <- rpart(y ~ ., data = train, cp = 0)
plotcp(maxTree)
cps <- maxTree$cptable
# Using min + 1se
cpid <- which.min(cps[, 4])
(cp <- cps[min(which(cps[, 4] < cps[cpid, 4] + cps[cpid,
5])), 1])
bestTree <- model <- rpart(y ~ ., data = train, cp =
cp)
# yhat
yhat <- predict(model, newdata = test)
# RMSE
cat(" RMSE(bestTree) =", result_bestTree <- rms(test$y,
yhat)) #2.153924

###GLMs###
##Gamma GLM##
##textbook#p.22#p.136##
gammaGLM <- model <- 
  glm(###, ### = Gamma(log), 
      data = train) # loglink

# yhat
yhat <- predict(model, newdata = test, 
                ###)

# RMSE
cat(" RMSE(gammaGLM) =", 
    result_gammaGLM <- 
      rms(test$y, yhat)) #2.088789

##LM with interactions##
##textbook#p.136##
lmInt <- model <- lm(y ~ ###, 
                     data = train)
# yhat
yhat <- predict(model, newdata = test, type = "response") 
#You can omit "type = "response""

# RMSE
cat(" RMSE(lmInt) =", 
    result_lmInt <- 
      rms(test$y, yhat)) #2.323613

##Stepwise LM (forward)##
lm1 <- lm(y ~ 1, data = train) # Intercept only
stepLM <- model <- 
  step(lm1, scope = formula(lmInt), 
       direction = "forward", trace = 0) 
AIC(model) #6558.577

# yhat
yhat <- predict(model, newdata = test)

# RMSE
cat(" RMSE(stepLM) =", 
    result_stepLM <- 
      rms(test$y, yhat)) #2.134819

###LASSO###
library(glmnetUtils)
(formu <- formula(lmInt))
##textbook#p.144##
lsso <- cv.glmnet(###, 
                  data = ###, 
                  alpha = ###)
plot(lsso)
(lambda.min <- lsso$lambda.min)
(lambda.1se <- lsso$lambda.1se)

# yhat
yhat <- predict(lsso, 
                ### = lambda.min, 
                newdata = test, 
                type = "response")

# RMSE
cat(" RMSE(lasso) =", 
    result_lasso <- 
      rms(test$y, yhat)) #2.134471

###Random Forest###
library(ranger)
set.seed(SEED)
rf <- model <- ranger(###, data = ###)

# yhat
yhat <- predict(model, data = test)$predictions

# RMSE
cat(" RMSE(rf) =", 
    result_rf <- 
      rms(test$y, yhat)) #2.009848

##########All results##########
c(linear = result_linear,
  tree = result_tree, 
  bestTree = result_bestTree,
  gammaGLM = result_gammaGLM,
  lmInt = result_lmInt,
  stepLM = result_stepLM,
  lasso = result_lasso,
  rf = result_rf)
#  linear     tree bestTree gammaGLM 
#2.088066 2.153924 2.153924 2.088789 
#   lmInt   stepLM    lasso       rf 
#2.323613 2.134819 2.134471 2.009848

##########Appendix##########
###AGLM###
library(aglm)
set.seed(SEED)
aglm <- cv.aglm(train[, -12], train$y, 
                alpha = 1,
                #family = Gamma(log),
                nbin.max = 10)
(lambda.min <- aglm@lambda.min)
(lambda.1se <- aglm@lambda.1se)

# yhat
yhat <- predict(aglm, 
                s = lambda.min, 
                newx = test[, -12], 
                type = "response")

# RMSE
cat(" RMSE(aglm) =", 
    result_aglm <- 
      rms(test$y, yhat)) #1.971832 #1.982154 for Gamma

###Tuned RF###Perhaps installation needed
library(tuneRanger)
task <- makeRegrTask(data = train, target = "y")
set.seed(SEED)
obj <- tuneRanger(task, 
                  num.trees = 40,
                  tune.parameters = c("mtry", "min.node.size"),
                  show.info = FALSE)
set.seed(SEED)
rf_tuned <- ranger(y ~ ., data = train,
                   mtry = obj$recommended.pars$mtry,
                   min.node.size = obj$recommended.pars$min.node.size)

# yhat
yhat <- predict(rf_tuned, data = test)$predictions

# RMSE
cat(" RMSE(rf_tuned) =", 
    result_rf_tuned <- 
      rms(test$y, yhat)) #2.006696
