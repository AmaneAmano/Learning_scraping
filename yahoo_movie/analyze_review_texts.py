import codecs
import json
import collections

import requests
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud

with codecs.open("./movie_reviews.json", "r", "utf-8") as f:
    reviews = json.load(f)

review_text_joined = "".join(reviews['reviews'].values()).replace("\n", "")

# Fetch Stop word
stop_word_url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/' \
                'Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
r_stopword = requests.get(stop_word_url, timeout=10)
stop_words = r_stopword.text.split()
stop_words += ["ポケモン", "映画", "の", "サトシ", "作品"]


t = Tokenizer()
words = []
for token in t.tokenize(review_text_joined):
    if token.part_of_speech.split(',')[0] == '名詞' and token.surface not in stop_words:
        words.append(token.surface)

c = collections.Counter(words)
print(c.most_common())