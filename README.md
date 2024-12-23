**Description**
This is an Intelligent Webscrapper Incorporated with Chatbot which Uses Crawl4ai to scrape a website by iterating over the internal and external links present on the website and gets me the following files

1. Markdown File (content.md file)
2. Json File (content.json file)
3. HTML File (conten.html file)
4. Media Files (Images , Video and pdfs )

In this I used **Sentence-Transformer(all-MiniLM-L6-v2)** to create the embedding of the content available in Markdown file which I preprocessed by cleaning the whitespaces and other noise which was present in the markdown file and then stored the embedding in ChromaDB Vector Store where I created the pages wise chuncks of the embeddings. 
Priorly I Scraped the Changi-Airport Website and extracted the necessary content.

Then I used OpenAI Chatgpt-4 to get a context based response for my user query where the results from RAG will be converted into proper answer with context and the Conversational Chatbot is hosted with the help of Gradio ChatInterface 

**Work-Flow**

Preprocessing:
    Load and clean Markdown and HTML files from a directory.
    Split content into chunks to preserve context.
Embedding Generation:
    Use sentence-transformers to generate embeddings for chunks.
    Store embeddings in ChromaDB along with metadata.
Chatbot Setup:
    Use ChromaDB as a retriever for relevant content.
    Create a RAG pipeline with GPT-4 to provide context-based answers.
User Interaction:
    Use Gradio to create an interactive chatbot interface for querying the data.


**Further Advancements**

1. Content Enrichment and Filtering - Using more rich content and the filtering your content will make the answer less vague
2. Better Embedding Model - Try expermenting on more embedding model
3. Incorporating Multi Modality - Add multimodal capabilities, allowing users to upload files for live processing
4. Scalability - Use distributed systems like FAISS or Weaviate for handling large-scale datasets.
5. Caching - Implement caching for frequently asked questions to improve response times.
6. Realtime Updates - Set up pipelines to periodically reprocess new files and update the embeddings in ChromaDB.


**P.S.**
Create you own config.py file which contains the API keys 
