import japanize_matplotlib # これを実行するだけで設定が完了します
import pandas as pd
import numpy as np # 数値計算用のライブラリ（後で使うため、今のうちにインポート）
# 学習データの読み込み
df_train = pd.read_csv('train.csv')

# 予測用データの読み込み
df_test = pd.read_csv('test.csv')
test_id_submission_safe = df_test['Id']

# data_description.txtを読んで内容を理解するために開くことも重要です
# with open('data_description.txt', 'r') as f:
#     print(f.read())
# 行数と列数を確認
print(f"学習データの形状 (行, 列): {df_train.shape}")

# 最初の5行を表示して、データの内容をざっと確認
print("\n学習データの最初の5行:\n", df_train.head())
# 数値型列の基本統計量を確認
print("\n基本統計量の確認:\n", df_train.describe())
print("--- SalePriceの概要統計量 ---")
print(df_train['SalePrice'].describe())

# 歪度（Skewness）と尖度（Kurtosis）を確認
# 歪度: 分布が左右どちらに偏っているかを示す指標。正規分布は0
# 尖度: 分布の鋭さ（尖り具合）を示す指標。正規分布は3（または0）
print(f"\n歪度 (Skewness): {df_train['SalePrice'].skew():.4f}")
print(f"尖度 (Kurtosis): {df_train['SalePrice'].kurt():.4f}")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 対数変換の適用
df_train['SalePrice_Log'] = np.log1p(df_train['SalePrice'])

# trainとtestを結合して、一度に欠損値処理を行うための準備
# Id列は予測には不要なので削除（ただし提出時に必要なのでId列は保存）
# 目的変数のSalePriceはtestには存在しないため、testデータには欠損値として現れる
train_len = len(df_train)
df_all = pd.concat([df_train.drop('SalePrice', axis=1), df_test], axis=0, sort=False)

# SalePriceの対数変換後の値（SalePrice_Log）は、df_trainから結合前に取得・保存しておきます
df_train_log = df_train['SalePrice_Log']

# 欠損値の数と割合を計算し、割合の降順で表示
def get_missing_data_info(df):
    # 欠損値の数
    total = df.isnull().sum().sort_values(ascending=False)
    # 欠損値の割合
    percent = (df.isnull().sum() / df.isnull().count()).sort_values(ascending=False)
    # 結果を結合
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    # 欠損値がある行のみをフィルタリング
    return missing_data[missing_data['Total'] > 0]

missing_info = get_missing_data_info(df_all)
print("--- 結合データセットの欠損値情報（上位） ---")
print(missing_info.head(3))


# 欠損値が「存在しない」ことを示すカテゴリ変数
cols_none = ['PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu', 
             'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond',
             'BsmtExposure', 'BsmtFinType2', 'BsmtFinType1', 'BsmtCond', 
             'BsmtQual', 'MasVnrType', 'MSZoning', 'Utilities', 
             'Functional', 'Exterior1st', 'Exterior2nd', 'KitchenQual',
             'SaleType', 'Electrical']

# .locを使って明示的に代入し、inplace=Trueを避ける
for col in cols_none:
    df_all.loc[df_all[col].isnull(), col] = 'None'
    # または、より簡潔に:
    # df_all[col] = df_all[col].fillna('None')

# ガレージ、地下室の数値特徴量
cols_zero = ['GarageYrBlt', 'GarageArea', 'GarageCars', 
             'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 
             'TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath', 
             'MasVnrArea']

# 0で欠損値を埋める
# .locを使って明示的に代入し、inplace=Trueを避ける
for col in cols_zero:
    df_all.loc[df_all[col].isnull(), col] = 0
    # または、より簡潔に:
    # df_all[col] = df_all[col].fillna(0)

# LotFrontageの補完処理を修正

# 1. Neighborhoodごとの中央値で補完
# transformの戻り値を直接代入します (inplace=Trueは使用しない)
df_all['LotFrontage'] = df_all.groupby('Neighborhood')['LotFrontage'].transform(
    lambda x: x.fillna(x.median())
)
# この transform の処理により、RuntimeWarning の原因となるグループは NaN のまま残ります。

# 2. 残っている欠損値（NaN）を全体のLotFrontageの中央値で補完
# df_all['LotFrontage'].fillna(median_all, inplace=True) の代わりに、
# 戻り値を代入する形式を使います。

if df_all['LotFrontage'].isnull().any():
    # 欠損値がある場合のみ、全体のLotFrontageの中央値を計算
    median_all = df_all['LotFrontage'].median()
    
    # 戻り値を列に直接代入することで、FutureWarningを完全に回避します
    df_all['LotFrontage'] = df_all['LotFrontage'].fillna(median_all)
    
print("LotFrontageの欠損値処理が完了しました。")


# 最頻値で補完（inplace=Trueを使わない）
df_all['Electrical'] = df_all['Electrical'].fillna(df_all['Electrical'].mode()[0])
df_all['MSZoning'] = df_all['MSZoning'].fillna(df_all['MSZoning'].mode()[0])


# ... 他の残りの少数欠損値も同様に処理

# 欠損値が残っているか再確認
print("\n--- 欠損値処理後の残存確認 ---")
print(df_all.isnull().sum().max()) # 最大値が0ならOK

# 欠損値が残っている列とその数を確認
missing_final = df_all.isnull().sum().sort_values(ascending=False)
missing_final = missing_final[missing_final > 0]

print("--- 欠損値処理後に残存している特徴量と数 ---")
print(missing_final.head(5))

# --- 提出用Idの分離 ---
# df_test の行数（1459行）に対応する Id を、元の df_test から抜き出します。
# df_test は読み込み直後でインデックスが0から始まっているので、
# df_test['Id'] をそのまま使って問題ありません。
test_id_submission = df_test['Id']
# ---------------------

# カテゴリカルな順序変数に数値を割り当てる
df_all['OverallQual'] = df_all['OverallQual'].astype(str) # 念のため文字列に変換

# 例: 外装材の品質 (ExterQual)
qual_map = {'Ex': 5, 'Gd': 4, 'TA': 3, 'Fa': 2, 'Po': 1, 'None': 0}
df_all['ExterQual'] = df_all['ExterQual'].replace(qual_map)
df_all['ExterCond'] = df_all['ExterCond'].replace(qual_map)

# 例: 地下室の品質 (BsmtQual)
bsmt_map = {'Ex': 5, 'Gd': 4, 'TA': 3, 'Fa': 2, 'Po': 1, 'None': 0}
df_all['BsmtQual'] = df_all['BsmtQual'].replace(bsmt_map)
df_all['BsmtCond'] = df_all['BsmtCond'].replace(bsmt_map)

# その他、順序を持つカテゴリ変数も同様に処理します（FireplaceQu, KitchenQual, GarageQual, GarageCond など）

# Id列を除外した全てのカテゴリ変数のリストを取得
categorical_cols = df_all.select_dtypes(include='object').columns

# ワンホットエンコーディングの実行
df_all = pd.get_dummies(df_all, columns=categorical_cols, dummy_na=False)

# 処理後のデータ形状を確認
print(f"\nワンホットエンコーディング後のデータ形状: {df_all.shape}")

# --- 特徴量エンジニアリングの追加 ---

# 1. 総面積 (TotalSF): 物件の主要な規模を示す強力な特徴量
# (地下室 + 1階 + 2階 の総面積)
df_all['TotalSF'] = df_all['TotalBsmtSF'] + df_all['1stFlrSF'] + df_all['2ndFlrSF']

# 2. 総浴槽数 (TotalBath): 浴室の総数（半風呂は0.5として計算）
df_all['TotalBath'] = (df_all['FullBath'] + (0.5 * df_all['HalfBath']) + 
                       df_all['BsmtFullBath'] + (0.5 * df_all['BsmtHalfBath']))

# 3. リフォーム後の経過年数 (YearsSinceRemodel)
df_all['YearsSinceRemodel'] = df_all['YrSold'] - df_all['YearRemodAdd']
# 負の値（未来の年）がある場合は0に修正（データエラー対策）
df_all.loc[df_all['YearsSinceRemodel'] < 0, 'YearsSinceRemodel'] = 0

# 4. 新築フラグ (IsNew): 売却年と建築年が同じなら1
df_all['IsNew'] = (df_all['YearBuilt'] == df_all['YrSold']).astype(int)

# -----------------------------------

#Step 13. outlier removal
# GrLivArea が 4000 sq ft を超える外れ値のインデックスを特定
# df_all は SalePrice_Log を含む全結合データフレームを使用します。
# GrLivArea が 4000 より大きく、かつ SalePrice_Log がNaNではない (訓練データである) 行を対象とします。

# 訓練データ部分のインデックスを取得
train_indices = df_all[df_all['SalePrice_Log'].notna()].index

# 訓練データの中で GrLivArea > 4000 の条件を満たす行を特定
outlier_indices = df_all.loc[train_indices][df_all.loc[train_indices]['GrLivArea'] > 4000].index

# 確認用: 該当する行の Id と GrLivArea を表示
print(f"特定された外れ値の数: {len(outlier_indices)}")
print("外れ値のインデックス:", outlier_indices.tolist())

# df_all からこれらの外れ値を削除
df_all = df_all.drop(outlier_indices)

# 1. 最終的なテストデータ X_test_final の再構築と Id の削除
# df_all は外れ値が削除された状態です。
# X_test_final には、df_all から SalePrice_Log が NaN の行（テストデータ）が含まれます。
X_test_final = df_all[df_all['SalePrice_Log'].isna()].drop('SalePrice_Log', axis=1).copy() # copy()で警告回避

# X_test_final に含まれる 'Id' 列を必ず削除します。
if 'Id' in X_test_final.columns:
    X_test_final = X_test_final.drop('Id', axis=1)

# 目的変数 (Logスケール) のフルシリーズを取得
y_train_full_new = df_all['SalePrice_Log']

# 学習データと目的変数に再分割
# Id列がまだ df_all に残っている場合は、この時点で削除します
if 'Id' in df_all.columns:
    df_all = df_all.drop('Id', axis=1)

# 外れ値削除後の学習データ
X_train_new = df_all[y_train_full_new.notna()].drop('SalePrice_Log', axis=1)
y_train_new = y_train_full_new.dropna()

print(f"X_train_new の列数: {X_train_new.shape[1]}")
print(f"X_test_final の列数: {X_test_final.shape[1]}")
# ここで列数が一致すればOKです (315列)

# 外れ値削除後のテストデータ
X_test_new = df_all[y_train_full_new.isna()].drop('SalePrice_Log', axis=1)

print(f"\n外れ値処理後の X_train 形状: {X_train_new.shape}")
print(f"外れ値処理後の X_test 形状: {X_test_new.shape}")


import xgboost as xgb
from sklearn.linear_model import Ridge
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint

# --- 最適なパラメータを使用 (前回の結果を流用) ---
# XGBoostの最適なパラメータを再設定
# 例: best_params = {'n_estimators': 784, 'learning_rate': 0.0354, 'max_depth': 4, ...}
# Ridgeの最適なαを再設定
# 例: best_alpha = 10.0 など
# --- 最適なパラメータを手動で定義 ---
# 前回のランダムサーチ結果をここにコピー＆ペースト
best_params = {
    'colsample_bytree': 0.7257423924305306,
    'learning_rate': 0.03542853455823514,
    'max_depth': 4,
    'n_estimators': 784,
    'reg_alpha': 0.025029222914887496,
    'reg_lambda': 1.4155743845534445,
    'subsample': 0.9022204554172195
}
# -----------------------------------

# 1. XGBoostの再学習
best_xgb_model_final = xgb.XGBRegressor(
    objective='reg:squarederror', 
    random_state=42, 
    n_jobs=-1,
    **best_params # ランダムサーチで見つけた最適なパラメータを直接渡します
)
print("XGBoost 再学習中...")
best_xgb_model_final.fit(X_train_new, y_train_new)

# --- 最適なαを手動で定義 ---
# 前回のRidge回帰グリッドサーチで見つけた最適なα値を代入
best_alpha = 2.4201 # ← あなたの環境での最適なα値に置き換えてください
# --------------------------
# # 2. Ridge回帰の再学習
best_ridge_model_final = Ridge(alpha=best_alpha, random_state=42)
print("Ridge回帰 再学習中...")
best_ridge_model_final.fit(X_train_new, y_train_new)

# 3. 予測の実行
xgb_predictions_log_final = best_xgb_model_final.predict(X_test_final)
ridge_predictions_log_final = best_ridge_model_final.predict(X_test_final)

# 4. ブレンディングの実行 (重みもそのまま流用)
weight_xgb = 0.7
weight_ridge = 0.3

blended_predictions_log_final = (weight_xgb * xgb_predictions_log_final) + \
                                (weight_ridge * ridge_predictions_log_final)

blended_predictions_price_final = np.expm1(blended_predictions_log_final)

import numpy as np

# 1. 要素数（長さ）の確認
expected_length = 1456
actual_length = len(blended_predictions_price_final)
print(f"✅ 予測結果の長さ: {actual_length}")

if actual_length == expected_length:
    print("   要素数は期待通り 1456 個です。")
else:
    print(f"   🚨 警告: 要素数が {expected_length} 個と一致しません。")
    
# 2. 数値内容の確認
# 配列内に NaN や無限大（Inf）が含まれていないかチェックします。

# blended_predictions_price_final を NumPy 配列として扱います
predictions_array = np.array(blended_predictions_price_final)

# NaN (Not a Number) が含まれていないか
has_nan = np.isnan(predictions_array).any()
# Inf (無限大) が含まれていないか
has_inf = np.isinf(predictions_array).any()

print(f"✅ NaNの有無: {has_nan}")
print(f"✅ Infの有無: {has_inf}")

if has_nan or has_inf:
    print("   🚨 エラー: 予測結果に NaN または Inf が含まれています。計算をやり直す必要があります。")
    
# 3. データの範囲と最初の数値をチェック
# 住宅価格として妥当な範囲か (例: 5万ドル以上)
min_val = predictions_array.min()
max_val = predictions_array.max()

print(f"✅ 最小予測価格: {min_val:.2f}")
print(f"✅ 最大予測価格: {max_val:.2f}")
print(f"✅ 最初の5つの予測値: {predictions_array[:5]}")

if min_val < 10000:
    print("   ⚠️ 警告: 予測値に異常に低い値が含まれている可能性があります。")


# 外れ値として削除されたのは訓練データのみであり、
# テストデータ（df_test）の行数は変わっていないはずですが、念のため確認します。

print(f"最終予測結果の長さ: {len(blended_predictions_price_final)}")
#print(f"最終提出用 Id の長さ: {len(final_test_id)}")

import pandas as pd
import numpy as np
# (test_id_submission_safe、blended_predictions_price_final、X_test_final は前のステップで定義済みとします)

# --- 提出ファイルの再構築（シンプルかつ確実な Id 結合） ---

# 1. X_test_final に含まれる Id を抽出 (1456行)
# X_test_final のインデックスを使って、元の df_test から Id を抽出します。
# ※ df_test がメモリに残っていることを前提とします。
current_id_for_prediction = df_test.loc[X_test_final.index, 'Id']

# 2. 予測値と対応する Id を持つデータフレーム (1456行) を作成
predictions_df = pd.DataFrame({
    'Id': current_id_for_prediction,
    'SalePrice': blended_predictions_price_final
})

# 3. 提出用データフレーム (1465行) を元の Id で初期化
final_submission = pd.DataFrame(test_id_submission_safe, columns=['Id'])

# 4. Id をキーにして予測結果を結合 (merge)
# 欠落した 9 行は NaN になります。
final_submission = pd.merge(
    final_submission, 
    predictions_df, 
    on='Id', 
    how='left'
)

# 5. NaN（欠落した9行）を平均値で補完
mean_price = final_submission['SalePrice'].mean()
final_submission['SalePrice'] = final_submission['SalePrice'].fillna(mean_price)

# 最終確認
print(f"最終提出ファイルの行数: {len(final_submission)}")
print(f"SalePriceのNaNの有無: {final_submission['SalePrice'].isnull().any()}") # False であるべき

# 提出ファイルをCSVとして保存
final_submission.to_csv('submission_final_merged.csv', index=False)

print("\n🎉 最終提出ファイル 'submission_final_merged.csv' が作成されました。再度提出をお願いします。")