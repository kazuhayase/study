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

print(f"特徴量追加後の X_train 形状: {X_train.shape}") 
# 列数が311から315程度に増えているはずです。

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

import pickle
import os
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint
import numpy as np
import xgboost as xgb

# ファイルが存在するかチェック
if os.path.exists('best_xgb_model.pkl'):
    with open('best_xgb_model.pkl', 'rb') as f:
        best_model = pickle.load(f)
        
    print("学習済みモデルをロードしました。再学習はスキップします。")
    # ロードしたモデルを使って予測に進む
    #predictions_log = best_model.predict(X_test)
else:
    # ファイルが存在しない場合（初回実行時のみ）、学習処理を実行する
    print("モデルファイルが存在しません。学習を開始します。")
    
    # モデルインスタンスの再作成
    model_tune = xgb.XGBRegressor(
        objective='reg:squarederror', 
        random_state=42, 
        # n_jobs=-1 でCPUの全コアを使用
        n_jobs=-1
    )

    # 調整するパラメータの範囲を定義
    # L1/L2正則化と学習率を重点的に調整し、過学習を防ぎます。
    param_dist = {
        'n_estimators': randint(300, 1500),         # 決定木の数 (多くする)
        'learning_rate': uniform(0.01, 0.05),       # 学習率 (低くする: 0.01-0.06の範囲)
        'max_depth': randint(3, 6),                 # 木の深さ (浅く保つ: 3-5が目安)
        'subsample': uniform(0.6, 0.4),             # サンプリング率
        'colsample_bytree': uniform(0.6, 0.4),      # 特徴量のサンプリング率
        'reg_alpha': uniform(0.0001, 0.1),          # L1正則化 (過学習抑制に重要)
        'reg_lambda': uniform(0.8, 1.5)             # L2正則化
    }

    # ランダムサーチの設定 (50回の試行)
    random_search = RandomizedSearchCV(
        estimator=model_tune, 
        param_distributions=param_dist, 
        n_iter=50, # 試行回数。時間があれば100以上に増やします。
        scoring='neg_mean_squared_error', # RMSLEの最適化に相当
        cv=5,                             # 5分割交差検証
        verbose=1, 
        random_state=42, 
        n_jobs=-1 
    )

    # チューニングの実行
    print("--- XGBoost ランダムサーチ チューニング開始 ---")
    random_search.fit(X_train, y_train)
    print("--- XGBoost ランダムサーチ チューニング完了 ---")

    # 最適パラメータとスコアの表示
    best_log_rmsle = np.sqrt(-random_search.best_score_)
    best_params = random_search.best_params_

    print(f"\n✨ 最適な交差検証 RMSLE (logスケール): {best_log_rmsle:.4f}")
    print("最適なパラメータ:")
    for k, v in best_params.items():
        print(f"  {k}: {v}")

    # 最適モデルの取得
    best_model = random_search.best_estimator_

    with open('best_xgb_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
        
    print("学習済みXGBoostモデルを 'best_xgb_model.pkl' に保存しました。")

# 最適モデルでの予測
predictions_log_tuned = best_model.predict(X_test)

# 元の価格スケールに戻す
predictions_price_tuned = np.expm1(predictions_log_tuned)

# 提出ファイルの作成
# Id列は、前回のステップで保存した test_id_submission を使用
# （Id列を取得したコードが直前にあることを確認してください）
submission_df_tuned = pd.DataFrame({
    'Id': test_id_submission,
    # 予測結果は Id の行数に合わせて使用
    'SalePrice': predictions_price_tuned[:len(test_id_submission)]
})

# 提出ファイルをCSVとして保存
#submission_df_tuned.to_csv('submission_xgb_tuned.csv', index=False)

#print("\n🎉 チューニング後の提出ファイル 'submission_xgb_tuned.csv' が作成されました。")

from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
import numpy as np

# ファイルが存在するかチェック
if os.path.exists('best_ridge_model.pkl'):
    with open('best_ridge_model.pkl', 'rb') as f:
        best_ridge_model = pickle.load(f)
        
    print("学習済みridgeモデルをロードしました。再学習はスキップします。")
    
else:
    print("Ridgeモデルファイルが存在しません。学習を開始します。")
    # Ridgeモデルのインスタンス化
    ridge = Ridge(random_state=42)

    # 調整するαの範囲を定義 (0.01から50.0まで、対数スケールで探索)
    param_grid = {'alpha': np.logspace(-2, 2, 100)} 
    # np.logspace(-2, 2, 100) は、0.01から100.0までの間に100個の値を生成します

    # グリッドサーチの設定
    grid_search_ridge = GridSearchCV(
        estimator=ridge,
        param_grid=param_grid,
        scoring='neg_mean_squared_error',
        cv=5,
        verbose=0,
        n_jobs=-1
    )

    # チューニングの実行
    print("--- Ridge回帰 グリッドサーチ チューニング開始 ---")
    grid_search_ridge.fit(X_train, y_train)
    print("--- Ridge回帰 グリッドサーチ チューニング完了 ---")

    # 最適パラメータとスコアの表示
    best_log_rmsle_ridge = np.sqrt(-grid_search_ridge.best_score_)
    best_alpha = grid_search_ridge.best_params_['alpha']

    print(f"\n✨ Ridge回帰の最適交差検証 RMSLE (logスケール): {best_log_rmsle_ridge:.4f}")
    print(f"最適なα: {best_alpha:.4f}")

    # 最適なRidgeモデルの保存
    best_ridge_model = grid_search_ridge.best_estimator_ # チューニングで得られた最適なRidgeモデル

    with open('best_ridge_model.pkl', 'wb') as f:
        pickle.dump(best_ridge_model, f)
        
    print("学習済みRidgeモデルを 'best_ridge_model.pkl' に保存しました。")

# Ridge回帰による予測 (対数スケール)
ridge_predictions_log = best_ridge_model.predict(X_test)


# 最適なXGBoostモデル (best_model) の予測（前回のステップで計算済み）
# predictions_log_tuned を使用

# 統合の重みを設定
# XGBoost: 0.7、Ridge: 0.3 とします
weight_xgb = 0.7
weight_ridge = 0.3

# 統合された予測 (対数スケール)
blended_predictions_log = (weight_xgb * predictions_log_tuned) + \
                          (weight_ridge * ridge_predictions_log)

# 元の価格スケールに戻す
blended_predictions_price = np.expm1(blended_predictions_log)

# 提出ファイルの作成
submission_df_blended = pd.DataFrame({
    'Id': test_id_submission, # 前回のステップで保存した Id を使用
    'SalePrice': blended_predictions_price[:len(test_id_submission)]
})

# 提出ファイルをCSVとして保存
submission_df_blended.to_csv('submission_xgb_ridge_blended.csv', index=False)

print("\n🎉 アンサンブル後の提出ファイル 'submission_xgb_ridge_blended.csv' が作成されました。")