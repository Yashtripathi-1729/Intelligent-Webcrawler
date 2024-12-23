from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import logging
from config import OPENAI_API_KEY
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def create_rag_pipeline(vectorstore):
    """
    Create a Retrieval-Augmented Generation (RAG) pipeline using ChromaDB.

    Args:
        vectorstore (Chroma): ChromaDB instance.

    Returns:
        RetrievalQA: The RAG pipeline.
    """
    logging.info("Creating RAG pipeline...")
    retriever = vectorstore.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0, model_name="gpt-4" , openai_api_key = OPENAI_API_KEY),
        retriever=retriever,
        return_source_documents=True
    )

    logging.info("RAG pipeline setup complete.")
    return qa_chain
