from textblob.classifiers import NaiveBayesClassifier
import nltk 
from nltk.stem.snowball import FrenchStemmer 
from nltk.corpus import stopwords 

from typing import Pattern

import csv
import re

path_init = "data/_57793TransmissionsSurvivors_2014V1.2.csv"
path_new_sentiments = "data/no-clean-text-sentiments.csv"

PATTERN_SUPP_HTML : Pattern = re.compile(r'<(.*?)>')
REPLACE_NO_SPACE : Pattern= re.compile(r"[.;:!=\%?,\"()\[\]]")
REPLACE_WITH_SPACE : Pattern = re.compile(r"(<br\s*/><br\s*/>)|(\-)|(\/)|°")

# nettoyer le texte 
def preprocess_clean(reviews):
	reviews = reviews.lower() # mettre le texte en minuscule

	reviews = re.sub(r'\bagrave\b', 'a', reviews) #replacer agrave par a (!à)
	reviews = re.sub(r'\beacut\b|\begrave\b|\bpreacute\b', 'e', reviews)#

	sub_html = re.findall(PATTERN_SUPP_HTML, reviews) #supprimer les balise html
	for html in sub_html:
		if html:
			reviews = re.sub(r'\s+', ' ', reviews)
			reviews = re.sub(r"\'", ' ', reviews)
			reviews = reviews.replace(html, '')
			reviews = reviews.replace('<>', ' ')

	reviews = REPLACE_NO_SPACE.sub(' ', reviews) #supprimer tout les caracteres [.;:!=\%?,\"()\[\]]
	reviews = REPLACE_WITH_SPACE.sub(' ', reviews) #supprimer espace entre balise html au cas où y'en a 
	reviews = reviews.replace('ttt', 'traitement') 
	# reviews = re.sub(r"([+])", ' plus ', reviews)
	reviews = re.sub(r"([+])", ' ', reviews)
	reviews = re.sub(r'[0-9]', '', reviews)

	reviews = re.sub(' +', ' ', reviews)#supprimer tout espace de plus qui peut exister à la fin de traitement

	return reviews


def get_stopswords(type="veronis"):
    '''Suppression des mots vides avec NLTK'''
    if type == "veronis":

        raw_stopword_list = ["Ap.", "Apr.", "GHz", "MHz", "USD", "a", "afin", "ah", "ai", "aie", "aient","aies", 
                             "ait", "alors", "après", "as", "attendu", "au", "au-delà", "au-devant","aucun", 
                             "aucune", "audit", "auprès", "auquel", "aura", "aurai", "auraient","aurais", 
                             "aurait", "auras", "aurez", "auriez", "aurions", "aurons", "auront", "aussi", 
                             "autour", "autre", "autres", "autrui", "aux", "auxdites", "auxdits", "auxquelles", 
                             "auxquels", "avaient", "avais", "avait", "avant", "avec", "avez", "aviez", 
                             "avions", "avons", "ayant", "ayez", "ayons", "b", "bah", "banco", "ben","bien", 
                             "bé", "c", "c'", "c'est", "c'était", "car", "ce", "ceci", "cela", "celle",
                             "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci",
                             "celui-là", "celà", "cent", "cents", "cependant", "certain", "certaine","certaines",
                             "certains", "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là","cf.", "cg", "cgr", 
                             "chacun", "chacune", "chaque", "chez", "ci", "cinq", "cinquante", "cinquante-cinq", 
                             "cinquante-deux", "cinquante-et-un","cinquante-huit", "cinquante-neuf", 
                             "cinquante-quatre", "cinquante-sept", "cinquante-six", "cinquante-trois", 
                             "cl", "cm", "cm²", "comme", "contre","d", "d'", "d'après", "d'un", "d'une", "dans", 
                             "de", "depuis", "derrière", "des", "desdites", "desdits", "desquelles", "desquels", 
                             "deux", "devant", "devers", "dg", "différentes", "différents", "divers", "diverses", "dix", 
                             "dix-huit", "dix-neuf", "dix-sept", "dl", "dm", "donc", "dont", "douze", "du", 
                             "dudit", "duquel", "durant", "dès", "déjà", "e", "eh", "elle", "elles","en", 
                             "en-dehors", "encore", "enfin", "entre", "envers", "es", "est", "et", "eu", "eue", 
                             "eues", "euh", "eurent", "eus", "eusse", "eussent", "eusses","eussiez", "eussions", 
                             "eut", "eux", "eûmes", "eût", "eûtes", "f", "fait", "fi", "flac", "fors", "furent", 
                             "fus", "fusse", "fussent", "fusses", "fussiez", "fussions", "fut", "fûmes", "fût", 
                             "fûtes", "g", "gr", "h", "ha", "han", "hein", "hem", "heu", "hg", "hl", "hm", "hm³", 
                             "holà", "hop", "hormis", "hors", "huit", "hum", "hé", "i", "ici", "il", "ils", "j", "j'", 
                             "j'ai", "j'avais", "j'étais","jamais", "je", "jusqu'", "jusqu'au", "jusqu'aux", "jusqu'à", 
                             "jusque", "k","kg", "km", "km²", "l", "l'", "l'autre", "l'on", "l'un", "l'une", "la", 
                             "laquelle", "le", "lequel", "les", "lesquelles", "lesquels", "leur", "leurs", "lez", 
                             "lors", "lorsqu'", "lorsque", "lui", "lès", "m", "m'", "ma", "maint", "mainte", 
                             "maintes", "maints", "mais", "malgré", "me", "mes", "mg", "mgr", "mil", "mille", 
                             "milliards", "millions", "ml", "mm", "mm²", "moi", "moins", "mon", "moyennant", "mt", 
                             "m²", "m³", "même", "mêmes", "n", "n'avait", "n'y", "ne", "neuf", "ni", "non", 
                             "nonante", "nonobstant", "nos", "notre", "nous", "nul", "nulle", "nº", "néanmoins", 
                             "o", "octante", "oh", "on", "ont", "onze", "or", "ou", "outre", "où", "p", "par", 
                             "par-delà", "parbleu", "parce", "parmi", "pas", "passé", "pendant", "personne", 
                             "peu", "plus", "plus_d'un", "plus_d'une", "plusieurs", "pour", "pourquoi", 
                             "pourtant", "pourvu", "près", "puisqu'", "puisque", "q", "qu", "qu'", "qu'elle",
                             "qu'elles", "qu'il", "qu'ils", "qu'on", "quand", "quant", "quarante", "quarante-cinq", 
                             "quarante-deux", "quarante-et-un", "quarante-huit", "quarante-neuf", "quarante-quatre", 
                             "quarante-sept", "quarante-six", "quarante-trois", "quatorze", "quatre", "quatre-vingt", 
                             "quatre-vingt-cinq", "quatre-vingt-deux", "quatre-vingt-dix", "quatre-vingt-dix-huit", 
                             "quatre-vingt-dix-neuf", "quatre-vingt-dix-sept", "quatre-vingt-douze", "quatre-vingt-huit", 
                             "quatre-vingt-neuf", "quatre-vingt-onze", "quatre-vingt-quatorze", "quatre-vingt-quatre", 
                             "quatre-vingt-quinze", "quatre-vingt-seize", "quatre-vingt-sept", "quatre-vingt-six", 
                             "quatre-vingt-treize", "quatre-vingt-trois", "quatre-vingt-un", "quatre-vingt-une", 
                             "quatre-vingts", "que", "quel", "quelle", "quelles", "quelqu'", "quelqu'un", 
                             "quelqu'une", "quelque", "quelques", "quelques-unes", "quelques-uns", "quels",
                             "qui", "quiconque", "quinze", "quoi", "quoiqu'", "quoique", "r", "revoici", 
                             "revoilà", "rien", "s", "s'", "sa", "sans", "sauf", "se", "seize", "selon", 
                             "sept", "septante", "sera", "serai", "seraient", "serais", "serait", "seras",
                             "serez", "seriez", "serions", "serons", "seront", "ses", "si", "sinon", "six", 
                             "soi", "soient", "sois", "soit", "soixante", "soixante-cinq", "soixante-deux", 
                             "soixante-dix", "soixante-dix-huit", "soixante-dix-neuf", "soixante-dix-sept", 
                             "soixante-douze", "soixante-et-onze", "soixante-et-un", "soixante-et-une", 
                             "soixante-huit", "soixante-neuf", "soixante-quatorze", "soixante-quatre", 
                             "soixante-quinze", "soixante-seize", "soixante-sept", "soixante-six", 
                             "soixante-treize", "soixante-trois", "sommes", "son", "sont", "sous", 
                             "soyez", "soyons", "suis", "suite", "sur", "sus", "t", "t'", "ta", 
                             "tacatac", "tandis", "te", "tel", "telle", "telles", "tels", "tes", 
                             "toi", "ton", "toujours", "tous", "tout", "toute", "toutefois", 
                             "toutes", "treize", "trente", "trente-cinq", "trente-deux", "trente-et-un",
                             "trente-huit", "trente-neuf", "trente-quatre", "trente-sept", "trente-six",
                             "trente-trois", "trois", "très", "tu", "u", "un", "une", "unes", "uns", "v", 
                             "vers", "via", "vingt", "vingt-cinq", "vingt-deux", "vingt-huit", "vingt-neuf", 
                             "vingt-quatre", "vingt-sept", "vingt-six", "vingt-trois", "vis-à-vis", "voici", 
                             "voilà", "vos", "votre", "vous", "w", "x", "y", "z", "zéro", "à", "ç'", "ça", 
                             "ès", "étaient", "étais", "était", "étant", "étiez", "étions", "été", "étée", 
                             "étées", "étés", "êtes", "être", "ô"]
    else:
        raw_stopword_list = stopwords.words('french')
        
    stopword_list = [word for word in raw_stopword_list] 
    return stopword_list

def filter_stopwords(text, stopword_list):
    # print(text)
    words = [w for w in text.split()] 
    filtered_words = [] 
    # print(words)
    for word in words: 
        if word not in stopword_list and word.isalpha() and len(word) > 1: 
            filtered_words.append(word) 
    filtered_words#.sort() 
    return filtered_words
#classifier les transmissions survivant 2014 
def Classifier_sentiment(path):
    global classifier
    with open(path, 'r') as csvfile:
        train_data, X_train, test_data = [], [], []

        for _,_,_,descriptions, sentiments in  csv.reader(csvfile, delimiter=';'):
            if descriptions:
                descriptions = preprocess_clean(descriptions)#clean text 
                stopword_list = get_stopswords()
                filtered_word = filter_stopwords(descriptions, stopword_list)
                # print(filtered_word)
                descriptions = ' '.join(filtered_word)
                data_tmp = descriptions, sentiments
                print(descriptions) 
                train_data.append(data_tmp)

        #split le dataset en train et test 
        r = .0 
        for i in train_data:
            if r <= 8.5:
                X_train.append(i)
            else:
                test_data.append(i)

            r += .1

        print(X_train)
        # #classifier avec NaiveBayesClassifier de package textblob
        classifier = NaiveBayesClassifier(X_train)
        print(classifier.accuracy(test_data))

#Mettre les prédiction dans csv 
def classifier_to_csv(path, path_s):
	with open(path_s,  'w') as file_csv: # nouveau fichier csv avec les sentiment 	 
		with open(path, 'r') as csvfile: # csv à classifier
			spamwriter = csv.writer(file_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for rows in  csv.reader(csvfile, delimiter=';'):
				if rows:
					descriptions = rows[3]
					sentiment = classifier.classify(descriptions) # classifier descriptions
					spamwriter.writerow([rows[0], rows[1], rows[2], descriptions, sentiment])


Classifier_sentiment('data/TransmissionsSurvivors_2014V1.100-sentiments.csv')

# classifier_to_csv(path_init, path_new_sentiments)


