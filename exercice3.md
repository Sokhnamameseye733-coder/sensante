# Exercice 3 : Réflexion sur les données de santé réelles

## Question
Le dataset contient 500 patients fictifs. Citez 3 difficultés qu'on pourrait rencontrer avec de vraies données de santé au Sénégal.

## Réponses

### 1. La qualité des données
Dans les centres de santé au Sénégal, beaucoup de dossiers sont encore sur papier. Les données peuvent être incomplètes, mal saisies ou manquantes 
(ex: température non mesurée, âge approximatif).

### 2. La vie privée des patients
Les données de santé sont très sensibles. Il faut respecter la confidentialité des patients et obtenir leur consentement avant d'utiliser leurs données pour entraîner un modèle ML.

### 3. La représentativité
Notre dataset a 30% de patients de Dakar. En réalité, les maladies varient selon les régions (ex: le paludisme est plus fréquent en zone rurale). Un modèle entraîné principalement sur Dakar pourrait mal fonctionner à Tambacounda ou Ziguinchor.