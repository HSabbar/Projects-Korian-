import numpy as np
import re
from nltk.tokenize import RegexpTokenizer


tokenizer = RegexpTokenizer(r"\w+|\$[\d\.]+|\S+\'")
file = open('T1815SDec2014AFAS0.txt', 'r', encoding="ISO-8859-1")
book = file.read()


pattern = r"|=|\+|\*|`|\'|\[|]|(|)|,|\.|:|\?|ù|%|«|»|\^|¨|/|&|@|#|§|°|\$|£|~|=|<|>|\t"


def tokenize():
    if book is not None:
        words = book.lower()
        return words
    else:
        return None

# ['mme', 'matin', 'dit', 'jour', 'car', 'fait', 'bien']

def count_word(tokens):
    count = []
    mots = []
    count_tmp = 1
    j = 0
    for element in tokens:
    	if mots is None :
    		mots.append(element)
    		count.append(count_tmp)
    		j = 0
    	for i, mot in enumerate(mots):
	    	if element == mots[i]:
	            # count_tmp += 1
	            count[i] +=1
	        else:
	        	mots.append(element)
	        	count[j] = 1
	        	j += 1
			

    return count, mots
    
    
# Tokenize the Book
words = tokenize()
textes = re.sub(pattern, '', str(words)).split()

Words, frequency = count_word(textes)

print(Words[0:10])
print(frequency[0:10])
# print(textes)
# Get Word Count

# word_shreash = ['mme', 'matin', 'dit', 'jour', 'car', 'fait', 'bien']
# for word in word_shreash:
# 	frequency = count_word(textes, word)
# 	print('Word: ' + word + ' Frequency: ' + str(frequency))



