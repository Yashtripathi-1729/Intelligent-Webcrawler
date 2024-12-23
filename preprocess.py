import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
import re
from langchain.docstore.document import Document


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def clean_markdown_content(md_content: str) -> str:
    """
    Cleans Markdown content by removing tags, links, and unnecessary syntax.

    Args:
        md_content (str): The raw Markdown content.

    Returns:
        str: Cleaned plain text suitable for embedding.
    """
    # Remove Markdown links (e.g., [text](url))
    cleaned_content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', md_content)

    # Remove inline HTML tags if any exist in the Markdown
    cleaned_content = re.sub(r'<[^>]+>', '', cleaned_content)

    # Remove Markdown image syntax (e.g., ![alt text](url))
    cleaned_content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', cleaned_content)

    # Remove headings (optional: Keep heading text but strip hashes)
    cleaned_content = re.sub(r'#+\s*', '', cleaned_content)

    # Remove other Markdown formatting symbols like *, _, ~ for bold/italics/strikethrough
    cleaned_content = re.sub(r'[*_~]', '', cleaned_content)

    # Collapse multiple newlines into one
    cleaned_content = re.sub(r'\n\s*\n', '\n', cleaned_content)

    return cleaned_content.strip()

def load_md_files_for_rag(parent_directory: str):
    """
    Load, clean, and process Markdown (.md) files for RAG from a directory.

    Args:
        parent_directory (str): Path to the directory containing .md files.

    Returns:
        dict: Dictionary with subdirectory names as keys and lists of chunks as values.
    """
    all_chunks = {}
    logging.info(f"Scanning parent directory: {parent_directory}...")

    # Iterate over subdirectories
    for subdir in os.listdir(parent_directory):
        subdir_path = os.path.join(parent_directory, subdir)
        if os.path.isdir(subdir_path):
            logging.info(f"Processing subdirectory: {subdir}")

            # Collect chunks for this subdirectory
            subdir_chunks = []
            for root, _, files in os.walk(subdir_path):
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        logging.info(f"Processing file: {file_path}")

                        # Load and clean Markdown content
                        with open(file_path, 'r', encoding='utf-8') as f:
                            md_content = f.read()
                        plain_text = clean_markdown_content(md_content)

                        # Create a Document object
                        document = Document(page_content=plain_text)

                        # Split content into page-like chunks
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=2000,  # Approximate page size
                            chunk_overlap=200  # overlap for independent pages
                        )
                        subdir_chunks.extend(text_splitter.split_documents([document]))

            logging.info(f"Processed {len(subdir_chunks)} chunks in subdirectory: {subdir}")
            all_chunks[subdir] = subdir_chunks

    logging.info(f"Completed processing all subdirectories in {parent_directory}.")
    return all_chunks

