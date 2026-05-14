# Exercice 3 - Réflexion sur la concurrence FastAPI

## Question
Que se passe-t-il si deux personnes accèdent à /predict exactement en même temps ? L'API peut-elle gérer ça ?

## Réponse

FastAPI est basé sur **asyncio**, un système d'exécution asynchrone qui lui permet de gérer plusieurs requêtes simultanément sans les bloquer.

Concrètement, si Cheikh à Tambacounda et Fatou à Ziguinchor envoient leurs symptômes en même temps, uvicorn traite les deux requêtes en parallèle grâce à ses **workers**.

Cependant, comme notre modèle est chargé en mémoire une seule fois et que `model.predict()` est une opération synchrone (non-async), FastAPI la traite dans un thread séparé pour ne pas bloquer les autres requêtes — c'est le comportement par défaut pour les fonctions `def` dans FastAPI.