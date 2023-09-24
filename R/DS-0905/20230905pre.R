########################################
#####Chapter 3
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

##Q1: Find other useful statistics functions in R.
##Hint: "?cor" See "Usage". See also "See also"
##Another hint: Google, of course.

#
plot(iris$Sepal.Length, pch = as.numeric(iris$Species))
legend("topleft", legend = levels(iris$Species), pch = 1:3)

##Q2: What does pch stand for?
##Hint: "?pch"

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

#Original code, but...
plot(density(iris$Sepal.Length), ylim = c(0, 0.5))
hist(iris$Sepal.Length, probability = TRUE, add = TRUE) #Newly revised

##Q3: How can the figure in the book be reproduced? 


##Q4: Any other way to have a nice(r) one?


#
plot.ecdf(iris$Sepal.Length)

##Q5: Produce some histogram of artificial data.
##Hint: "hist(rpois(1000, 10))" Any other?

#
library(psych)
pairs.panels(iris)

##Message: If you see an error, why don't you ask about it?

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
#####Chapter 6
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
RNGversion("3.5")#To get the same results as the book #Newly added
set.seed(2018)#Newly revised
test.id <- sample(n, round(n / 4))
RNGversion(getRversion())#Newly added
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
