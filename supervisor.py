import os

from dotenv import load_dotenv
from agent_rh import full_chain_rh

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

print(f"Lancement du superviseur avec le modèle : {MODEL_NAME}")


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
# 4. Création de l'outil SQL (Noms verrouillés)
# ============================================================

# ASTUCE : On force le nom de l'outil ici
@tool("outil_chiffres_ventes")
def outil_chiffres_ventes(question: str) -> str:
    """
    Interroge la base de données SQL de l'entreprise.
    À utiliser pour obtenir des chiffres précis : montants, volumes de ventes, nombre de clients, revenus.
    """
    print(f"  [Outil SQL appelé pour : {question}]")
    resultat = full_chain.invoke({"question": question})
    return str(resultat)

# ASTUCE : On force le nom de l'outil ici aussi
@tool("outil_ressources_humaines")
def outil_ressources_humaines(question: str) -> str:
    """Utilise cet outil EXCLUSIVEMENT pour les questions liées aux employés, aux salaires, aux congés et aux recrutements."""
    return full_chain_rh.invoke({"question": question})

# ============================================================
# 5. Liste des outils disponibles
# ============================================================

outils_disponibles = [
    outil_chiffres_ventes,
    outil_ressources_humaines,
    recherche_documentaire,
]


# ============================================================
# 6. Prompt du superviseur (Noms explicites ajoutés)
# ============================================================

system_prompt = """
Tu es le Chef de Cabinet du PDG.

Ton rôle est de répondre aux questions de la direction en combinant les données quantitatives et qualitatives.

RÈGLES STRICTES DE ROUTAGE (NE TE TROMPE JAMAIS DE NOM D'OUTIL) :
1. VENTES : Pour les revenus, montants, ou clients, appelle l'outil exact `outil_chiffres_ventes`.
2. RH : Pour les employés, effectifs, ou salaires, appelle l'outil exact `outil_ressources_humaines`.
3. STRATÉGIE : Pour le contexte qualitatif, rapports ou réunions, appelle l'outil exact `recherche_documentaire`.

AUTRES RÈGLES :
- Pour une analyse complète combinant chiffres et contexte, récupère d'abord les chiffres avec l'outil SQL approprié, PUIS utilise l'outil documentaire.
- Ne fabrique jamais de chiffres. Si une donnée n'est pas disponible, indique-le.
- Ne mentionne jamais les outils, requêtes SQL ou le fonctionnement technique dans ta réponse finale.
- Structure tes réponses avec "## Les Chiffres" et "## L'Analyse Qualitative".
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

    print(f"\nPDG : {question_pdg}\n")
    print("Le Superviseur réfléchit...\n")

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

    print("\n================ SYNTHÈSE FINALE ================\n")

    print(resultat["messages"][-1].content)
