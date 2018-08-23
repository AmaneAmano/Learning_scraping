from janome.tokenizer import Tokenizer

t = Tokenizer()
text = u"最高の映画でした！とてもたのしかった！楽しかった！本当に！"
for token in t.tokenize(text):
    if token.part_of_speech.split(',')[0] == "形容詞":
        print(token.base_form)