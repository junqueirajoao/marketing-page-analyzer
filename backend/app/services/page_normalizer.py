"""
Page normalizer service for extracting structured data from raw HTML.
"""
from typing import Dict, List
from bs4 import BeautifulSoup


def normalize_page(raw_page: dict) -> dict:
    """
    Normalize raw page data into structured format.
    
    Args:
        raw_page: Dictionary containing:
            - url: The page URL
            - html: Raw HTML content
            - status_code: HTTP status code (optional)
            - error: Error message if fetch failed (optional)
    
    Returns:
        Dictionary containing:
            - url: The page URL
            - metadata: Dict with title, meta_description, canonical
            - headings: List of dicts with level and text
            - links: List of dicts with text and href
            - images: List of dicts with alt and src
            - main_text: Extracted main text content
            - modules: Empty list (placeholder for future implementation)
            - error: Error message if present
    """
    result = {
        "url": raw_page.get("url", ""),
        "metadata": {
            "title": "",
            "meta_description": "",
            "canonical": ""
        },
        "headings": [],
        "links": [],
        "images": [],
        "main_text": "",
        "modules": [],
        "error": raw_page.get("error")
    }
    
    # If there's an error, return early with empty fields
    if raw_page.get("error"):
        return result
    
    html = raw_page.get("html", "")
    
    # If HTML is empty, return early with empty fields
    if not html or not html.strip():
        return result
    
    # Parse HTML with BeautifulSoup
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        result["error"] = f"HTML parsing error: {str(e)}"
        return result
    
    # Extract metadata
    result["metadata"] = _extract_metadata(soup)
    
    # Extract headings
    result["headings"] = _extract_headings(soup)
    
    # Extract links
    result["links"] = _extract_links(soup)
    
    # Extract images
    result["images"] = _extract_images(soup)
    
    # Extract main text
    result["main_text"] = _extract_main_text(soup)
    
    return result


def _extract_metadata(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Extract metadata from HTML.
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        Dictionary with title, meta_description, canonical
    """
    metadata = {
        "title": "",
        "meta_description": "",
        "canonical": ""
    }
    
    # Extract title
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        metadata["title"] = title_tag.string.strip()
    
    # Extract meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        content = meta_desc.get("content")
        if isinstance(content, str):
            metadata["meta_description"] = content.strip()
    
    # Extract canonical URL
    canonical = soup.find("link", attrs={"rel": "canonical"})
    if canonical and canonical.get("href"):
        href = canonical.get("href")
        if isinstance(href, str):
            metadata["canonical"] = href.strip()
    
    return metadata


def _extract_headings(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Extract all headings from HTML.
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        List of dictionaries with level and text
    """
    headings = []
    
    for level in range(1, 7):  # h1 to h6
        for heading in soup.find_all(f"h{level}"):
            text = heading.get_text().strip()
            if text:  # Only include non-empty headings
                headings.append({
                    "level": str(level),
                    "text": text
                })
    
    return headings


def _extract_links(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Extract all links from HTML.
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        List of dictionaries with text and href
    """
    links = []
    
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href or not isinstance(href, str):  # Ignore links without href
            continue
        
        href = href.strip()
        if not href:  # Ignore empty href
            continue
        
        text = link.get_text().strip()
        links.append({
            "text": text,
            "href": href
        })
    
    return links


def _extract_images(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Extract all images from HTML.
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        List of dictionaries with alt and src
    """
    images = []
    
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src or not isinstance(src, str):  # Ignore images without src
            continue
        
        src = src.strip()
        if not src:  # Ignore empty src
            continue
        
        alt_value = img.get("alt", "")
        alt = alt_value.strip() if isinstance(alt_value, str) else ""
        images.append({
            "alt": alt,
            "src": src
        })
    
    return images


def _extract_main_text(soup: BeautifulSoup) -> str:
    """
    Extract main text content from HTML.
    
    Args:
        soup: BeautifulSoup object
    
    Returns:
        Main text content (limited to 10000 characters)
    """
    # Remove script and style elements
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Clean up text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = " ".join(chunk for chunk in chunks if chunk)
    
    # Limit to 10000 characters to avoid huge payloads
    if len(text) > 10000:
        text = text[:10000]
    
    return text


# Made with Bob