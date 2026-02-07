# パッケージ読み込み
required_packages <- c(
  "tidyverse", "ranger", "xgboost", "iml", "gridExtra", "midr", "DALEX", "DALEXtra", "nnet", "grid"
)
new_packages <- required_packages[!(required_packages %in% installed.packages()[,"Package"]) ]
if(length(new_packages)) install.packages(new_packages, repos = "https://cran.ism.ac.jp/")
library(tidyverse)
library(ranger)
library(xgboost)
library(nnet)
library(iml)
library(gridExtra)
library(midr)
library(DALEX)
library(DALEXtra)
library(grid)

# データ読み込み
url <- "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
wine <- read.csv(url, sep = ";")
colnames(wine)[ncol(wine)] <- "y"

# 注意: dplyr::select が他パッケージと衝突するときがあるため、ベースRを使って安全に列を除去します
x <- wine[ , setdiff(names(wine), "y")]
y <- wine$y

# 分布表示
p_dist1 <- ggplot(wine, aes(x = y)) + geom_bar(fill = "steelblue") + labs(title = "Quality Distribution")
p_dist2 <- ggplot(wine, aes(x = alcohol, y = volatile.acidity, color = as.factor(y))) + geom_point(alpha = 0.5) + labs(title = "Alcohol vs Acidity by Quality")
grid.arrange(p_dist1, p_dist2, ncol = 2)

# モデル学習
wine_scaled <- as.data.frame(scale(wine[ , setdiff(names(wine), "y")]))
wine_scaled$y <- wine$y

cat("Learning models...
")
model_list <- list(
  "Linear_Regression" = lm(y ~ ., data = wine),
  "Random_Forest"    = ranger(y ~ ., data = wine, importance = "permutation"),
  "XGBoost"          = xgboost(data = as.matrix(x), label = y, nrounds = 50, verbose = 0, params = list(objective = "reg:squarederror")),
  "Neural_Network"   = nnet(y ~ ., data = wine_scaled, size = 5, linout = TRUE, trace = FALSE, maxit = 500)
)

# iml による一括解析ループ
pdf("Wine_XAI_IML_Report.pdf", width = 18, height = 14)
for (name in names(model_list)) {
  cat("Processing:", name, "
")
  mod <- model_list[[name]]

  p_fun <- function(object, newdata) {
    newdata_df <- as.data.frame(newdata)
    if (inherits(object, "ranger")) return(predict(object, data = newdata_df)$predictions)
    if (inherits(object, "xgb.Booster")) return(predict(object, as.matrix(newdata_df)))
    if (inherits(object, "nnet")) return(as.numeric(predict(object, newdata_df)))
    return(as.numeric(predict(object, newdata_df)))
  }

  current_x <- if(name == "Neural_Network") wine_scaled %>% dplyr::select(-y) else x
  current_y <- if(name == "Neural_Network") wine_scaled$y else y
  current_data <- if(name == "Neural_Network") wine_scaled else wine

  predictor <- Predictor$new(mod, data = current_x, y = current_y, predict.fun = p_fun)

  p1 <- plot(FeatureImp$new(predictor, loss = "rmse")) + ggtitle("PFI (Importance)")
  p5 <- plot(Interaction$new(predictor, feature = "alcohol")) + ggtitle("Interaction (H-stat for Alcohol)")
  p2 <- plot(FeatureEffect$new(predictor, feature = "alcohol", method = "pdp+ice")) + ggtitle("PD & ICE (Alcohol)")
  p3 <- plot(FeatureEffect$new(predictor, feature = "alcohol", method = "ale")) + ggtitle("ALE (Alcohol)")

  # Grouped PDP: PDP カーブを作成（色分けなし）
  if ("volatile.acidity" %in% colnames(current_x)) {
    p4 <- plot(FeatureEffect$new(predictor, feature = "alcohol", method = "pdp")) + ggtitle("Grouped PDP (Alcohol Effect)")
  } else {
    p4 <- ggplot() + labs(title = "Grouped PDP (not available)")
  }

  shapley <- Shapley$new(predictor, x.interest = current_x[1, ])
  p6 <- plot(shapley) + ggtitle("SHAP (Shapley) for Sample #1")

  tryCatch({
    res_mid <- midr::interpret(y ~ (.)^2, data = current_data, model = mod, predict_function = p_fun)
    p9 <- ggmid(mid.importance(res_mid), type = "heatmap", theme = "Oslo") + labs(title = "MID Heatmap", subtitle = paste("UR:", round(res_mid$ratio, 4)))
  }, error = function(e) { p9 <<- ggplot() + labs(title = "MID Error") })

  grid.arrange(p1, p5, p6, p9, ncol = 2, top = textGrob(paste("Model:", name), gp=gpar(fontSize=22, font=2)))
  grid.arrange(p2, p3, p4, ncol = 2, top = textGrob(paste(name, ": Alcohol Effects"), gp=gpar(fontSize=22, font=2)))
}
dev.off()
cat("Done! Report saved as Wine_XAI_IML_Report.pdf\n")
