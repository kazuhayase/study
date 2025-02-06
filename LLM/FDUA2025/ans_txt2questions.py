import pandas as pd
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_csv_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    # CSVファイルの読み込み（ヘッダ行を指定）
    df = pd.read_csv(input_file)

    # 1列目のみを抽出（列名を取得）
    column_name = df.columns[0]
    column1 = df[column_name]

    # インデックスを追加
    result = pd.DataFrame({'index': range(len(column1)), column_name: column1})

    # 結果を標準出力に表示（ヘッダを含む）
    print(result.to_csv(index=False))

if __name__ == "__main__":
    main()
