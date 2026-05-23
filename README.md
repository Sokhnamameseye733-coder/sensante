---
title: SenSante
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# SenSante

Assistant pré-diagnostic médical pour le Sénégal.

## Démo en ligne

https://sokhna-mame-seye-sensante.hf.space

## Description

SenSante utilise le Machine Learning pour aider au pré-diagnostic des maladies courantes
(paludisme, grippe, typhoïde) à partir des symptômes du patient. L'application combine
un modèle RandomForest avec une explication générée par un LLM (Llama 3 via Groq).

## Stack

- scikit-learn (modèle ML)
- FastAPI (API REST)
- Tailwind CSS (frontend responsive)
- Groq / Llama 3 (explication LLM)
- Docker (conteneurisation)

## Structure du projet

```
sensante/
├── Dockerfile          ← NOUVEAU (Lab 6)
├── .dockerignore       ← NOUVEAU (Lab 6)
├── requirements.txt
├── data/
│   └── patients_dakar.csv
├── models/
│   ├── model.pkl
│   ├── encoder_sexe.pkl
│   ├── encoder_region.pkl
│   └── feature_cols.pkl
├── api/
│   └── main.py         (modifié : sert le frontend)
├── frontend/
│   └── index.html      (URL modifiée)
└── notebooks/
```

## Lancer en local avec Docker

```bash
# Construire l'image
docker build -t sensante .

# Lancer le conteneur
docker run -p 8000:8000 -e GROQ_API_KEY=votre_cle sensante

# Ouvrir http://localhost:8000
```

## Historique des versions

| Tag  | Lab   | Contenu                              |
|------|-------|--------------------------------------|
| v0   | Lab 1 | Structure projet + Git + dataset     |
| v1   | Lab 2 | Modèle ML (RandomForest)             |
| v2   | Lab 3 | API FastAPI (/health + /predict)     |
| v3   | Lab 4 | Frontend Tailwind CSS (responsive)   |
| v4   | Lab 5 | LLM Groq (/explain + explication)    |
| v1.0 | Lab 6 | Docker + déploiement en ligne        |

## Auteur

Sokhna Mame Seye Mbacké MBOUP - L2 GLSI - ESP/UCAD - 2026

## Cours

Intégration de Modèles IA - Dr. El Hadji Bassirou TOURE
