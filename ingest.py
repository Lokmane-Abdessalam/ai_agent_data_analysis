import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def creer_base_vectorielle(chemin_txt: str, dossier_chroma: str = "./chroma_db"):
    print(f"📄 Lecture du document : {chemin_txt}")
    loader = TextLoader(chemin_txt, encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    
    # Modèle local open-source (tourne sur votre CPU, pas besoin d'API)
    print("⏳ Téléchargement/Chargement du modèle d'embedding local...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("🧠 Création des vecteurs et sauvegarde dans ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=dossier_chroma
    )
    print("✅ Base de données vectorielle prête !")

if __name__ == "__main__":
    creer_base_vectorielle("rapport_strat.txt")