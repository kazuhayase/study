#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <input_csv_file>"
  exit 1
fi

input_file=$1

# 1行目をヘッダとして取得
header=$(head -n 1 $input_file)
first_column_header=$(echo $header | awk -F, '{print $1}')

# インデックスを追加して標準出力に表示
{ echo "index,$first_column_header" && tail -n +2 $input_file | awk -F, '{print NR-1 "," $1}'; } 
