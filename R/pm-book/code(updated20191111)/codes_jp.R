##### 目次 #####
#付録B
#初期化
#第1章
#第3章
#第4章
#第5章
#第6章
#第7章
#第8章
#第9章
#補章

########################################
#####付録B
#
2 + 3

#
seq(1, 10, 0.2)

#
a <- sign(pi)
a + 2

#
?"sign"

#
set.seed(1234)
for (n in c(2, 5, 10, 20, 50)) {
  x <- stats::rnorm(n)
  cat(n, ": ", sum(x ^ 2), "\n", sep = "")
}

#
quadraticFormula <- function(a, b, c) {
  return(c((-b + sqrt(b ^ 2 - 4 * a * c)) / (2 * a),
           (-b - sqrt(b ^ 2 - 4 * a * c)) / (2 * a)))
}

quadraticFormula(1, 5, 6)

#
quadraticFormula <- function(a, b, c) {
  x_r <- (-b + sqrt(b ^ 2 - 4 * a * c)) / (2 * a)
  x_l <- (-b - sqrt(b ^ 2 - 4 * a * c)) / (2 * a)
  curve(a * x ^ 2 + b * x + c, 2 * x_l - x_r, 2 * x_r - x_l)
  abline(h = 0)
  c(x_r, x_l)
}

quadraticFormula(1, 5, 6)

#
sin(c(0, pi / 4, pi / 2))

c(sin(0), sin(pi / 4), sin(pi / 2))

#
rnorm

#
2 + 3  

#
2 + 
3  

#
2
+ 3  

#
2 + 3; 3 + 4

#
2 + 3
3 + 4

#
ls()

#
rm(a)

#
rm(n, x)

#
rm(list = ls())

########################################
#####初期化 (非入門者向け．必要な全パッケージの事前インストール）
rm(list = ls())
required <- c(
 "caret", "corrplot", "devtools", "doParallel",
 "DT", "glmnetUtils", "mgcv", "parallel", "pdp",
 "psych", "randomForest", "ranger", "ROCR", "rpart",
 "sp", "xgboost", "xts"
)
required <- setdiff(required, library()$results[, 1])
if (!length(required) == 0)
  install.packages(required)
rm(required)

########################################
#####第1章
#
x_1 <- trees$Girth
x_2 <- trees$Height
y <- trees$Volume
(model_1 <- model <- lm(y ~ x_1 + x_2))

#
yhat <- fitted(model)
plot(y, yhat, main = model$call)
curve(identity, add = TRUE)

#
x_3 <- x_1 ^ 2
(model_2 <- model <- lm(y ~ x_1 + x_2 + x_3))
yhat <- fitted(model)
plot(y, yhat, main = model$call)
curve(identity, add = TRUE)

#
(model <- lm(Volume ~ Girth + Height + I(Girth ^ 2),
             data = trees))

#
(model_3 <- model <-
   glm(y ~ log(x_1) + log(x_2),
       family = Gamma(link = "log")))
yhat <- fitted(model)
plot(y, yhat, main = model$call)
curve(identity, add = TRUE)

#
cat(

  "AICs:\n lm(x_1 + x_2):", AIC(model_1),
  "\n lm(x_1 + x_2 + x_1 ^ 2):", AIC(model_2),
  "\n glm(log(x_1) + log(x_2), Gamma(log)):", AIC(model_3)
  )

########################################
#####第3章
#
str(iris)

#
summary(iris)

#
quantile(iris$Sepal.Length, probs = 0.25)

#
var(iris[!colnames(iris) == "Species"])

#
cor(iris[-5], method = "kendall")

#
plot(iris$Sepal.Length, pch = as.numeric(iris$Species))
legend("topleft", legend = levels(iris$Species), pch = 1:3)

#
plot(iris[1:4], pch = as.numeric(iris$Species))

plot(iris[1:4], col = as.numeric(iris$Species))

#
?plot.data.frame

#
dat <- iris[c(1, 3)]
plot(dat, pch = as.numeric(iris$Species))
lines(lowess(dat), col = "red")

#
hist(iris$Sepal.Length)

#
hist(iris$Sepal.Length, probability = TRUE)

#
plot(density(iris$Sepal.Length), ylim = c(0, 0.5))
hist(iris$Sepal.Length, probability = TRUE, add = TRUE)

#
plot.ecdf(iris$Sepal.Length)

#
library(psych)
pairs.panels(iris)

#
set.seed(1234)
result <- kmeans(scale(iris[1:4]), 2) # k = 2
plot(iris[1:4], col = result$cluster,
     pch = as.numeric(iris$Species))

#
(pca <- prcomp(iris[1:4]))
plot(pca$x[, 1:2], pch = as.numeric(iris$Species))
legend("topright", legend = levels(iris$Species), pch = 1:3)

########################################
#####第4章
#
a <- sqrt(2)
a

#
(a <- sqrt(2))

#
sqrt(a <- sqrt(2))

#
(b <- a)

#
pi

#
str(pi)

#
str(c <- seq(-0.2, 1, 0.4))

#
t(c) %*% c

#
(d <- c %*% t(c))

#
str(d)

#
(e <- matrix(1:8, nrow = 2)) 

#
str(e)

#
str(glm)

#
g <- glm(dist ~ ., data = cars)
# str(g)

#
g

#
summary(g)

#
class(g)

#
methods(summary)

#
?summary.glm

########################################
#####第5章
#
iris

#
View(iris)

#
library(help = "datasets")

#
str(iris)

#
iris[4, 2]

#
str(iris[2])

#
str(iris$Sepal.Width)

#
str(iris[, 2])
str(iris[, "Sepal.Width"])

#
str(iris[, colnames(iris) == "Sepal.Width"])

#
levels(iris$Species)

#
iris.num <- iris
iris.num$Species <- as.numeric(iris.num$Species)
str(iris.num)

#
head(iris.num)

#
iris.mx <- as.matrix(iris.num)
head(iris.mx)

#
str(iris.mx, give.attr = FALSE)

#
str(as.matrix(iris))

#
getwd()

#
iris.df <- read.csv(file = "./data/iris.csv")
str(iris.df)

#
iris.df <- read.csv(file = "./data/iris.csv",
                    header = TRUE,
                    fileEncoding = "UTF-8")
str(iris.df)

#
iris.df <- iris
save(iris.df, file = "./data/iris.rda")

#
rm(iris.df)
load(file = "./data/iris.rda")
str(iris.df)

#
library(MASS)
head(Boston)

#
install.packages("mlbench")

#
library(mlbench)
data(Sonar)

#
dim(Sonar)
colnames(Sonar)

#
install.packages(
  "CASdatasets",
  repos = "http://cas.uqam.ca/pub/R/",
  dependencies = TRUE,
  type = "source"
  )

#
library(CASdatasets)
data(ausprivauto0405)
head(ausprivauto0405)

########################################
#####第6章
#
library(MASS)
str(Boston)

#
?Boston

#
apply(Boston, MARGIN = 2, function(x) {sum(is.na(x))})

#
apply(Boston, MARGIN = 2, function(x){sum(!is.na(x))})

#
xy <- Boston
colnames(xy)[ncol(xy)] <- "y"
str(xy[ncol(xy)])

#
n <- nrow(xy)
set.seed(2018, sample.kind = "Rounding")
test.id <- sample(n, round(n / 4))
test <- xy[test.id, ]
train <- xy[-test.id, ]

#
str(test)
str(train)

#
dim(test)
dim(train)

#
library(corrplot)
corrplot(
  cor(train, method = "kendall"),
  type = "upper",
  order = "hclust",
  addCoef.col = "gray10",
  number.cex = 0.5
  )

#
summary(train$y)
length(unique(train$y))
hist(train$y)

#
sum(train$y == 50)
hist(train$y, breaks = 100)

#
summary(train[, -ncol(xy)])

#
apply(X = train[, -ncol(xy)],
      MARGIN = 2,
      FUN = function(x) {length(unique(x))})

#
oldpar <- par(no.readonly = TRUE)
par(mfrow = c(3, 5))
for (i in 1:(ncol(xy) - 1)) {
  xname <- colnames(xy)[i]
  hist(train[, i],
       main = paste("Histogram of", xname),
       xlab = xname)
}
par(oldpar)

#
oldpar <- par(no.readonly = TRUE)
par(mfrow = c(3, 5))
for (i in 1:(ncol(xy) - 1)) {
  xname <- colnames(xy)[i]
  plot(train[, i], train$y, pch = ".", xlab = xname)
}
par(oldpar)

#
i <- 13
xname <- colnames(xy)[i]
plot(train[, i], train$y, xlab = xname)
lines(lowess(train[, i], train$y))

#
xname <- "indus"
hist(train[, xname],
     breaks = 100,
     main = paste("Histogram of", xname),
     xlab = xname)

#
names(which.max(table(train$indus)))
sum(train$indus == 18.1)

#
summary(train[train$indus == 18.1, ])

#
sum(train[, "rad"] == 24)
nrow(train[train$tax == 666,])

#
var(train$y[train$rad == 24])
var(train$y[!train$rad == 24])

#
library(randomForest)
set.seed(2018)
boston.rf <- randomForest(y ~ .,
                          data = train,
                          importance = TRUE)

#
pred <- predict(boston.rf, newdata = test)
plot(test$y, pred, main = boston.rf$call)
curve(identity, add = TRUE)
rms <- function(act, pred) {
  sqrt(mean((act - pred) ^ 2))
}
cat(" RMSE =", rms(test$y, pred))

#
cat(" RMSE = ",
    rms(test$y,
        predict(lm(y ~ ., data = train), newdata = test)))

#
boston.imp <-
  sort(importance(boston.rf, type = 1, scale = FALSE)[, 1],
       decreasing = TRUE)
barplot(boston.imp, names.arg = rownames(boston.imp))

#
library(pdp)
ice <- partial(object = boston.rf,
               pred.var = c("lstat"),
               ice = TRUE)
plotPartial(ice)

#
pdp <- partial(object = boston.rf,
               pred.var = c("lstat"))
plot(pdp, type = "l", col = "red")

#
oldpar <- par(no.readonly = TRUE)
par(mfrow = c(3, 5))
for (i in 1:(ncol(xy) - 1)) {
  xname <- colnames(xy)[i]
  pdp <- partial(object = boston.rf,
                 pred.var = c(xname))
  plot(pdp, type = "l", col = "red")
  abline(h = mean(train$y))
}
par(oldpar)

#
xlim <- range(train$lstat)
ylim <- range(train$y)
h <- mean(train$y)
plot(train[, "lstat"], train$y, pch = 20, col = "gray", 
     xlim = xlim, ylim = ylim, axes = FALSE, ann = FALSE)
par(new = TRUE)
plot(pdp, type = "l", col = "red", xlim = xlim, ylim = ylim)
par(new = TRUE)
plot(lowess(train[, "lstat"], train$y), type = "l", 
     xlim = xlim, ylim = ylim, 
     axes = FALSE, ann =FALSE)
abline(h = h)

#
ice <- partial(
  object = boston.rf,
  pred.var = c("indus"),
  ice = TRUE,
  center = TRUE
  )
plotPartial(ice)

#
oldpar <- par(no.readonly = TRUE)
par(mfrow = c(2, 4))
for(i in 1:(ncol(xy) - 1)) {
  xname <- colnames(xy)[i]
  pdp <- partial(object = boston.rf,
                 pred.var = c(xname))
  pdp[,2] <- pdp[,2] - pdp[1, 2] 
  ice <- partial(object = boston.rf,
                 pred.var = c(xname),
                 ice = TRUE,
                 center = TRUE)
  xlim <- c(min(ice[, 1]), max(ice[, 1]))
  ylim <- c(-26, 20)
  plot(ice[ice[, 3] == 1, 1:2],
       type = "l",
       xlim = xlim,
       ylim = ylim)
  for(j in 2:max(ice[,3])){
    par(new = TRUE)
    plot(ice[ice[, 3] == j, 1:2], 
         type = "l",
         xlim = xlim,
         ylim = ylim,
         axes = FALSE,
         ann = FALSE)
  }
  par(new = TRUE)
  plot(pdp, 
       type = "l",
       col = "red",
       xlim = xlim,
       ylim = ylim)
}
par(oldpar)

#
pdp <- 
  partial(object = boston.rf,
          pred.var = c("lstat", "rm"),
          chull = TRUE  # assure points exist in convex hull
          )
plotPartial(pdp, contour = TRUE) 
plotPartial(pdp, 
            levelplot = FALSE, 
            drape = TRUE,
            screen = list(z = -40, x = -60))

########################################
#####第7章
#
SEED <- 2018

#
library(MASS)
xy <- Boston; colnames(xy)[ncol(xy)] <- "y"; n <- nrow(xy)
set.seed(SEED, sample.kind = "Rounding")
test.id <- sample(n, round(n / 4))
test <- xy[test.id, ]; train <- xy[-test.id, ]

#
rms <- function(act, pred) {sqrt(mean((act - pred) ^ 2))}

#
library(rpart)
tree <- rpart(y ~ ., data = train)

#
par(xpd = NA)
plot(tree)
text(tree, use.n = TRUE)
par(xpd = FALSE)

#
cat(" RMSE(tree) =",
    rms(test$y, predict(tree, newdata = test)),
    "\t RMSE(lm) =",
    rms(test$y, 
        predict(lm(y ~ ., data = train), newdata = test)))

#
set.seed(SEED)
maxTree <- rpart(y ~ ., data = train, cp = 0)
cps <- maxTree$cptable
cp <-
  cps[which.min(
    cps[, 4] > cps[nrow(cps), 4] + cps[nrow(cps), 5]
    ), 1]
bestTree <- rpart(y ~ ., data = train, cp = cp)
cat(" RMSE(bestTree) =",
    rms(test$y, predict(bestTree, newdata = test)))

#
library(xgboost)
set.seed(SEED)
model <- xgboost(data = as.matrix(train[,-14]),
                 label = train$y,
                 nrounds = 3100,
                 max_depth = 6,
                 eta = 0.01,
                 gamma = 0.6,
                 colsample_bytree = 0.8,
                 min_child_weight = 1,
                 subsample = 0.7,
                 verbose = 0)

#
cat(" RMSE =",
    rms(test$y,
        predict(model, newdata = as.matrix(test[, -14]))))

#
model <- glm(y ~ ., family = Gamma(log), data = train)

#
pred <- predict(model, newdata = test, type = "response")
plot(test$y, pred, main = model$call)
curve(identity, add = TRUE)
cat(" RMSE =", rms(test$y, pred))

#
glm_model <- model <-
  glm(y ~ (.) ^ 2, family = Gamma(log), data = train)
cat(" Number of coefficients =", length(coef(glm_model)))

#
pred <- predict(model, 
                newdata = test, 
                type = "response")
plot(test$y, pred, main = model$call)
curve(identity, add = TRUE)
cat("\n RMSE =", rms(test$y, pred))

#
step_model <- step(glm_model, trace = 0)
pred <- predict(step_model, 
                newdata = test, 
                type = "response")
cat(" RMSE =", rms(test$y, pred))

#
AIC(step_model)
AIC(step(glm(y ~ 1, family = Gamma(log), data = train), 
         direction = "forward", 
         scope = "y ~ (crim + zn + indus + chas + nox + rm + 
           age + dis + rad + tax + ptratio + black + lstat)^2",
         trace = 0))

#
A <- matrix(c(1.42857, 5.71429, 2.85714, 11.4286), 
            nrow = 2)
b <- c(4.28571, 17.1429)
ans <- solve(A, b)
cat(" x =", ans[1], "\t y =", ans[2])

#
A <- matrix(c(1.428571, 5.714286, 2.857143, 11.42857),
            nrow = 2)
b <- c(4.285714, 17.14286)
ans <- solve(A, b)
cat(" x =", ans[1], "\t y =", ans[2])

#
library(glmnetUtils)
lambdas <- 0.1 ^ seq(1, 3, length.out = 100)
bostonGlmnet <- function(alpha) {
  set.seed(SEED)
  cv.result <- model <- cv.glmnet(
    y ~ (crim + zn + indus + chas + nox + rm + age + dis +
           rad + tax + ptratio + black + lstat) ^ 2,
    data = train,
    #nfolds = nrow(train),
    alpha = alpha,
    lambda = lambdas
    )
  cat(" lambda.min =", lambda.min <- cv.result$lambda.min)
  #data.frame(lambda = cv.result$lambda, cvm = cv.result$cvm)
  pred <- predict(cv.result, newdata = test, s = lambda.min)
  plot(test$y, pred, 
       main = paste0("glmnet(alpha = ", alpha, ")"))
  curve(identity, add = TRUE)
  cat("\n RMSE =", rms(test$y, pred))
  return(cv.result)
}
cv.result <- bostonGlmnet(alpha = 0)

#
cv.result <- bostonGlmnet(alpha = 1)
#coef(cv.result, s = cv.result$lambda.min)

#
df <- data.frame()
for(alpha in seq(0, 1, by = 0.1)) {
  set.seed(SEED)
  cv.result <- cv.glmnet(
    y ~ (crim + zn + indus + chas + nox + rm + age +
           dis + rad + tax + ptratio + black + lstat) ^ 2,
    data = train,
    #nfolds = nrow(train),
    alpha = alpha,
    lambda = lambdas
    )
  df <- rbind(df,
              data.frame(
                alpha = alpha,
                lambda.min = cv.result$lambda.min,
                cvm.min = min(cv.result$cvm)
                ))
}
df

#
cat(" alpha.min =",
    alpha.min <- df[which.min(df$cvm.min), "alpha"],
    "\t lambda.min =",
    lambda.min <- df[which.min(df$cvm.min), "lambda.min"])

#
library(mgcv)
model <- gam(
  y ~ s(crim) + s(zn) + s(indus) + chas + s(nox) + 
    s(rm) + s(age) + s(dis) + rad + s(tax) + s(ptratio) +
    s(black) + s(lstat),
  data = train,
  family = Gamma(log)
)
plot(model, residuals = TRUE, se = FALSE, pages = 2)

pred <- predict(model, newdata = test, type = "response")
plot(test$y, pred, main = "GAM")
curve(identity, add = TRUE)
cat(" RMSE =", rms(test$y, pred))

########################################
#####第8章
#
SEED <- 2018
library(MASS)
xy <- Boston; colnames(xy)[ncol(xy)] <- "y"; n <- nrow(xy)

#
set.seed(SEED, sample.kind = "Rounding")
half <- xy[sample(n, round(n / 2)), ]
#str(half)

#
nfolds <- 10
set.seed(SEED, sample.kind = "Rounding")
cv.no <- split(sample(1:nrow(xy)), 1:nfolds)
str(cv.no)

#
err <- function(act, pred) {
  sum(((act - pred) ^ 2)[act < 50])
}

#
lmPred <- function(train, fitting){
  predict(lm(y ~ ., data = train), newdata = fitting)
}

#
doCV <- function(data, cv.pred) {
  total_err <- 0
  for (i in 1:nfolds) {
    cv.train <- data[-cv.no[[i]], ]
    cv.valid <- data[cv.no[[i]], ]
    pred <- cv.pred(cv.train, cv.valid)
    total_err <- total_err + err(cv.valid$y, pred)
  }
  return(total_err)
}

(result <- doCV(xy, lmPred))

#
cat(" RMSE =", lm.rmse <- sqrt(result / sum(xy$y < 50)))

#
glmPred <- function(train, fitting) {
  predict(glm(y ~ (.) ^ 2, 
              data = train, 
              family = Gamma(log)),
          newdata = fitting,
          type = "response")
}

cat(" RMSE =", 
    glm.rmse <- sqrt(doCV(xy, glmPred) / sum(xy$y < 50)))

#
library(randomForest)
defaultRFPred <- function(train, fitting) {
  set.seed(SEED)
  predict(randomForest(y ~ ., data = train), 
          newdata = fitting)
}

cat(" RMSE =",
    defaultRF.rmse <- 
      sqrt(doCV(xy, defaultRFPred) / sum(xy$y < 50)))

#
library(glmnetUtils)
lambdas <- 0.1 ^ seq(2, 4, length.out = 100)
lassoPred <- function(train, fitting) {
  set.seed(SEED)
  cv.result <- cv.glmnet(
    y ~ (crim + zn + indus + chas + nox + rm + age + 
           dis + rad + tax + ptratio + black + lstat) ^ 2,
    data = train, alpha = 1, lambda = lambdas, nfolds = 20
  )
  cat("\n lambda.min =", 
      lambda.min <- cv.result$lambda.min)
  predict(cv.result, newdata = fitting, s = lambda.min) 
}

cat("\n RMSE =",
    lasso.rmse <- sqrt(doCV(xy, lassoPred) / sum(xy$y < 50)))

#
detailedCV <- function(data, cv.pred, name = NULL) {
  total_err <- 0 ## "err"はバリデーションデータの誤差（error）の意
  total_res <- 0 ## "res"は学習データの残差（residual）の意
  df <- data.frame() ## 結果を表示するためのData frame
  y <- vector()
  yhat <- vector()
  for (i in 1:nfolds) {
    cv.train <- data[-cv.no[[i]], ] 
    cv.valid <- data[cv.no[[i]], ]
    fit <- cv.pred(cv.train, cv.train)
    residual <- err(cv.train$y, fit)
    total_res <- total_res + residual
    pred <- cv.pred(cv.train, cv.valid)
    error <- err(cv.valid$y, pred)
    total_err <- total_err + error
    df <- rbind(
      df,
      data.frame(
        fold = i,
        train.size = sum(cv.train$y < 50),
        RMSR =
          round(sqrt(residual / sum(cv.train$y < 50)), 6),
        valid.size = sum(cv.valid$y < 50),
        RMSE =
          round(sqrt(error / sum(cv.valid$y < 50)), 6)
        )
      )
    y <- c(y, cv.valid$y)
    yhat <- c(yhat, pred)
  }
  plot(y, yhat, main = name)
  curve(identity, add = TRUE)
  df <- rbind(
    df,
    c(0,
      sum(df[, 2]) / nfolds,
      round(sqrt(total_res / sum(df[, 2])), 6),
      sum(df[, 4]) / nfolds,
      round(sqrt(total_err / sum(df[, 4])), 6)
      )
    )
  df[11, 1] <- "Mean"
  return(df)
}

detailedCV(xy, glmPred, "GLM")

#
library(mgcv)
gamPred <- function(train, fitting) {
  model <- gam(
    y ~ s(crim) + s(zn) + s(indus) + chas + s(nox) + 
      s(rm) + s(age) + s(dis) + rad + s(tax) + 
      s(ptratio) + s(black) + s(lstat),
    data = train,
    family = Gamma(log)
  )
  predict(model, newdata = fitting, type = "response")
}

(result <- detailedCV(xy, gamPred, "GAM"))

gam.rmse <- as.numeric(result[nfolds + 1, "RMSE"])

#
elastic0Pred <- function(train, fitting, parallel){
  alphas <- seq(0, 1, by = 0.1)
  lambdas <- 0.1 ^ seq(1, 5, length.out = 200)
  k <- length(alphas)
  zeros <- rep(0, k)
  df <- data.frame(alpha = zeros,
                   lambda.min = zeros,
                   cvm.min = zeros)
  lst <- split(rep(NA, k), 1:k)
  for(i in 1:k){
    alpha <- alphas[i]
    set.seed(SEED)
    cv.result <- cv.glmnet(
      y ~ (crim + zn + indus + chas + nox + rm + age + 
             dis + rad + tax + ptratio + black + lstat) ^ 2,
      data = train, nfolds = 20,
      alpha = alpha, lambda = lambdas, parallel = parallel)
    df[i, ] <- 
      c(alpha, cv.result$lambda.min, min(cv.result$cvm))
    lst[[i]] <- cv.result
  }
  best <- which.min(df$cvm.min)
  #cat("\n range of lambda.min:", range(df[, "lambda.min"]))
  cat(" alpha.min =", 
      alpha.min <- format(df[best, "alpha"], nsmall = 1),
      "\t lambda.min =", 
      lambda.min <- df[best, "lambda.min"], 
      "\n")
  predict(lst[[best]], newdata = fitting, s = lambda.min)
}

elasticFPred <- function(train, fitting) {
  elastic0Pred(train, fitting, FALSE)
}

system.time(
  cat(" RMSE =",
      sqrt(doCV(xy, elasticFPred) / sum(xy$y < 50)),
      "\n"))

#
library(parallel)
library(doParallel)
cl <- makePSOCKcluster(detectCores())
registerDoParallel(cl)

elasticTPred <- function(train, fitting) {
  elastic0Pred(train, fitting, TRUE)
}

system.time(
  cat(" RMSE =",
      elastic.rmse <- 
        sqrt(doCV(xy, elasticTPred) / sum(xy$y < 50)),
      "\n")
)

stopCluster(cl)

#
library(ranger)
ranger(y ~ ., data = half)

#
library(caret)
rfCV <- function(train) {
  rf_grid <- expand.grid(
    mtry = c(3, 5, 7),
    splitrule = "variance",
    min.node.size = c(3, 5, 7)
    )
  set.seed(SEED)
  model <- train(
    y ~ .,
    data = train,
    method = "ranger",
    num.trees = 500,
    trControl = trainControl(method = "cv",
                             number = 10,
                             search = "grid"),
    tuneGrid = rf_grid
    )
  model
}

#
cl <- makePSOCKcluster(detectCores())
registerDoParallel(cl)

rfCV(half)

stopCluster(cl)

#
rfPred <- function(train, fitting) {
  predict(rfCV(train), newdata = fitting)
}

#
cl <- makePSOCKcluster(detectCores())
registerDoParallel(cl)

cat(" RMSE =", 
    rf.rmse <- sqrt(doCV(xy, rfPred) / sum(xy$y < 50)))
#detailedCV(xy, rfPred, "Random Forest")

stopCluster(cl)

#
library(xgboost)
xgbCV <- function(train) {
  xgbGrid <- expand.grid(
    nrounds = c(3000, 4000),
    max_depth = c(6),
    eta = c(0.01, 0.02),
    gamma = c(0.6),
    subsample = c(0.7),
    colsample_bytree = c(0.8),
    min_child_weight = c(1)
    )
  set.seed(SEED)
  model <- train(
    y ~ .,
    data = train,
    method = "xgbTree",
    num.trees = 500,
    trControl = trainControl(method = "cv",
                             number = 10,
                             search = "grid"),
    tuneGrid = xgbGrid
    )
  model
}

#
cl <- makePSOCKcluster(detectCores())
registerDoParallel(cl)

xgbCV(half)

stopCluster(cl)

#
#xgbPred <- function(train, fitting){
#  predict(xgbCV(train), newdata = fitting)
#}
#
#cl <- makePSOCKcluster(detectCores())
#registerDoParallel(cl)
#
#cat("\n RMSE =", 
#    sqrt(doCV(xy, xgbPred) / sum(xy$y < 50)))
#
#stopCluster(cl)

#
xgbPred <- function(train, fitting){
  set.seed(SEED)
  model <- xgboost(
    data = as.matrix(train[, -14]),
    label = train$y,
    nrounds = 4000,
    max_depth = 6,
    eta = 0.02,
    gamma = 0.6,
    colsample_bytree = 0.8,
    min_child_weight = 1,
    subsample = 0.7,
    verbose = 0
    )
  predict(model, newdata = as.matrix(fitting[, -14]))
}

cat(" RMSE =", 
    xgb.rmse <- sqrt(doCV(xy, xgbPred) / sum(xy$y < 50)))
#detailedCV(xy, xgbPred, "XGBoost")

#
c(LM = lm.rmse, GLM = glm.rmse, defaultRF = defaultRF.rmse,
  LASSO = lasso.rmse, ENet = elastic.rmse, GAM = gam.rmse, 
  RF = rf.rmse, XGBoost = xgb.rmse)

########################################
#####第9章
#
SEED <- 2018

#
install.packages(c("xts", "sp"))
install.packages(
  "CASdatasets",
  repos = "http://dutangc.free.fr/pub/RRepos/",
  type = "source",
  dependencies = TRUE
)

#
library(CASdatasets)
data("ausprivauto0405")

#
aus.df <- ausprivauto0405

#
load(file = "./data/ausprivauto0405.rda")

#
str(aus.df)

#
summary(aus.df)

#
summary(aus.df$VehBody)

#
apply(aus.df, MARGIN = 2, FUN = function(x) sum(is.na(x)))

#
set.seed(SEED, sample.kind = "Rounding")
hold.out.num <-
  sample(seq(nrow(aus.df)), round(nrow(aus.df) / 4))
aus.df["isHoldOut"] <- FALSE
aus.df[hold.out.num, "isHoldOut"] <- TRUE
train <- aus.df[!aus.df$isHoldOut, ]
hold.out <- aus.df[aus.df$isHoldOut, ]
dim(train)
dim(hold.out)

#
(a <- nrow(aus.df))
(b <- sum(aus.df$ClaimOcc))
b / a * 100

#
berDev <- function(y, yhat) {
  -2 * mean(ifelse(y == 0, log(1 - yhat), log(yhat)))
}

#
(pred <- sum(train$ClaimOcc) / nrow(train))

#
cat(" Deviance =", 
    mean.dev <- berDev(hold.out$ClaimOcc, pred))

#
Pos <- hold.out$Exposure[hold.out$ClaimOcc == 1]
Neg <- hold.out$Exposure[hold.out$ClaimOcc == 0]
fp <- function(theta) sum(Neg > theta)/ length(Neg)
tp <- function(theta) sum(Pos > theta)/ length(Pos)
for(theta in seq(0, 1, 0.01)){
  plot(x = fp(theta), y = tp(theta), 
       xlim = c(0, 1), ylim = c(0, 1))
  par(new = TRUE)
}
par(new = FALSE)

#
library(ROCR)
preds <- prediction(hold.out$Exposure, hold.out$ClaimOcc)
perf <- performance(preds, "tpr", "fpr")
exposure.auc <- performance(preds, "auc")@y.values[[1]]
plot(perf,
     main = paste("AUC =", round(exposure.auc, 5)))
curve(identity, lty = "dotted", add = TRUE)

#
performance(prediction(rep(pred, nrow(hold.out)),
                       hold.out$ClaimOcc),
            "auc")@y.values[[1]]

#
berDev(hold.out$ClaimOcc, hold.out$Exposure)

#
expectedAUC <- function(c) {(8 - 3 * c) / (12 - 6 * c)}
plot(expectedAUC, from = 0, to = 1, ylim = c(0.5, 1), 
     xlab = "c")
abline(h = 0.7, lty = "dotted")

#
curve(log(x / (1 - x)), from = 1e-10, to = 1 - 1e-10)

#
model <-
  glm(ClaimOcc ~ ., data = train[1:7],
      family = binomial(logit))

#
pred <-
  predict(model, newdata = hold.out, type = "response")
cat(" Deviance(hold.out) =",
    logistic.dev <- berDev(hold.out$ClaimOcc, pred),
    "\n AUC(hold.out) =",
    logistic.auc <-
      performance(prediction(pred, hold.out$ClaimOcc),
                  "auc")@y.values[[1]]) 

#
pred <-
  predict(model, newdata = train, type = "response")
cat(" Deviance(train) =", 
    berDev(train$ClaimOcc, pred),
    "\n AUC(train) =", 
    performance(prediction(pred, train$ClaimOcc),
                "auc")@y.values[[1]]) 

#
summary(model)

#
library(randomForest)
set.seed(SEED)
model <-
  randomForest(as.factor(1 - ClaimOcc) ~ .,
               data = train[1:7])

#
pred <- predict(model, newdata = hold.out, type = "prob")
head(pred)
cat(" Deviance =",
    RF.dev <- berDev(hold.out$ClaimOcc, pred[, 1]))

#
sum(hold.out$ClaimOcc == 1 & pred[, 1] == 0)

#
cat(" AUC =",
    RF.auc <-
      performance(preds <-
                    prediction(pred[, 1], hold.out$ClaimOcc),
                  "auc")@y.values[[1]])

#
library(ranger)
set.seed(SEED)
model <- ranger(as.factor(1 - ClaimOcc) ~ .,
                data = train[1:7],
                probability = TRUE)

pred <-
  predict(model, data = hold.out, verbose = 0)$predictions
head(pred)
cat(" Deviance =",
    ranger.dev <- berDev(hold.out$ClaimOcc, pred[, 1]),
    "\n AUC =",
    ranger.auc <-
      performance(preds <-
                    prediction(pred[, 1],
                               hold.out$ClaimOcc),
                  "auc")@y.values[[1]])

#
pred <- predict(model, data = train)$predictions
cat(
  " Deviance(train) =",
  berDev(train$ClaimOcc, pred[, 1]),
  "\n AUC(train) =",
  performance(preds <-
                prediction(pred[, 1], train$ClaimOcc),
              "auc")@y.values[[1]])

#
set.seed(SEED)
model <- ranger(as.factor(1 - ClaimOcc) ~ .,
                data = train[1:7],
                probability = TRUE,
                num.trees = 2000,
                mtry = 3,
                min.node.size = 1,
                max.depth = 4,
                sample.fraction = 0.3,
                verbose = 0)

pred <- predict(model, data = hold.out)$predictions

cat(" Deviance =",
    tuned.ranger.dev <- 
      berDev(hold.out$ClaimOcc, pred[, 1]),
    "\n AUC =",
    tuned.ranger.auc <- performance(
      preds <- prediction(pred[, 1], hold.out$ClaimOcc),
      "auc")@y.values[[1]])

#
pred <- predict(model, data = train)$predictions
cat(" Deviance(train) =", 
    berDev(train$ClaimOcc, pred[,1]),
    "\n AUC(train) =", 
    performance(
      preds <- prediction(pred[, 1], train$ClaimOcc),
      "auc")@y.values[[1]])

#
tuned.ranger.model <- model

#
model <- glm(ClaimNb ~ . - Exposure,
             offset = log(Exposure),
             data = train[c(1:6, 8)],
             family = poisson)

cat(" AIC =", AIC(model))

#
pred <-
  1 - exp(-predict(model, newdata = hold.out,
                   type = "response"))

cat(" Deviance(hold.out) =", 
    berDev(hold.out$ClaimOcc, pred),
    "\n AUC(hold.out) =", 
    performance(prediction(pred, hold.out$ClaimOcc),
                "auc")@y.values[[1]]) 

#
model <- glm(ClaimNb ~ . + log(Exposure),
             data = train[c(1:6, 8)],
             family = poisson)

cat(" AIC =", AIC(model))

#
summary(model)

#
pred <-
  1 - exp(-predict(model, newdata = hold.out,
                   type = "response"))
cat(" Deviance(hold.out) =", 
    poisson.dev <- berDev(hold.out$ClaimOcc, pred),
    "\n AUC(hold.out) =", 
    poisson.auc <-
      performance(prediction(pred, hold.out$ClaimOcc),
                  "auc")@y.values[[1]])

#
library(glmnetUtils)
set.seed(SEED)
model <- cv.glmnet(
  ClaimNb ~ VehValue + VehAge + VehBody + Gender + DrivAge
  + Exposure + log(Exposure),
  family = "poisson",
  data = train,
  alpha = 1,
  lambda = 0.1 ^ seq(1, 7, length.out = 100)
  )

(lambda.min <- model$lambda.min)

coef <- coef(model, s = lambda.min)

cat(" nzero =", sum(coef == 0))

#
pred <- 1 - exp(-predict(object = model,
                         s = lambda.min,
                         newdata = hold.out,
                         type = "response"))
cat(" Deviance(hold.out) =",
    lasso.dev <- berDev(hold.out$ClaimOcc, pred),
    "\n AUC(hold.out) =",
    lasso.auc <-
      performance(prediction(pred, hold.out$ClaimOcc),
                  "auc")@y.values[[1]])

#
library(mgcv)
model <- gam(
  ClaimNb ~ s(VehValue) + VehAge + VehBody + Gender
  + DrivAge + s(log(Exposure)),
  data = train,
  family = poisson
  )

#
plot(model, residuals = FALSE, se = FALSE, pages = 1 )

#
pred <- as.vector(1 - exp(-predict(
  model, newdata = hold.out,type = "response")))
cat(" Deviance(hold.out) =", 
    gam.dev <- berDev(hold.out$ClaimOcc, pred),
    "\n AUC(hold.out) =", 
    gam.auc <-
      performance(prediction(pred, hold.out$ClaimOcc),
                  "auc")@y.values[[1]])

#
list(Deviance = 
       sort(c(mean = mean.dev,
              Logistic = logistic.dev,
              RF = RF.dev,
              ranger = ranger.dev,
              tuned.ranger = tuned.ranger.dev,
              poisson = poisson.dev,
              LASSO = lasso.dev,
              GAM = gam.dev)),
     AUC = 
       sort(c(Exposure = exposure.auc,
              Logistic = logistic.auc,
              RF = RF.auc,
              ranger = ranger.auc,
              tuned.ranger = tuned.ranger.auc,
              poisson = poisson.auc,
              LASSO = lasso.auc,
              GAM = gam.auc),
            decreasing = TRUE))

########################################
#####補章
#
SEED <- 2018

#
library(CASdatasets)
data("ausprivauto0405")
aus.df <- ausprivauto0405

#
load(file = "./data/ausprivauto0405.rda")

#
berDev <- function(y, yhat) {
  -2 * mean(ifelse(y == 0, log(1 - yhat), log(yhat)))
}
library(ROCR)

#
## VehAge
aus.df[, "VehAge"] <- as.character(aus.df$VehAge)
ord.map <-
  c("oldest cars", "old cars", "young cars", "youngest cars")
for(om in ord.map) {
  aus.df[aus.df$VehAge == om, "VehAge"] <-
    which(ord.map == om)
}
aus.df[, "VehAge"] <- as.integer(aus.df$VehAge)
aus.df[, "VehAge"] <- as.ordered(aus.df$VehAge)

## DriveAge
aus.df[, "DrivAge"] <- as.character(aus.df$DrivAge)
ord.map <- c("oldest people", 
             "old people", 
             "older work. people",
             "working people",
             "young people", 
             "youngest people")
for(om in ord.map) {
  aus.df[aus.df$DrivAge == om, "DrivAge"] <-
    which(ord.map == om)
}
aus.df[, "DrivAge"] <- as.integer(aus.df$DrivAge)
aus.df[, "DrivAge"] <- as.ordered(aus.df$DrivAge)

#
set.seed(SEED, sample.kind = "Rounding")
hold.out.num <- sample(seq(nrow(aus.df)),
                       round(nrow(aus.df) / 4))
aus.df["isHoldOut"] <- FALSE
aus.df[hold.out.num, "isHoldOut"] <- TRUE

#
library(devtools)
install_github("kkondo1981/aglm", build_vignettes = TRUE)

#
library(aglm)

#
aus.xy <- cbind(logExpo = log(aus.df[, 1]), aus.df[, c(1:8)])
train.x <- aus.xy[!aus.df$isHoldOut, 1:7]
hold.out.x <- aus.xy[aus.df$isHoldOut, 1:7]
train.y <- aus.xy$ClaimNb[!aus.df$isHoldOut]
hold.out.Occ <- aus.xy$ClaimOcc[aus.df$isHoldOut]

#
set.seed(SEED)
cv.model <- cv.aglm(
  x = train.x,
  y = train.y,
  family = "poisson",
  add_interaction_columns = FALSE,
  alpha = 1,
  lambda = 0.1 ^ seq(1, 4, length.out = 100)
)
(lambda.min <- cv.model@lambda.min)

#
plot(cv.model, s = lambda.min, verbose = 0)

#
pred <- 1 - exp(-predict(cv.model,
                         newx = hold.out.x,
                         s = lambda.min,
                         type = "response"))

cat(" Deviance(hold.out) =", 
    aglm.dev <- berDev(hold.out.Occ, pred),
    "\n AUC(hold.out) =", 
    aglm.auc <- performance(prediction(pred, hold.out.Occ),
                            "auc")@y.values[[1]])