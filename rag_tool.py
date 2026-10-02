from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Chargement du modèle d'embedding local
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

@tool
def recherche_documentaire(query: str) -> str:
    """
    Effectue une recherche sémantique dans la documentation stratégique et les rapports de l'entreprise.
    Utilise cet outil UNIQUEMENT lorsque la question porte sur la stratégie, les notes de réunions, 
    ou les explications qualitatives (ex: 'pourquoi les ventes ont baissé ?', 'que dit le plan ?').
    """
    print(f"  [📚 Outil RAG appelé pour : {query}]")
    docs = retriever.invoke(query)
    resultat = "\n\n".join([doc.page_content for doc in docs])
    return resultat

if __name__ == "__main__":
    print(recherche_documentaire.invoke("Quels sont nos objectifs ?"))