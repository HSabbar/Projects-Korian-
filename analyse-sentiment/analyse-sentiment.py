from textblob.classifiers import NaiveBayesClassifier
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

#classifier les transmissions survivant 2014 
def Classifier_sentiment(path):
	global classifier
	with open(path, 'r') as csvfile:
		train_data, X_train, test_data = [], [], []

		for _,_,_,descriptions, sentiments in  csv.reader(csvfile, delimiter=';'):
			if descriptions:
				descriptions = preprocess_clean(descriptions)#clean text 
				data_tmp = descriptions, sentiments 
				train_data.append(data_tmp)

		#split le dataset en train et test 
		r = .0 
		for i in train_data:
			if r <= 8.5:
				X_train.append(i)
			else:
				test_data.append(i)

			r += .1

		#classifier avec NaiveBayesClassifier de package textblob
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

str = '"trés aggressive lors des soins<span style=""text-decoration: underline; background-color: green;"">grande difficulté a la changé frappe++ crie"'

print(str)
print(preprocess_clean(str))
# Classifier_sentiment('data/TransmissionsSurvivors_2014V1.100-sentiments.csv')

# classifier_to_csv(path_init, path_new_sentiments)


