# api/main.py
# SenSante API - Assistant pre-diagnostic medical
# Lab 3 - Integration de Modeles IA - ESP/UCAD

from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import joblib
import numpy as np
import os
from dotenv import load_dotenv
from groq import Groq

# --- Schemas Pydantic ---
class PatientInput(BaseModel):
    age: int = Field(..., ge=0, le=120)
    sexe: str = Field(...)
    temperature: float = Field(..., ge=35.0, le=42.0)
    tension_sys: int = Field(..., ge=60, le=250)
    toux: bool = Field(...)
    fatigue: bool = Field(...)
    maux_tete: bool = Field(...)
    region: str = Field(...)

class DiagnosticOutput(BaseModel):
    diagnostic: str
    probabilite: float
    confiance: str
    message: str

class ExplainInput(BaseModel):
    diagnostic: str
    probabilite: float
    age: int
    sexe: str
    temperature: float
    region: str

class ExplainOutput(BaseModel):
    explication: str

# Charger la clé API
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- Application FastAPI ---
app = FastAPI(
    title="SenSante API",
    description="Assistant pre-diagnostic medical pour le Senegal",
    version="0.2.0"
)

# --- Chargement du modele (une seule fois) ---
print("Chargement du modele...")
model = joblib.load("models/model.pkl")
le_sexe = joblib.load("models/encoder_sexe.pkl")
le_region = joblib.load("models/encoder_region.pkl")
feature_cols = joblib.load("models/feature_cols.pkl")
print(f"Modele charge : {list(model.classes_)}")

# Autoriser les requetes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # En dev : tout accepter
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SenSante API is running"}

@app.get("/model-info")
def model_info():
    """Informations sur le modele charge."""
    return {
        "type": type(model).__name__,
        "nombre_arbres": model.n_estimators,
        "classes": list(model.classes_),
        "nombre_features": model.n_features_in_
    }

@app.post("/predict", response_model=DiagnosticOutput)
def predict(patient: PatientInput):
    """Predire un diagnostic a partir des symptomes d'un patient."""

    # 1. Encoder les variables categoriques
    try:
        sexe_enc = le_sexe.transform([patient.sexe])[0]
    except ValueError:
        return DiagnosticOutput(
            diagnostic="erreur", probabilite=0.0,
            confiance="aucune",
            message=f"Sexe invalide : {patient.sexe}. Utiliser M ou F.")

    try:
        region_enc = le_region.transform([patient.region])[0]
    except ValueError:
        return DiagnosticOutput(
            diagnostic="erreur", probabilite=0.0,
            confiance="aucune",
            message=f"Region inconnue : {patient.region}")

    # 2. Construire le vecteur de features
    features = np.array([[
        patient.age, sexe_enc, patient.temperature,
        patient.tension_sys, int(patient.toux),
        int(patient.fatigue), int(patient.maux_tete),
        region_enc
    ]])

    # 3. Predire
    diagnostic = model.predict(features)[0]
    proba_max = float(model.predict_proba(features)[0].max())

    # 4. Determiner le niveau de confiance
    confiance = ("haute" if proba_max >= 0.7
                 else "moyenne" if proba_max >= 0.4
                 else "faible")

    # 5. Generer la recommandation
    messages = {
        "palu": "Suspicion de paludisme. Consultez un medecin rapidement.",
        "paludisme": "Suspicion de paludisme. Consultez un medecin rapidement.",
        "grippe": "Suspicion de grippe. Repos et hydratation recommandes.",
        "typh": "Suspicion de typhoide. Consultation medicale necessaire.",
        "typhoide": "Suspicion de typhoide. Consultation medicale necessaire.",
        "sain": "Pas de pathologie detectee. Continuez a surveiller."
    }

    # 6. Renvoyer le resultat
    return DiagnosticOutput(
        diagnostic=diagnostic,
        probabilite=round(proba_max, 2),
        confiance=confiance,
        message=messages.get(diagnostic, "Consultez un medecin.")
    )

@app.post("/explain", response_model=ExplainOutput)
def explain(data: ExplainInput):
    sexe_label = "Femme" if data.sexe == "F" else "Homme"
    prompt = (
        f"Patient : {sexe_label}, {data.age} ans, région {data.region}\n"
        f"Température : {data.temperature}°C\n"
        f"Diagnostic : {data.diagnostic} (probabilité {data.probabilite:.0%})\n"
        f"Explique ce résultat au patient."
    )
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Tu es un assistant médical sénégalais. Explique le diagnostic en français simple, comme un médecin parlerait à son patient. Sois rassurant et recommande une consultation. Maximum 3 phrases."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=200,
        temperature=0.3
    )
    return ExplainOutput(explication=response.choices[0].message.content)