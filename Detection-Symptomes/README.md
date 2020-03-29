# Detection-Symptomes-

## Contexte : 
Les données extrait à partir de base de données de NetSoins : entre 30/12/2019 et 03/02/2020 (NetSoins-TRANSMISSIONS-APP).
Nous avons construit le jeu de données en utilisant les opérateurs logiques et les regex (les expressions régulières) en particulier le pattern matching LIKE et NOT LIKE  avec des groupes de mots spécifique qui décrit les symptômes.
[référence à documentation](https://www.postgresql.org/docs/9.5/functions-matching.html)

## Objectif : 
L’objectif de ce travail est de prédire des symptômes potentiels sur les transmissions NetSoins, nous pensons que ce travail peut-être utile pour :
* Prendre des mesures de sécurité avant la maladie. 
* Détecter rapidement des incidents (chutes fréquentes, grippe …)
* Améliorer la vie de nos résidents.
* Augmenter l’espérance de vie.

## Méthode : 

### Pre-Processing : 
Pour réaliser ce travail nous avons utilisé les regex (les expressions régulières) pour le nettoyer du texte :
* Suppression des caractères spéciaux **`['.;:!*=\%?,<>\"()\[\]]`**
* Suppression des balises html restantes dans les transmissions.
* Suppression des espaces en trop.
*la suppression des stopwords, Ce sont les mots très courants dans la langue étudiée ("et", "à", "le"...) qui n'apportent pas de valeur informative pour la compréhension du sens d'un document et corpus. Il sont très fréquents et ralentissent notre travail.
* Transformer les chiffres numérique en alphabet
* Suppression des lines qui n'a importe pas d'informations (erreur ou suite)

#### Exemple de clean texte : 
```
str = "23/02/2018 à 14:30 trés aggressive lors des soins<span style=""text-decoration: underline; background-color: green;"">grande difficulté a la changé frappe++ crie 1992é2323"
new_str = vingt-trois deux deux mille dix-huit quatorze trente trés aggressive lors soins grande difficulté changé frappe plus plus crie mille neuf cent quatre-vingt-douze deux mille trois cent vingt-trois
```
### Normaliser les données :
Normaliser le texte signifie le convertir en un format standard plus pratique avant de le transformer en fonctionnalités pour des algorithmes d’apprentissage. cette étape est considéré comme la conversion d'un langage humain en une forme lisible par la machine.
Un [tokenizer](https://keras.io/preprocessing/text/) sépare le texte en une liste de séquence de mot, qui correspondent à des mots, puis on transforme grâce la fonctionne [`pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)`](https://keras.io/preprocessing/sequence/) les listes des mots en tableaux de formes Numpy avec les mêmes longueurs

### Train test split : 

les données que nous utilisons sont généralement divisées en données d’apprentissage et données de test. L’ensemble d'apprentissage contient une sortie connue et le modèle apprend sur ces données afin d'être généralisé à d'autres données ultérieurement. Nous avons le sous-ensemble des données de test afin de tester la prédiction de notre modèle sur ce sous-ensemble.

### Créer le modèle :

```
MAX_NB_WORDS = 50000 # Le nombre maximum de mots à utiliser.
EMBEDDING_DIM = 100  # int >= 0: Dimension de Embedding dense.

model = Sequential()
model.add(Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=X_train.shape[1]))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(60, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(2, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
embedding_2 (Embedding)      (None, 512, 200)          10000000  
_________________________________________________________________
spatial_dropout1d_2 (Spatial (None, 512, 200)          0         
_________________________________________________________________
lstm_2 (LSTM)                (None, 60)                62640     
_________________________________________________________________
dense_2 (Dense)              (None, 2)                 122       
=================================================================
Total params: 10,062,762
Trainable params: 10,062,762
Non-trainable params: 0
_________________________________________________________________
None
```

* La première couche est le [`Embedding`](https://keras.io/layers/embeddings/) initialise d'abord le vecteur de embedding au hasard, puis utilise l'optimiseur de réseau pour le mettre à jour de la même manière que pour toute autre couche réseau en **keras**. cette couche utilise `MAX_NB_WORDS = 100` vecteurs de longueur pour représenter chaque mot, Le `MAX_NB_WORDS = 50000` représente la taille de notre vocabulaire, [`input_length=X_train.shape[1]`](https://keras.io/layers/core/) détermine la taille de chaque séquence d'entrée.
* SpatialDropout1D effectue le Dropout variationnel dans les modèles PNL, l'avantage d'ajouter SpatialDropout par rapport au dropout des keras normaux, dans le SpatialDropout  des canaux embedding complets sont supprimés tandis que le ropout embedding Keras normal supprime tous les canaux pour des mots entiers, et parfois perdre un ou plusieurs mots peut corrompre complètement la signification. ([`keras.layers.SpatialDropout1D(rate)`](https://keras.io/layers/core/) :  **`Dropout`** : consiste à définir au hasard une fraction `rate`  d'unités d'entrée à 0 à chaque mise à jour pendant le temps de formation, ce qui permet d'éviter un surapprentissage.) 
* La couche suivante est la couche LSTM avec 60 unités de mémoire.
* La couche de sortie doit créer 7 valeurs de sortie, une pour chaque classe.
* La fonction d'activation est `softmax` pour la classification multi-classes.
* Parce qu'il s'agit d'un problème de classification multi-classes, `categorical_crossentropy` est utilisé comme fonction de loss.

## Résultat

### Résultat d'apprentissage : 

#### Loss 
![alt text](https://github.com/HSabbar/Detection-Symptomes-/blob/master/images/Loss-de-sympto%CC%82mes-.png)
#### Accuracy 
![alt text](https://github.com/HSabbar/Detection-Symptomes-/blob/master/images/Accuracy-de-sympto%CC%82mes-.png)

### Tester avec des nouvelles transmissions

```
new_transmissions = ["BILAN BIO DEMANDÉ INFECTIEUX , SERO GRIPPALEGAÏACS SUR SELLES , SUSPICION D'UN SYNDROME \
                NÉOPLASIQUEKINÉ RESPIRATOIRE", 
                 "SUITE CONSULTATION : D'APÈS SON ACCOMPAGNATEUR : PAS DE PB PNEUMO, PAS DE VISITE \
                 À REPROGRAMMER. DEMANDE DE ME DENIS POUR ARRET DU DIURÉTIQUE, PNEUMOLOGUE PAS CONTRE \
                 À PRIORI MAIS ABSENCE DE COMPTE RENDU. DEMANDE DE CONSULTATION FAITE AVEC LE DR FROMONT,\
                 VIENDRA DEMAIN OU VENDREDI.",
                "ETAT GÉNÉRAL OKTOUSSE PEU, NON ENCOMBRÉTRAITEMENT TAMIFLU + ANTIBIOTIQUES DONNÉS HIER \
                ET AUJOURDH'UIAIMERAIT QU'ON LUI APPORTE LE JOURNAL LE MATIN CAR ÉTANT ISOLÉ IL NE PEUT \
                PAST°= 36.8°C À 10HINJECTION DE ZARZIO FAIT LE 11/02", 
                "GRIPPE A CONFIRMÉE, RESPIRATION SIFFLANTE REMARQUÉE AUJOURD'HUI PLUS QUE LES AUTRES JOURS", 
                "A DES APPAREILS AUDITIFS DES 2 COTÉS ET DES LUNETTESA SAVOIR : A ÉTÉ HOSPITALISÉE EN DÉCEMBRE\
                EN SERVICE DE RÉANIMATION POUR UNE PNEUMOPATHIE"]
for transmissions in new_transmissions :
    transmissions = [preprocess_clean(transmissions)]
    seq = tokenizer.texts_to_sequences(transmissions)
    padded = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH)
    pred = model.predict(padded)

    labels = ['GRIPPE_IRA', 'rien']
    print('pred : ', labels[np.argmax(pred)])

    
[out :]

pred :  rien
pred :  GRIPPE_IRA
pred :  GRIPPE_IRA
pred :  GRIPPE_IRA
pred :  GRIPPE_IRA

```

## Conclusion

Vu les résultat de teste sur les nouvelles transmissions il détecte avec une note 4/5,  
