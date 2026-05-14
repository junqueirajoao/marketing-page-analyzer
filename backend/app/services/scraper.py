"""
Scraper service for fetching HTML content from URLs.
"""
import httpx
from typing import Dict, Optional


async def fetch_page(url: str) -> Dict[str, Optional[str]]:
    """
    Fetch HTML content from a given URL.
    
    Args:
        url: The URL to fetch
        
    Returns:
        Dictionary containing:
        - url: The original URL
        - status_code: HTTP status code (None if request failed)
        - html: HTML content (empty string if request failed)
        - error: Error message (None if successful)
    """
    result = {
        "url": url,
        "status_code": None,
        "html": "",
        "error": None
    }
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36"
        )
    }
    
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                url, headers=headers, follow_redirects=True
            )
            result["status_code"] = response.status_code
            result["html"] = response.text
            
    except httpx.TimeoutException:
        result["error"] = "Request timeout after 20 seconds"
        
    except httpx.RequestError as e:
        result["error"] = f"Request error: {str(e)}"
        
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
    
    return result

# Made with Bob
