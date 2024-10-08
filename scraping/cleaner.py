import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Set for storing already visited URLs
visited_urls = set()

def get_page_content(url):
    """
    Returns the content of the webpage at `url`.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_text_elements(soup):
    """
    Extracts text from specific HTML elements like <p> and <div>.
    Returns a list of cleaned text segments.
    """
    text_segments = []
    
    # Extract text from <p> and <div> elements
    for tag in soup.find_all(['p', 'div']):
        text = tag.get_text(separator=' ', strip=True)  # Extract and clean text
        if text:  # Only add non-empty text
            text_segments.append(text)
    
    return text_segments

def clean_text(text):
    """
    Cleans the extracted text by removing unnecessary whitespace and formatting.
    Segments the text into meaningful chunks.
    """
    # Remove extra spaces and unwanted characters
    text = ' '.join(text.split())
    return text

def write_to_jsonl(text_segments):
    """
    Write the extracted and cleaned text segments to a JSON Lines file named token.jsonl.
    """
    if not os.path.exists('data'):
        os.makedirs('data')

    filename = 'data/token.jsonl'  # Set the filename to token.jsonl
    
    # Open the file in append mode to add new lines
    with open(filename, 'a', encoding='utf-8') as f:
        for segment in text_segments:
            json.dump({'text': segment}, f, ensure_ascii=False)
            f.write('\n')  # Write a newline after each JSON object

def scrape(url, depth):
    """
    Scrapes the webpage at `url` up to a certain `depth`.
    """
    scheme = urlparse(url).scheme  # Get the scheme
    domain = urlparse(url).netloc  # Get base domain
    path = os.path.dirname(urlparse(url).path)  # Get base path excluding the last part

    if depth == 0 or url in visited_urls:
        return

    visited_urls.add(url)

    print(f"Scraping: {url}")
    content = get_page_content(url)
    
    if content is None:  # If content couldn't be fetched, skip
        return

    soup = BeautifulSoup(content, "html.parser")
    
    # Extract text segments from the page
    text_segments = extract_text_elements(soup)
    cleaned_segments = [clean_text(text) for text in text_segments]
    
    # Write the cleaned text segments to a JSON Lines file
    write_to_jsonl(cleaned_segments)

    # Get all links to follow for further scraping
    links = get_all_links(content, scheme + "://" + domain + path)

    for link in links:
        scrape(link, depth - 1)

def get_all_links(content, domain):
    """
    Returns all valid links on the page.
    """
    soup = BeautifulSoup(content, "html.parser")
    links = soup.find_all("a")
    valid_links = []

    for link in links:
        href = link.get('href')
        if href is not None and not href.startswith("..") and href != "#" and not href.startswith("#"):
            if href.startswith("http"):
                if href.startswith(domain):
                    print("Following", href)
                    valid_links.append(href)
            else:
                print("Following", strip_after_last_hash(href))
                valid_links.append(domain + '/' + strip_after_last_hash(href))
    return valid_links

def strip_after_last_hash(url):
    """
    Strips off all characters after the last "#" in `url`,
    if "#" does not have a "/" character before it.
    """
    hash_index = url.rfind('#')
    if hash_index > 0 and url[hash_index - 1] != '/':
        return url[:hash_index]
    else:
        return url

# Example usage
scrape('https://aphrc.org/', 2)  # Start scraping from the specified URL with a depth of 2
