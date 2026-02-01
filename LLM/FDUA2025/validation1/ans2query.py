import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('ans_txt.csv')  # 'input_file.csv'をあなたのファイル名に置き換えてください

# indexカラムを作成し、元のカラムを選択
df['index'] = range(len(df))
new_df = df[['index', 'problem']]

# 新しいCSVファイルとして保存する
new_df.to_csv('query.csv', index=False)
