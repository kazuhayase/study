##########GLM##########
# 必要なパッケージをロード
library(catdata)

### For reproducibility ###
SEED <- 2020

### Data ###
data("rent", package = "catdata")
y <- rent$rentm
xnames <- setdiff(colnames(rent), c("rent", "rentm"))
x <- rent[, colnames(rent) %in% xnames]
x$area <- as.factor(x$area)
xy <- cbind(x, y)
n <- nrow(xy)

### Holdout ###
set.seed(SEED)
test.id <- sample(n, round(n / 4))
test <- xy[test.id, ]
train <- xy[-test.id, ]

### Loss function: RMS ###
rms <- function(act, pred) {sqrt(mean((act - pred) ^ 2))}

# GLMモデルの構築 (ガンマ分布とログリンク関数を使用)
model <- glm(y ~ ., family = Gamma(link = "log"), data = train)

# テストデータでの予測
test$pred <- predict(model, test, type = "response")

# RMS損失の計算
loss <- rms(test$y, test$pred)
print(paste("RMS loss:", loss))

###########LASSO##########

# 必要なパッケージをロード
library(catdata)
library(glmnet)

### For reproducibility ###
SEED <- 2020

### Data ###
data("rent", package = "catdata")
y <- rent$rentm
xnames <- setdiff(colnames(rent), c("rent", "rentm"))
x <- rent[, colnames(rent) %in% xnames]
x$area <- as.factor(x$area)
xy <- cbind(x, y)
n <- nrow(xy)

### Holdout ###
set.seed(SEED)
test.id <- sample(n, round(n / 4))
test <- xy[test.id, ]
train <- xy[-test.id, ]

### Loss function: RMS ###
rms <- function(act, pred) {sqrt(mean((act - pred) ^ 2))}

# LASSOモデルの構築
x_train <- model.matrix(y ~ . - 1, data=train)  # '- 1' はインターセプト項を削除するため
y_train <- train$y

# クロスバリデーションを用いたモデルの構築
cv.lasso_model <- cv.glmnet(x_train, y_train, alpha=1)

# テストデータでの予測
x_test <- model.matrix(y ~ . - 1, data=test)  # '- 1' はインターセプト項を削除するため
test$pred <- predict(cv.lasso_model, x_test, s = "lambda.min")

# RMS損失の計算
loss <- rms(test$y, test$pred)
print(paste("RMS loss:", loss))
