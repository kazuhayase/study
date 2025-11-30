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

# 1. Neighborhoodごとの中央値で補完
df_all['LotFrontage'] = df_all.groupby('Neighborhood')['LotFrontage'].transform(
    lambda x: x.fillna(x.median())
)

# 2. それでも欠損値が残っている場合（警告の原因となったグループ）は、
#    全体のLotFrontageの中央値で補完する
if df_all['LotFrontage'].isnull().any():
    median_all = df_all['LotFrontage'].median()
    df_all['LotFrontage'].fillna(median_all, inplace=True) 

# 注: df_all['LotFrontage'].fillna(...) の形式なら SettingWithCopyWarning は出にくいです。
# 心配なら df_all.loc[:, 'LotFrontage'] = df_all['LotFrontage'].fillna(median_all) を使用。

# 最頻値で補完（inplace=Trueを使わない）
df_all['Electrical'] = df_all['Electrical'].fillna(df_all['Electrical'].mode()[0])
df_all['MSZoning'] = df_all['MSZoning'].fillna(df_all['MSZoning'].mode()[0])


# ... 他の残りの少数欠損値も同様に処理

# 欠損値が残っているか再確認
print("\n--- 欠損値処理後の残存確認 ---")
print(df_all.isnull().sum().max()) # 最大値が0ならOK

