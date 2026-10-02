import os
from operator import itemgetter
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. Chargement des variables d'environnement
load_dotenv(".env", override=True)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "llama3-70b-8192") # Modèle par défaut suggéré pour le code

# 2. Base de données et LLM
db = SQLDatabase.from_uri("sqlite:///ventes.db")

llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0,
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# 3. Fonctions utilitaires
def get_schema(_):
    return db.get_table_info()

def run_query(query: str):
    clean_query = query.replace("```sql", "").replace("```", "").strip()
    print(f" > SQL Exécuté : {clean_query}")
    return db.run(clean_query)

# 4. Prompts
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

# 5. Pipeline LCEL
generate_query_chain = (
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
    print(f"🤖 Test de l'Agent SQL avec {MODEL_NAME} sur Groq...")
    reponse = full_chain.invoke({"question": "Quel est le montant total des commandes passées par des clients en France ?"})
    print(f"\nRéponse finale : {reponse}\n")