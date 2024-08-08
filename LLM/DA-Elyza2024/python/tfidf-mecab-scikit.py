#import MeCab
from fugashi import Tagger
import re
from sklearn.feature_extraction.text import TfidfVectorizer

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


# MeCabを使用してトークン化
#t = MeCab.Tagger("-r/etc/mecabrc -Owakati")

t = Tagger("-r/etc/mecabrc -Owakati")
tokenized_documents = [' '.join(t.parse(doc).split()) for doc in nihon_list]

# TF-IDFの計算
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(tokenized_documents)

# 各単語のTF-IDFスコアを取得
word_scores = {word: tfidf.getcol(idx).sum() for word, idx in vectorizer.vocabulary_.items()}

# スコアでソートして上位の単語を取得
sorted_word_scores = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)

for word, score in sorted_word_scores:
    print(f'単語: {word}, TF-IDFスコア: {score}')

    ###  termextract 
    ## http://gensen.dl.itc.u-tokyo.ac.jp/
