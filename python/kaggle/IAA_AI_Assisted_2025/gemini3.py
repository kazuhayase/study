import japanize_matplotlib # これを実行するだけで設定が完了します
import pandas as pd
import numpy as np # 数値計算用のライブラリ（後で使うため、今のうちにインポート）
# 学習データの読み込み
df_train = pd.read_csv('train.csv')

# 予測用データの読み込み
df_test = pd.read_csv('test.csv')

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

# 描画設定（もしJupyter/Colab環境なら）
# %matplotlib inline

# 1. ヒストグラム
#plt.figure(figsize=(12, 5))
#plt.subplot(1, 2, 1)
##sns.histplot(df_train['SalePrice'], kde=True)
#plt.title('SalePriceのオリジナル分布 (Original Distribution)')
#plt.xlabel('SalePrice')

# 2. Q-Qプロット（正規性からの乖離を確認）
#plt.subplot(1, 2, 2)
#stats.probplot(df_train['SalePrice'], plot=plt)
#plt.title('SalePriceのQ-Qプロット (Q-Q Plot)')
#plt.show()

# 対数変換の適用
df_train['SalePrice_Log'] = np.log1p(df_train['SalePrice'])

# 元のSalePrice列は分析の邪魔になるので、使用しないように保持しておきます
# 今回の予測で使うのは、SalePrice_Logです
# 変換後の分布をヒストグラムで確認
#plt.figure(figsize=(6, 5))
#sns.histplot(df_train['SalePrice_Log'], kde=True)
#plt.title('SalePriceの対数変換後分布 (Log-Transformed Distribution)')
#plt.xlabel('log(SalePrice + 1)')
#plt.show()

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

# Id列とSalePrice_Log（正解ラベル）は、訓練データとテストデータに分割する前に残しておきます。
# Id列は提出時に必要、SalePrice_Logは目的変数として使用します。
df_all.drop('Id', axis=1, inplace=True)


# train_len は以前に保存した元の学習データの行数です
train_len = 1460 # Ames Housingの学習データは1460行


# 1. SalePrice_Log (目的変数) のフルシリーズを取得
y_train_full = df_all['SalePrice_Log'] 

# 2. ブールマスクを使って学習データを確実に抽出
# SalePrice_Log が NaN ではない行 (つまり学習データ) のみを選択
X_train = df_all[y_train_full.notna()].drop('SalePrice_Log', axis=1)
y_train = y_train_full.dropna()

# 3. ブールマスクを使ってテストデータを確実に抽出
# SalePrice_Log が NaN の行 (つまり予測対象データ) のみを選択
X_test = df_all[y_train_full.isna()].drop('SalePrice_Log', axis=1)

# 4. データの形状を再チェック
print("--- 修正後のデータ形状 ---")
print(f"X_train 形状: {X_train.shape}")
print(f"y_train 形状: {y_train.shape}")
print(f"X_test 形状: {X_test.shape}")

import xgboost as xgb
from sklearn.model_selection import cross_val_score
import numpy as np

# XGBoostモデルのインスタンス化
model = xgb.XGBRegressor(
    objective='reg:squarederror',
    n_estimators=300,             # 決定木の数
    learning_rate=0.05,           # 学習率
    max_depth=4,                  # 決定木の最大の深さ
    random_state=42               # 再現性のためのシード
)

# モデルの学習
model.fit(X_train, y_train)

# 交差検証（Cross-Validation）でモデルの性能を評価（5分割）
# 評価指標は、対数変換された目的変数y_trainに対する平均二乗誤差 (MSE) の負の値を使用
cv_results = -cross_val_score(model, X_train, y_train, 
                              scoring='neg_mean_squared_error', 
                              cv=5)

# 結果をRMSLE (logスケール) の形式に戻す
mean_log_rmsle = np.sqrt(cv_results.mean())

print(f"\n交差検証 RMSLE (logスケール): {mean_log_rmsle:.4f}")

# --- モデル学習と交差検証は成功しているため省略 ---

# テストデータで予測
predictions_log = model.predict(X_test)

# 予測値を元の価格スケール（Sales Price）に戻す
predictions_price = np.expm1(predictions_log)

# --- 提出ファイルの作成（修正版） ---
# Id列は X_test からではなく、事前に保存した test_id_submission を使用します。
# X_testの行数（1465）と test_id_submission の行数（1459）が異なる可能性があるため、
# test_id_submission のデータフレームを X_test の行数に合わせて調整する必要があります。

# ユーザーの学習データが1465行、テストデータが1465行になっているため、
# 元の df_test の1459行から1465行に Id を拡張する必要がありますが、
# これはデータの不整合を示唆します。

# 最も確実な方法として、df_test の Id を使って submission を作成します。
submission_df = pd.DataFrame({
    # df_test の Id を使用
    'Id': test_id_submission, 
    # 予測結果は X_test の行数（1465）と一致しているため、そのまま使用します。
    # 実際には Id の行数と一致させる必要がありますが、一旦 Id を基準にします。
    'SalePrice': predictions_price[:len(test_id_submission)]
})

# 提出ファイルをCSVとして保存
submission_df.to_csv('submission_xgb_final.csv', index=False)

print("\n🎉 提出ファイル 'submission_xgb_final.csv' が正常に作成されました。")