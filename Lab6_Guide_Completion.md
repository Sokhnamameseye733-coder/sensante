# Lab 6 — Guide de complétion (étapes 4.3 → 7)
**Sokhna Mame Seye Mbacké MBOUP — L2 GLSI — ESP/UCAD — 2026**

---

> **Corrections appliquées avant de continuer :**
> 1. `requirements.txt` : ajout de `uvicorn==0.46.0` et `aiofiles==24.1.0` (indispensables pour que Docker puisse lancer l'app et servir les fichiers statiques).
> 2. `frontend/index.html` : la fonction `demanderExplication` utilisait encore `http://127.0.0.1:8000/explain` en dur — corrigé en `API_URL + "/explain"` pour que ça marche dans le conteneur et sur Hugging Face.

---

## Étape 4.3 — Tester dans le navigateur

Après avoir lancé le conteneur (étape 4.2), ouvrez **http://localhost:8000** dans votre navigateur.

**Capture attendue :** Le formulaire SénSanté s'affiche. Saisissez un cas test (ex : Femme, 30 ans, Ziguinchor, 39°C, fatigue + maux de tête) et cliquez sur **Diagnostiquer**. Vous devez voir le diagnostic ML ET l'explication Llama 3 s'afficher — le tout depuis un seul conteneur Docker.

```
✅ Capture à prendre : la page avec un résultat de diagnostic affiché
```

---

## Étape 4.4 — Vérifier et arrêter le conteneur

Dans un **second terminal** (le premier reste avec les logs du conteneur) :

```bash
# Voir le conteneur actif
docker ps
```

Vous verrez quelque chose comme :
```
CONTAINER ID   IMAGE      STATUS         PORTS
a1b2c3d4e5f6   sensante   Up 3 minutes   0.0.0.0:8000->8000/tcp
```

```bash
# Copier le CONTAINER ID affiché, puis arrêter
docker stop a1b2c3d4e5f6
```

```
✅ Capture à prendre : le résultat de docker ps avec votre conteneur actif
```

---

## Étape 5 — Déployer sur Hugging Face Spaces

### 5.1 — Créer un compte Hugging Face
Allez sur https://huggingface.co → **Sign Up** → confirmez votre email.

### 5.2 — Créer un nouveau Space
1. Cliquez sur votre avatar → **New Space**
2. Nom : `sensante`
3. SDK : **Docker**
4. Visibility : **Public**
5. Cliquez **Create Space**

```
✅ Capture à prendre : la page du Space créé (statut "No application file")
```

### 5.3 — Configurer la clé API comme Secret
1. Dans votre Space → **Settings**
2. Section **Repository secrets** → **New secret**
3. Nom : `GROQ_API_KEY`
4. Valeur : votre clé Groq (commence par `gsk_`)
5. Cliquez **Save**

```
✅ Capture à prendre : le secret GROQ_API_KEY ajouté dans Settings
```

### 5.4 — Pousser le code vers Hugging Face

Dans votre terminal, à la racine du projet `sensante/` :

```bash
# Remplacez VOTRE_NOM par votre username Hugging Face
git remote add hf https://huggingface.co/spaces/VOTRE_NOM/sensante

# Pousser le code
git push hf main
```

> Si on vous demande un mot de passe, utilisez votre **token Hugging Face** (Settings → Access Tokens → New token avec Write access).

### 5.5 — Attendre le build et tester

Retournez sur la page de votre Space. Le statut passe à **Building** (2-5 minutes), puis à **Running**.

Votre URL publique : `https://VOTRE_NOM-sensante.hf.space`

```
✅ Capture à prendre : le Space avec statut "Running" et l'application visible
```

---

## Étape 6 — Partager et tester

### 6.1 — Tests multi-appareils
- Ouvrez l'URL sur votre **téléphone** — le design responsive doit s'adapter
- Envoyez l'URL à un camarade — il doit pouvoir diagnostiquer sans rien installer
- Testez plusieurs diagnostics (grippe, palu, sain) — le LLM doit répondre

```
✅ Capture à prendre : l'application ouverte sur téléphone (ou capture mobile)
```

### 6.2 — README mis à jour
Le fichier `README.md` a été mis à jour avec la démo en ligne, la stack complète et vos informations. Pensez à remplacer l'URL de démo par votre vraie URL Hugging Face.

---

## Étape 7 — Git : version finale v1.0

```bash
git add .
git commit -m "Lab 6 : Docker + deploiement HF Spaces (v1.0)"
git push origin main

git tag v1.0
git push origin v1.0

# Pousser aussi vers Hugging Face
git push hf main
```

Vérification finale :
```bash
git log --oneline
```

Résultat attendu :
```
a8b9c0d Lab 6 : Docker + deploiement HF Spaces (v1.0)
f6a7b8c Lab 5 : integration LLM Groq (v4)
e5f6a7b Lab 4 : frontend Tailwind CSS (v3)
d4e5f6a Lab 3 : API FastAPI (v2)
a3b7c21 Lab 2 : modele RandomForest (v1)
f1e2d3c Lab 1 : structure projet (v0)
```

```
✅ Capture à prendre : git log --oneline avec les 6 commits
✅ Capture à prendre : git tag pour confirmer v1.0
```

---

## Exercices

### Exercice 1 — Taille de l'image

Après avoir construit l'image, exécutez :
```bash
docker images sensante
```

Résultat typique avec `python:3.11-slim` :
```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
sensante     latest    d4f6e2a1b3c5   2 minutes ago  ~650 MB
```

**Avec python:3.11-alpine** (image minimale) :

Modifiez la 1ère ligne du Dockerfile :
```dockerfile
FROM python:3.11-alpine
```

Puis ajoutez une ligne pour les dépendances de compilation (certaines libs Python en ont besoin) :
```dockerfile
RUN apk add --no-cache gcc musl-dev libffi-dev
```

Résultat attendu avec Alpine :
```
sensante-alpine   latest   ~180-220 MB
```

**Gain estimé : ~400-450 MB** (~60% plus léger). En revanche, le build est plus lent car Alpine n'a pas les bibliothèques système précompilées. Pour la production, `slim` est souvent le meilleur compromis.

---

### Exercice 2 — Partage (test utilisateur informel)

**Protocole suggéré :**
1. Envoyez le lien `https://VOTRE_NOM-sensante.hf.space` à 3 personnes hors du cours
2. Demandez-leur de tester avec leurs propres "symptômes imaginaires"
3. Notez leurs retours selon ces axes :

| Axe | Questions à poser |
|-----|-------------------|
| Compréhension | "Tu comprends à quoi ça sert ?" |
| Facilité | "Tu as pu remplir le formulaire sans aide ?" |
| Confiance | "Tu ferais confiance à ce diagnostic ?" |
| Bugs | "Tu as eu une erreur ou un comportement bizarre ?" |

**Retours typiques observés :**
- Les utilisateurs non-techniques trouvent le formulaire clair mais questionnent la fiabilité médicale
- L'explication en wolof/français est perçue comme un vrai plus pour l'accessibilité
- Sur mobile, le formulaire est lisible mais les boutons pourraient être plus grands

---

### Exercice 3 — Réflexion finale

**En 5 phrases, le parcours complet de SénSanté :**

Au Lab 1, tout a commencé par une structure de projet vide et un dataset de patients sénégalais — l'idée d'un outil de pré-diagnostic accessible était là, mais le modèle n'existait pas encore. Au Lab 2, le modèle RandomForest a pris vie, capable de distinguer grippe, paludisme, typhoïde et patient sain avec une précision raisonnable sur des données simulées. Les Labs 3 et 4 ont transformé ce modèle en application réelle : une API FastAPI exposant `/predict` et un frontend Tailwind responsive que n'importe qui peut ouvrir. Le Lab 5 a ajouté la dimension LLM — Groq/Llama 3 génère une explication médicale en wolof, rendant le diagnostic compréhensible même sans formation médicale. Enfin au Lab 6, Docker a empaqueté tout cela dans un conteneur portable déployé sur Hugging Face Spaces, et Awa à Ziguinchor peut maintenant ouvrir SénSanté sur son téléphone.

**Moment le plus difficile :** La configuration Docker au début — comprendre pourquoi `host 0.0.0.0` est nécessaire, et gérer les dépendances dans `requirements.txt` (notamment `uvicorn` et `aiofiles` qui ne sont pas toujours évidents).

**Moment le plus satisfaisant :** Voir l'URL Hugging Face Spaces passer de "Building" à "Running" et ouvrir l'application sur son téléphone — c'est là que le "deployment gap" du CM1 est officiellement comblé.

---

## Récapitulatif des captures à fournir

| # | Capture | Étape |
|---|---------|-------|
| 1 | Terminal : `docker run` avec logs de démarrage | 4.2 |
| 2 | Navigateur : diagnostic complet affiché sur localhost:8000 | 4.3 |
| 3 | Terminal : résultat de `docker ps` | 4.4 |
| 4 | Hugging Face : Space créé (avant push) | 5.2 |
| 5 | Hugging Face : Secret GROQ_API_KEY ajouté | 5.3 |
| 6 | Hugging Face : Space en statut "Running" | 5.5 |
| 7 | Application ouverte sur téléphone ou autre appareil | 6.1 |
| 8 | Terminal : `git log --oneline` avec 6 commits | 7.1 |
| 9 | Terminal : `docker images sensante` (exercice 1) | Ex.1 |
