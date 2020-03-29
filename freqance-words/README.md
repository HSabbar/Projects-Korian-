# Analyse words groups

## Contexte : 
Les groupes de mots ou expression extrait à partir de la base de données de l'analyse de sentiment 
Nous avons construit les groupes des mots en analysant humainement les transmissions.



## Objectif : 
L’objectif de ce travail est de pouvoir classifier des transmissions grâce aux groupes des mots significative, l’importance des groupes des mots c’est trouver un point fort entre les groupes.


## Méthode : 

### Pre-Processing : 
Pour réaliser ce travail nous avons utilisé les regex (les expressions régulières) pour le nettoyer du texte :
* Suppression des caractères spéciaux **`['.;:!*=\%?,<>\"()\[\]]`**
* Suppression des balises html restantes dans les transmissions.
* Suppression des espaces en trop.
*la suppression des stopwords, Ce sont les mots très courants dans la langue étudiée ("et", "à", "le"...) qui n'apportent pas de valeur informative pour la compréhension du sens d'un document et corpus. Il sont très fréquents et ralentissent notre travail.


### Normaliser les données :
Normaliser le texte signifie le convertir en un format standard plus pratique avant de le transformer en fonctionnalités pour des algorithmes d’apprentissage. cette étape est considéré comme la conversion d'un langage humain en une forme lisible par la machine.

### Train test split : 

les données que nous utilisons sont généralement divisées en données d’apprentissage et données de test. L’ensemble d'apprentissage contient une sortie connue et le modèle apprend sur ces données afin d'être généralisé à d'autres données ultérieurement. Nous avons le sous-ensemble des données de test afin de tester la prédiction de notre modèle sur ce sous-ensemble.

### Appliquer les algorithmes  :
## RandomForest 

# Accuracy : 0.7870370370370371

## NaiveBayes

# Accuracy : 0.7962962962962963


 
