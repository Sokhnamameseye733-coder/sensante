# Exercice 3 - Lab 2 : Réflexion sur l'accuracy du modèle

## Question
Le modèle a 76% d'accuracy. Dans un contexte médical réel, est-ce suffisant ?
Quels seraient les risques d'un faux diagnostic ?

## Réponse

Le modèle SénSanté obtient 76% d'accuracy sur les données de test. Dans un 
contexte médical réel, ce score est insuffisant. Un faux diagnostic peut avoir 
des conséquences graves : un patient atteint de paludisme diagnostiqué "sain" 
ne recevra pas de traitement et risque de développer des complications mortelles. 
À l'inverse, un faux positif entraîne des traitements inutiles et coûteux pour 
le patient. En médecine, on vise généralement une accuracy supérieure à 95%, 
avec une attention particulière au recall pour les maladies graves comme le 
paludisme — il vaut mieux sur-diagnostiquer que rater un cas réel. SénSanté 
doit donc être utilisé comme outil d'aide à la décision et non comme 
remplacement du médecin.