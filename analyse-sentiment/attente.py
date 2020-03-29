from nltk.stem.snowball import FrenchStemmer
import spacy
from spellchecker import SpellChecker

import numpy as np
from sklearn.model_selection import train_test_split

import nltk.data
from textblob import TextBlob
from textblob import Word
# spell = SpellChecker(language='fr')
# nlp = spacy.load('fr_core_news_sm')

path = "data/_57793TransmissionsSurvivors_2014V1.csv"
path_s = "data/sentiment.csv"
#split le cvs par id_resident

def block_id_resident(path, path_s):
	with open(path_s,  'w') as file_csv:
		with open(path, 'r') as csvfile:
			id_tmp = 166
			new_text = ''
			spamwriter = csv.writer(file_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow(['id_resident', 'descriptions'])
			for rows in  csv.reader(csvfile, delimiter=';'):
				if rows:
					id_resident = rows[0]
					descrip = rows[3] 
					new_text += preprocess_clean(descrip) + ', '

					if id_resident != str(id_tmp):
						spamwriter.writerow([id_tmp, new_text])
						new_text = ''

					id_tmp = id_resident


tokenizer = nltk.data.load('tokenizers/punkt/PY3/french.pickle')

text_blob_object = TextBlob(document)

document_words = text_blob_object.words


text_blob_object = TextBlob(document)
for ngram in text_blob_object.ngrams(2):
    print(ngram)

document = "je n'ai pas vu le pilulier,\
traitement non donné,\
j'ai retrouvé mr en train de pleurer ce soir il m'informe la mort de sa femme à l'hopital pompidou,\
dr traolen est contacté aujourd'hui pour renouveller le stilnox de mr prince il a faxé une ordonnance de stilnox pour un mois l'ordonnance est faxé à la pharmacie cet aprés midi,\
les filles lui ont donné le laxatif suppositoire,\
selles,\
remis à patricia fille de mprince ce jour les 25 € que salomé avait laissé dans le coffre,\
mr prince me qu'il a trés mal au dent il n'a pas mangé son plat a midi ide prévenue,\
monsieur n'ayant pas eu de selles pendant trois jours a eu un lavement par l'infirmier avant la toilette intime monsieur a fait des selles n2,\
absence de selle depuis plus de 3 jorus,\
lavement par normacol fait ce matin,\
le résident a eu des selles en fin de matinée selon les dires de la soingnantes,\
il dit qu'il a mal a la dent,\
mme etait perturber ce matin par rapport qu'on lui est voler de l'argent"


train_data = [
    ('je n\'ai pas vu le pilulier', 'neg'),
    ('traitement non donné', 'neg'),
    ('j\'ai retrouvé mr en train de pleurer ce soir il m\'informe la mort de sa femme à l\'hopital pompidou', 'neg'),
    ('les filles lui ont donné le laxatif suppositoire', 'neg'),
    ("selles", 'neg'),
    ('mr prince me qu\'il a trés mal au dent il n\'a pas mangé son plat a midi ide prévenue', 'neg'),
    ('absence de selle depuis plus de 3 jorus', 'neg'),
    ("le résident a eu des selles en fin de matinée selon les dires de la soingnantes", 'pos'),
    ('il a mal a la dent', 'neg'),
    ('mme etait perturber', 'neg'),
    ('fait sa toilette seule', 'pos'),
    ('mme etait mecontente car on lui a changer la taille de protection ', 'pos'),
    ('se sentir en sécurité face à son incontinence nocturneactions', 'pos'),
    ('eu son vaccin antigrippal', 'pos'),
    ('mme demartini va bien a passe une bonne journee', 'pos'), 
    ('fatigué il a du mal à se mouvoir je lui ai fait une toilette au lit', 'neg')
]


classifier = NaiveBayesClassifier(train_data)
print(classifier.accuracy(test_data))

print(classifier.classify("mme n'a pas eu ses selles"))
print(classifier.classify("mme a eu ses selles"))
print(classifier.classify("mme a pleuré"))
print(classifier.classify("mr a peur"))
stemmer = FrenchStemmer()
print(stemmer.stem('voudrais'))

doc = nlp(u"voudrais non animaux yeux dors couvre")
for token in doc:
    print(token, token.lemma_)

misspelled = ["traitementtes", "matinnée", "plonbier", "tecnicien"]
misspelled = spell.unknown(misspelled)
for word in misspelled:
	print(word, spell.correction(word))

for x in document.split(','):
	print(tokenizer.tokenize(x))



# def classify_sentiment(santence):
# 	for str in santence:
# 		print(str + ' : ', classifier.classify(str))



# str = ["Tousse beaucoup depuis hier.Fesses trés rouge ce matin, mis traitement",\
# "etait tremblant ce soirT° rectale :37.3dextro o,87presence de sa fillemasse fluctuante au niveau du genou gauche (douloureux)",\
# "Trés douloureux lors de la manipulation pour le change,souffre de son genou gauche.",\
# "mme accepte une toilette seule"
# ]


# classify_sentiment(str)



