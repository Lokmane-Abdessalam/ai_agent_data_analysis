import os

from dotenv import load_dotenv

# ============================================================
# 1. Chargement des variables d'environnement
# ============================================================

load_dotenv(".env", override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

print("ENV FILE LOADED")
print("MODEL:", MODEL_NAME)
print("GROQ_API_KEY exists:", bool(GROQ_API_KEY))
print("GROQ_API_KEY length:", len(GROQ_API_KEY or ""))

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY n'est pas défini dans le fichier .env"
    )

print(f"🤖 Lancement du superviseur avec le modèle : {MODEL_NAME}")


# ============================================================
# 2. Imports LangChain
# ============================================================

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


# ============================================================
# 3. Outils existants
# ============================================================

from agent import full_chain
from rag_tool import recherche_documentaire


# ============================================================
# 4. Création de l'outil SQL
# ============================================================

@tool
def outil_chiffres_ventes(question: str) -> str:
    """
    Interroge la base de données SQL de l'entreprise.

    À utiliser pour obtenir des chiffres précis :
    - montants
    - volumes de ventes
    - nombre de clients
    - revenus
    - statistiques commerciales
    """

    print(f"  [🛠️ Outil SQL appelé pour : {question}]")

    resultat = full_chain.invoke({
        "question": question
    })

    return str(resultat)


# ============================================================
# 5. Liste des outils disponibles
# ============================================================

outils_disponibles = [
    outil_chiffres_ventes,
    recherche_documentaire,
]


# ============================================================
# 6. Prompt du superviseur
# ============================================================

system_prompt = """
Tu es le Chef de Cabinet du PDG.

Ton rôle est de répondre aux questions de la direction
en combinant les données quantitatives de l'entreprise
et les informations qualitatives disponibles dans les documents.

RÈGLES STRICTES :

1. Pour toute question nécessitant des chiffres précis
   (ventes, revenus, montants, volumes, nombre de clients,
   statistiques, etc.), utilise l'outil de données commerciales.

2. Pour une analyse complète combinant chiffres et contexte :

   - récupère d'abord les chiffres avec l'outil de données commerciales ;
   - puis utilise l'outil documentaire pour rechercher
     le contexte qualitatif pertinent.

3. Ne fabrique jamais de chiffres.

   Si une donnée n'est pas disponible, indique-le clairement.

4. Ne mentionne jamais les outils, les fonctions internes,
   les requêtes SQL ou le fonctionnement technique du système
   dans ta réponse finale.

5. Réponds comme un expert qui présente directement
   l'analyse au PDG.

6. Structure les réponses importantes avec :

   ## Les Chiffres

   - résultats quantitatifs importants

   ## L'Analyse Qualitative

   - facteurs explicatifs
   - contexte
   - éléments importants trouvés dans les documents

7. Sois clair, concis et orienté décision.

8. Utilise uniquement les données réellement disponibles.

9. Ne déduis jamais un chiffre qui n'a pas été fourni
   par les données de l'entreprise.
"""


# ============================================================
# 7. Initialisation de Groq
# ============================================================

llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0,
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


# ============================================================
# 8. Création de l'agent superviseur
# ============================================================

superviseur = create_agent(
    model=llm,
    tools=outils_disponibles,
    system_prompt=system_prompt,
)


# ============================================================
# 9. Test du système complet
# ============================================================

if __name__ == "__main__":

    question_pdg = (
        "Donne-moi le montant total des ventes en France, "
        "puis explique-moi qualitativement ce qui a impacté "
        "ces résultats ce trimestre."
    )

    print(f"\n👔 PDG : {question_pdg}\n")
    print("🧠 Le Superviseur réfléchit...\n")

    resultat = superviseur.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question_pdg,
                }
            ]
        }
    )

    print(
        "\n================ SYNTHÈSE FINALE ================\n"
    )

    print(resultat["messages"][-1].content)