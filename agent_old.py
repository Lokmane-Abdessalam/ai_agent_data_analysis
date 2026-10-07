import os
from operator import itemgetter  # Nouvel import

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI

# Charge les variables du fichier .env dans l'environnement Python
load_dotenv(".env")

# 2. Base de données et LLM
db = SQLDatabase.from_uri("sqlite:///ventes.db")
# On récupère le modèle depuis le .env (avec gemini-1.5-flash par défaut en cas d'oubli)
nom_modele = os.getenv("GEMINI_MODEL")
print(f"Lancement du superviseur avec le modèle : {nom_modele}")

llm = ChatGoogleGenerativeAI(model=nom_modele, temperature=0)


def get_schema(_):
    return db.get_table_info()


def run_query(query: str):
    clean_query = query.replace("```sql", "").replace("```", "").strip()
    print(f" > SQL Exécuté : {clean_query}")
    return db.run(clean_query)


sql_prompt = ChatPromptTemplate.from_template(
    "Tu es un expert SQLite. Écris une requête SQL pour répondre à la question.\n"
    "Ne renvoie QUE la requête SQL, sans aucun texte autour.\n\n"
    "Schéma de la base :\n{schema}\n\n"
    "Question : {question}\n"
    "Requête SQL :"
)

answer_prompt = ChatPromptTemplate.from_template(
    "En te basant sur la question, la requête SQL et le résultat brut ci-dessous, "
    "rédige une réponse naturelle et concise en français.\n\n"
    "Question : {question}\n"
    "SQL : {query}\n"
    "Résultat brut : {result}\n\n"
    "Réponse finale :"
)

# Correction
generate_query_chain = (
    # On extrait la clé "question" du dictionnaire d'entrée.
    {"schema": get_schema, "question": itemgetter("question")}
    | sql_prompt
    | llm
    | StrOutputParser()
)

full_chain = (
    RunnablePassthrough.assign(query=generate_query_chain)
    .assign(result=lambda x: run_query(x["query"]))
    | answer_prompt
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    question = "Quel est le montant total des commandes passées par des clients en France ?"
    print(f"\nQuestion : {question}")
    print("Analyse en cours...\n")

    # On envoie un dictionnaire.
    reponse = full_chain.invoke({"question": question})
    print(f"\nRéponse finale : {reponse}\n")
