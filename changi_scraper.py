import asyncio
import logging
import os
import json
from pathlib import Path
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("crawler.log"),
        logging.StreamHandler()
    ]
)

# Directory for storing scraped data
BASE_DIR = Path("scraped_data_hipster_1")
BASE_DIR.mkdir(exist_ok=True)

def setup_logger():
    """
    Configure and return the logger instance.
    """
    logger = logging.getLogger(__name__)
    return logger

# Initialize logger
logger = setup_logger()

# Utility function to save content to a file
def save_content(file_path, content):
    """
    Saves content to a specified file.

    Args:
        file_path (Path): The path where content will be saved.
        content (str): The content to save.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Utility function to save media files
def save_media(media_type, media_list, base_dir):
    """
    Saves media details such as images and videos.

    Args:
        media_type (str): The type of media (e.g., 'images', 'videos').
        media_list (list): List of media metadata dictionaries.
        base_dir (Path): The base directory to save the media metadata.
    """
    media_dir = base_dir / media_type
    media_dir.mkdir(exist_ok=True)
    for media in media_list:
        media_file = media_dir / Path(media["src"]).name
        save_content(media_file, json.dumps(media))
        logger.info(f"Saved {media_type} metadata: {media_file}")

# Crawl a single page and its links
async def crawl_page(crawler, url, visited, base_dir):
    """
    Crawls a single page, saves its content, media, and recursively visits links.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        url (str): The URL to crawl.
        visited (set): A set of already visited URLs.
        base_dir (Path): The base directory for saving content.
    """
    if url in visited:
        logger.info(f"URL already visited: {url}")
        return
    visited.add(url)

    logger.info(f"Scraping URL: {url}")
    try:
        # Crawl the page
        result = await crawler.arun(
            url=url,
            process_iframes=True,                  # Extract iframe content
            remove_overlay_elements=True,         # Remove popups and overlays
            screenshot=True,                      # Capture a screenshot
            magic=True,                           # Enable anti-detection
            bypass_cache=True                     # Avoid cached responses
        )

        # Check if the crawling was successful
        if result.success:
            # Create a directory for the page
            page_dir = base_dir / Path(url).name
            page_dir.mkdir(exist_ok=True)

            # Save extracted content
            save_content(page_dir / "content.html", result.html)
            save_content(page_dir / "content.md", result.markdown)
            save_content(page_dir / "content.json", json.dumps(result.metadata))
            logger.info(f"Saved content for: {url}")

            # Save media files
            save_media("images", result.media["images"], page_dir)
            save_media("videos", result.media["videos"], page_dir)

            # Extract PDFs and other files
            pdfs = [link for link in result.links["internal"] if link["href"].endswith(".pdf")]
            for pdf in pdfs:
                pdf_path = page_dir / Path(pdf["href"]).name
                save_content(pdf_path, f"PDF Placeholder for {pdf['href']}")  # Replace with download logic.
                logger.info(f"Saved PDF metadata: {pdf['href']}")

            # Recursively crawl internal links
            for link in result.links["internal"]:
                await crawl_page(crawler, link["href"], visited, base_dir)
        else:
            logger.warning(f"Failed to scrape: {url} - Error: {result.error_message}")
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")

# Main function for starting the crawl
async def main(start_url):
    """
    Main entry point for the crawling process.

    Args:
        start_url (str): The starting URL for the crawler.
    """
    async with AsyncWebCrawler(verbose=True) as crawler:
        visited = set()  # To track visited URLs and avoid duplicates
        await crawl_page(crawler, start_url, visited, BASE_DIR)

# Entry point for script execution
if __name__ == "__main__":
    # Replace with the starting URL
    start_url = "https://www.jewelchangiairport.com/"
    logger.info("Starting the crawl process")
    asyncio.run(main(start_url))
    logger.info("Crawl process completed")
