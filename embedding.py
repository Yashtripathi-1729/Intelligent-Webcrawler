from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def create_chroma_db(chunks: list, collection_name: str):
    """
    Create a ChromaDB instance and store embeddings.

    Args:
        chunks (list): List of document chunks.
        collection_name (str): Name of the ChromaDB collection.

    Returns:
        Chroma: ChromaDB instance with stored embeddings.
    """
    logging.info(f"Initializing embeddings with SentenceTransformers model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory="./chromadb"  # Directory to persist ChromaDB
    )

    logging.info("Adding document chunks to ChromaDB...")
    vectorstore.add_documents(chunks)

    logging.info(f"ChromaDB setup complete with collection: {collection_name}")
    return vectorstore
