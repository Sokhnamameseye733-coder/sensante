"""
SenSante - Entrainement et serialisation du modele
Lab 2 : Entrainer et Serialiser un Modele
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import os

# ===== ETAPE 1 : CHARGER LES DONNEES =====
print("=" * 50)
print("SENSANTE - Entrainement du modele")
print("=" * 50)

df = pd.read_csv("data/patients_dakar.csv")
print(f"\nDataset : {df.shape[0]} patients, {df.shape[1]} colonnes")
print(f"\nDiagnostics :\n{df['diagnostic'].value_counts()}")

# ===== ETAPE 2 : PREPARER LES FEATURES =====
le_sexe = LabelEncoder()
le_region = LabelEncoder()

df['sexe_encoded'] = le_sexe.fit_transform(df['sexe'])
df['region_encoded'] = le_region.fit_transform(df['region'])

feature_cols = ['age', 'sexe_encoded', 'temperature', 'tension_sys',
                'toux', 'fatigue', 'maux_tete', 'region_encoded']

X = df[feature_cols]
y = df['diagnostic']

print(f"\nFeatures : {X.shape}")
print(f"Cible : {y.shape}")

# ===== ETAPE 3 : SEPARER TRAIN / TEST =====
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"\nEntrainement : {X_train.shape[0]} patients")
print(f"Test : {X_test.shape[0]} patients")

# ===== ETAPE 4 : ENTRAINER LE MODELE =====
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)
print(f"\nModele entraine !")
print(f"Nombre d'arbres : {model.n_estimators}")
print(f"Classes : {list(model.classes_)}")

# ===== ETAPE 5 : EVALUER LE MODELE =====
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy : {accuracy:.2%}")

cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
print("\nMatrice de confusion :")
print(cm)

print("\nRapport de classification :")
print(classification_report(y_test, y_pred))

# ===== ETAPE 6 : SERIALISER LE MODELE =====
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/model.pkl")
joblib.dump(le_sexe, "models/encoder_sexe.pkl")
joblib.dump(le_region, "models/encoder_region.pkl")
joblib.dump(feature_cols, "models/feature_cols.pkl")

size = os.path.getsize("models/model.pkl")
print(f"\nModele sauvegarde : models/model.pkl")
print(f"Taille : {size/1024:.1f} Ko")

# ===== ETAPE 7 : TESTER LE MODELE SERIALISE =====
model_loaded = joblib.load("models/model.pkl")
le_sexe_loaded = joblib.load("models/encoder_sexe.pkl")
le_region_loaded = joblib.load("models/encoder_region.pkl")

nouveau_patient = {
    'age': 28,
    'sexe': 'F',
    'temperature': 39.5,
    'tension_sys': 110,
    'toux': True,
    'fatigue': True,
    'maux_tete': True,
    'region': 'Dakar'
}

sexe_enc = le_sexe_loaded.transform([nouveau_patient['sexe']])[0]
region_enc = le_region_loaded.transform([nouveau_patient['region']])[0]

features = [
    nouveau_patient['age'],
    sexe_enc,
    nouveau_patient['temperature'],
    nouveau_patient['tension_sys'],
    int(nouveau_patient['toux']),
    int(nouveau_patient['fatigue']),
    int(nouveau_patient['maux_tete']),
    region_enc
]

features_df = pd.DataFrame([features], columns=feature_cols)
diagnostic = model_loaded.predict(features_df)[0]
probas = model_loaded.predict_proba(features_df)[0]
proba_max = probas.max()

print(f"\n--- Resultat du pre-diagnostic ---")
print(f"Patient : {nouveau_patient['sexe']}, {nouveau_patient['age']} ans")
print(f"Diagnostic : {diagnostic}")
print(f"Probabilite : {proba_max:.1%}")
print(f"\nProbabilites par classe :")
for classe, proba in zip(model_loaded.classes_, probas):
    bar = '#' * int(proba * 30)
    print(f"  {classe:8s} : {proba:.1%} {bar}")

# ===== EXERCICE 1 : IMPORTANCE DES FEATURES =====
print(f"\n--- Importance des features ---")
importances = model.feature_importances_
for name, imp in sorted(zip(feature_cols, importances),
                        key=lambda x: x[1], reverse=True):
    bar = '#' * int(imp * 50)
    print(f"  {name:20s} : {imp:.3f} {bar}")

# ===== EXERCICE 2 : TESTER 3 PATIENTS =====
print(f"\n--- Exercice 2 : Test de 3 patients fictifs ---")

patients_test = [
    {'age': 8,  'sexe': 'M', 'temperature': 36.6, 'tension_sys': 10, 'toux': 0, 'fatigue': 0, 'maux_tete': 0, 'region': 'Dakar'},
    {'age': 35, 'sexe': 'F', 'temperature': 40.2, 'tension_sys': 13, 'toux': 1, 'fatigue': 1, 'maux_tete': 1, 'region': 'Tambacounda'},
    {'age': 72, 'sexe': 'M', 'temperature': 38.1, 'tension_sys': 15, 'toux': 1, 'fatigue': 1, 'maux_tete': 0, 'region': 'Ziguinchor'},
]

descriptions = [
    "Enfant 8 ans sans symptomes",
    "Adulte 35 ans forte fievre",
    "Age 72 ans avec toux",
]

for patient, desc in zip(patients_test, descriptions):
    sexe_enc = le_sexe.transform([patient['sexe']])[0]
    region_enc = le_region.transform([patient['region']])[0]
    f = [patient['age'], sexe_enc, patient['temperature'],
         patient['tension_sys'], patient['toux'],
         patient['fatigue'], patient['maux_tete'], region_enc]
    features_df = pd.DataFrame([f], columns=feature_cols)
    diag = model_loaded.predict(features_df)[0]
    proba = model_loaded.predict_proba(features_df)[0].max()
    print(f"  {desc:35s} => {diag:10s} ({proba:.1%})")

print(f"\n{'=' * 50}")
print("Modele entraine, evalue et serialise avec succes !")
print(f"{'=' * 50}")