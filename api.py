from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import full_chain  # Import du cerveau IA

# 1. Initialisation de l'API
app = FastAPI(
    title="Agent Data Analyst",
    description="API Text-to-SQL propulsée par Gemini et LangChain",
)

# 2. Définition du format de la requête attendue (Validation Pydantic)
class QueryRequest(BaseModel):
    question: str


# 3. Création de la route principale
@app.post("/ask")
async def ask_database(request: QueryRequest):
    try:
        # On transmet la question à la chaîne LCEL
        resultat = full_chain.invoke({"question": request.question})

        # On retourne la réponse au format JSON
        return {"question": request.question, "reponse": resultat}

    except Exception as e:
        # En cas d'erreur (ex: base inaccessible, quota API dépassé)
        raise HTTPException(status_code=500, detail=str(e))
