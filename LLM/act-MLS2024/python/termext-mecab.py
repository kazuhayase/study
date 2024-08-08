from fugashi import Tagger
import re

#http://gensen.dl.itc.u-tokyo.ac.jp/pytermextract/
import termextract.mecab
import termextract.core
from pprint import pprint # このサンプルでの処理結果の整形表

# ファイルの読み込み
with open("/home/kazu/Books/Actuary-ebook/hoken1-ch1.txt", mode="r", encoding="utf-8") as f:
    nihon_orig = f.read()
# 不要な部分を削除
nihon = re.sub("（[^）]+）", "", nihon_orig)
nihon = re.sub("\[[^\]]+\]", "", nihon)
nihon = re.sub("[\n ]", "", nihon)

separator = "。"
nihon_list = nihon.split(separator)
nihon_list.pop()  # 最後の要素は空文字列なので削除
t = Tagger("-r/etc/mecabrc -Owakati")
#tokenized_documents = [' '.join(t.parse(doc).split()) for doc in nihon_list]
#node = t.parseToNodeList(str(nihon_list))
wakati_text = t.parse(str(nihon_list))
term_list = termextract.mecab.cmp_noun_list(wakati_text)
pprint(term_list)
