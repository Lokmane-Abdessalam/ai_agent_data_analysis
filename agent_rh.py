import os
from operator import itemgetter
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ============================================================
# 1. Chargement des variables d'environnement
# ============================================================
load_dotenv(".env", override=True)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# ============================================================
# 2. Connexion à la Base de Données RH
# ============================================================
# Pour tester localement avec un fichier SQLite :
db_rh = SQLDatabase.from_uri("sqlite:///rh.db")

# Si vous avez une vraie base PostgreSQL, commentez la ligne ci-dessus 
# et décommentez celle du dessous en mettant vos identifiants :
# db_rh = SQLDatabase.from_uri("postgresql+psycopg2://utilisateur:motdepasse@localhost:5432/base_rh")

# ============================================================
# 3. Initialisation du LLM (Groq)
# ============================================================
llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0,
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# ============================================================
# 4. Fonctions utilitaires
# ============================================================
def get_schema(_):
    return db_rh.get_table_info()

def run_query(query: str):
    clean_query = query.replace("```sql", "").replace("```", "").strip()
    print(f" > SQL RH Exécuté : {clean_query}")
    return db_rh.run(clean_query)

# ============================================================
# 5. Prompts spécialisés RH
# ============================================================
sql_prompt = ChatPromptTemplate.from_template(
    "Tu es un expert SQL spécialisé dans les bases de données de Ressources Humaines (RH).\n"
    "Écris une requête SQL pour répondre à la question.\n"
    "Ne renvoie QUE la requête SQL, sans aucun texte autour.\n\n"
    "Schéma de la base RH :\n{schema}\n\n"
    "Question : {question}\n"
    "Requête SQL :"
)

answer_prompt = ChatPromptTemplate.from_template(
    "En te basant sur la question, la requête SQL et le résultat brut ci-dessous, "
    "rédige une réponse naturelle et professionnelle en français pour la direction des Ressources Humaines.\n\n"
    "Question : {question}\n"
    "SQL : {query}\n"
    "Résultat brut : {result}\n\n"
    "Réponse finale :"
)

# ============================================================
# 6. Pipeline LCEL
# ============================================================
generate_query_chain = (
    {"schema": get_schema, "question": itemgetter("question")} 
    | sql_prompt
    | llm
    | StrOutputParser()
)

full_chain_rh = (
    RunnablePassthrough.assign(query=generate_query_chain)
    .assign(result=lambda x: run_query(x["query"]))
    | answer_prompt
    | llm
    | StrOutputParser()
)

# ============================================================
# 7. Test unitaire du module
# ============================================================
if __name__ == "__main__":
    print(f"🤖 Test de l'Agent RH avec {MODEL_NAME} sur Groq...")
    
    # Ce test échouera si la base rh.db n'existe pas ou est vide.
    question = "Combien avons-nous d'employés au total et quel est le salaire moyen ?"
    print(f"Question : {question}")
    
    try:
        reponse = full_chain_rh.invoke({"question": question})
        print(f"\nRéponse finale : {reponse}\n")
    except Exception as e:
        print(f"\nErreur (Vérifiez que rh.db existe bien et contient des tables) : {e}")