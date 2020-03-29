# Analyse-survivant

## Contexte : 
Nous avons sélectionnés toutes les transmissions de 6 dernière semaines de 2014.

## Objectif : 
L’objectif de ce travaille est de classifier les transmissions est ce que c'est positive, négative ou neutre, ce travaille nous pensons qui peut-être utile pour :
* Avoir un impact sur les survie. 
* Bien réfléchir comment nous pouvons améliorer la vie de nos résidents.
* Trouver des indices pour augmenter l’espérance de vie également.

## Méthode : 
Nous avons sélectionnés des résidents avec leur transmissions de 6 dernière semaines 2014.
Pour réaliser ce travaille nous avons utilisé les regex (les expression régulière) pour le pré-traitement de texte où nous avons nettoyé le texte, 
* Suppression des caractère spéciaux **`[.;:!=\%?,\"()\[\]]`**
* Suppression des balises html restant dans les transmissions.
* Suppression des espaces de trop.

Exemple clean texte : 
```
str = "trés aggressive lors des soins<span style=""text-decoration: underline; background-color: green;"">grande difficulté a la changé frappe++ crie"
new_str = trés aggressive lors des soins grande difficulté a la changé frappe crie 
```
La classification de sentiment nous avons  utilisé principalement la classe **NaiveBayesClassifier** dans le package [**textblob**](https://textblob.readthedocs.io/en/dev/) nous avons construit un petite dataset manuellement où nous avons ajouté la parti classe (label); il s’agit de classifier les transmissions (négative,  positive, neutre)

![alt text](https://github.com/HSabbar/Analyse-survivant/blob/master/dataset-analyse-sentiment.png)

Pour construir le modèle d’apprentissage, nous avons divisé le dataset en deux partis; la première pour la parti d’apprentissage, la deuxième pour la parti de teste.
À l'aide de la fonction NaiveBayesClassifier de package textblob elle permet d’apprendre à classifier 
```
X_train = [('je n’ai pas vu le pilulier', 'neg'),
            ('traitement non donné', 'neg'),
            ("selles", 'neg')]
train_data = [('il a mal a la dent', 'neg'),
              ('mme etait perturber', 'neg'),
              ('fait sa toilette seule', 'pos')]

classifier = NaiveBayesClassifier(X_train) 
print(classifier.accuracy(test_data))
0.6785714285714286
```
Résultats :

Nous avons construit les résultats dans csv :

![alt text](https://github.com/HSabbar/Analyse-survivant/blob/master/re%CC%81sultats.png)

