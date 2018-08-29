from janome.tokenizer import Tokenizer

t = Tokenizer()
text = u"空けない闇の果て"
for token in t.tokenize(text):
   print(token.surface)