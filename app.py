import gradio as gr
from chatbot import create_rag_pipeline
from embedding import create_chroma_db
from preprocess import load_md_files_for_rag
from config import DATA_DIRECTORY, COLLECTION_NAME

# Process Markdown files
chunks_by_subdir = load_md_files_for_rag(DATA_DIRECTORY)
all_chunks = [chunk for subdir_chunks in chunks_by_subdir.values() for chunk in subdir_chunks]

# Create ChromaDB and RAG pipeline
vectorstore = create_chroma_db(all_chunks, COLLECTION_NAME)
qa_chain = create_rag_pipeline(vectorstore)

def chatbot_interface(query,x):
    """
    Handles user input and generates chatbot responses.

    Args:
        query (str): User's question.

    Returns:
        str: Chatbot's response.
    """
    response = qa_chain.invoke({"query": query})
    return response["result"]

# Create Gradio chat interface
chatbox = gr.ChatInterface(
    fn=chatbot_interface,
    title="Changi Chatbot",
    description="Ask questions about the content of Changi Airport",
    theme="default"
)

if __name__ == "__main__":
    chatbox.launch()

# def chatbot_interface(query):
#     """
#     Handles user input and generates chatbot responses while maintaining context.

#     Args:
#         query (str): User's question.

#     Returns:
#         str: Chatbot's response.
#     """
#     global conversation_history

#     try:
#         logging.info(f"Received user query: {query}")

#         # Validate and prepare context
#         if not isinstance(conversation_history, list):
#             logging.error("conversation_history is not a valid list.")
#             conversation_history = []  # Reinitialize if corrupted

#         context = " ".join([f"Q: {q} A: {a}" for q, a in conversation_history]) if conversation_history else ""

#         # Append the query to context
#         query_with_context = f"{context} Q: {query}" if context else query

#         # Get response from the RAG pipeline
#         response = qa_chain.invoke({"query": query_with_context})["result"]

#         # Update conversation history (limit to last 5 turns)
#         conversation_history.append((query, response))
#         if len(conversation_history) > 5:
#             conversation_history.pop(0)

#         logging.info(f"Generated response: {response}")
#         return response
#     except Exception as e:
#         logging.error(f"Error in chatbot interface: {e}")
#         return "Sorry, an error occurred while processing your request."
