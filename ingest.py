import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def creer_base_vectorielle(dossier_source: str, dossier_chroma: str = "./chroma_db"):
    print(f" Lecture de tous les fichiers dans : {dossier_source}")

    # 1. On charge TOUS les fichiers .txt d'un dossier
    loader = DirectoryLoader(dossier_source, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    # Divise les documents en segments.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=dossier_chroma,
    )
    print(f" {len(documents)} documents ajoutés à la base vectorielle !")

if __name__ == "__main__":
    # Il suffit de mettre tous vos textes dans un dossier "mes_documents"
    creer_base_vectorielle("./mes_documents")
