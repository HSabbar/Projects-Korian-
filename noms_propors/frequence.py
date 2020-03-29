from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import re

pattern = r"|=|\+|\*|`|\'|\[|]|\)|\(|,|\"|\.|:|;|-|\?|ù|%|«|»|\^|¨|/|&|@|#|§|°|\$|£|~|=|<|>|\t"
patternum = r"([a-zA-Z]+)([0-9]+)"
patternlen3 = r"\b\w{1,3}\b"
temp = r"([a-zA-Z]+)([0-9]+)"
# patternmm = r"|pour|avoir|elle|dans|avec|"

file = open('data/_57793TransmissionsSurvivors_2014V1.txt', 'r')
book = file.read()

textes = re.sub(pattern, '', str(book))
textes = re.sub(patternum, '', str(textes))
textes = re.sub(patternlen3, '', str(textes))
textes = re.sub(' +', ' ', textes) 
textes = re.sub(temp, '', textes) 
# textes = re.sub(patternmm, '', textes) 

# print(textes)
tokenized_word=word_tokenize(textes)
# print(tokenized_word)
fdist = FreqDist(tokenized_word)
figure(num=None, figsize=(15, 10), dpi=60, facecolor='w', edgecolor='k')

# histo = fdist.most_common(50)
# print(histo)

fdist.plot(50,cumulative=False)

plt.show()
