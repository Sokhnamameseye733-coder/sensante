# Exercice 3 - Réflexion UX : SénSanté pour Kolda (3G + petit écran)

## Contexte
Un agent de santé à Kolda dispose d'une connexion 3G limitée 
et d'un téléphone avec un petit écran.

## 3 améliorations UX proposées

### 1. Réduire le poids de la page
Remplacer le CDN Tailwind (fichier très lourd) par une version 
compilée contenant uniquement les classes utilisées dans l'application.
Cela réduit considérablement le temps de chargement en 3G.

### 2. Mode hors-ligne
Sauvegarder le dernier diagnostic dans la mémoire locale du téléphone 
(localStorage) pour pouvoir le consulter même sans connexion internet.
Utile dans les zones à couverture instable comme Kolda.

### 3. Interface simplifiée sur mobile
- Agrandir les boutons et les champs pour faciliter la saisie 
  sur petit écran avec les doigts
- Afficher uniquement les champs essentiels au départ
- Utiliser des icônes à la place des textes longs pour gagner de l'espace