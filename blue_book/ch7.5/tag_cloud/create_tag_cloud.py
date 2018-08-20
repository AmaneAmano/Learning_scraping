import requests
from janome.tokenizer import Tokenizer
from bs4 import BeautifulSoup
from wordcloud import WordCloud

# Fetch html
url = "https://www.aozora.gr.jp/cards/000879/files/42_15228.html"
r = requests.get(url, timeout=10)

# Parse
soup = BeautifulSoup(r.content, 'lxml')

# Extract text
text_elm = soup.find('div', attrs={'class': 'main_text'})
# Remove kana element (ruby)
[e.extract() for e in text_elm.select('rt')]

# Get the text kana removed
text = text_elm.text

# Fetch Stop word
stop_word_url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/' \
                'Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
r_stopword = requests.get(stop_word_url, timeout=10)
stop_words = r_stopword.text.split()

# Split into words
t = Tokenizer()
words = []
for token in t.tokenize(text):
    if token.part_of_speech.split(',')[0] == '名詞' and token.surface not in stop_words:
        words.append(token.surface)

# Generate wordcloud object
font_path = r"C:\Users\agoot\Desktop\LightNovelPOP_FONT\lanobe_pop.otf"
wordcloud = WordCloud(background_color="white", font_path=font_path, regexp=r"\w+").generate(" ".join(words))

# Output graph
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

