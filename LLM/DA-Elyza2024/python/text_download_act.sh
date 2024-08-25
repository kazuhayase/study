#!/bin/sh

url='https://www.actuaries.jp/examin/textbook/'
dir='./Downloads/actuaries-examin-textbook/'
python download_files.py  $url $dir
cd $dir

mkdir 'hoken1_seiho' 'hoken2_seiho' 'sonpo' 'nenkin' '1ji' 'GOMI'
mv *suuri*pdf 1ji/
mv *taihi*pdf GOMI
mv hoken1-seiho*.pdf hoken1_seiho/
mv hoken2-seiho*.pdf hoken2_seiho/
mv sonpo*pdf sonpo/
mv nenkin*.pdf nenkin/
mv *pdf 1ji/

cd ../..

python llama_mkvec_act2.py
