#!/bin/bash

url='https://www.actuaries.jp/examin/textbook/'
dir_path='./Downloads/actuaries-examin-textbook/'

python ./download_files.py url dir_path

cd ./Downloads/actuaries-examin-textbook/

mkdir 'hoken1_seiho' 'hoken2_seiho' 'sonpo' 'nenkin' '1ji'
mv sonpo*pdf sonpo/
mv nenkin*.pdf nenkin/
mv hoken1-seiho*.pdf hoken1_seiho/
mv hoken2-seiho*.pdf hoken2_seiho/
mv *pdf 1ji/

cd ../..


#python llama_mkvec_act2.py

