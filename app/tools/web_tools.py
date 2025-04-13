"""
Web Tools for MCP Skeleton

This module provides tools for navigating and scraping web pages.
"""

import urllib.parse
from typing import Dict, Any, List, Optional

import requests
from bs4 import BeautifulSoup

from app import BaseClient, tool_definition, logger

class WebNavigator(BaseClient):
    """Client for navigating web pages."""
    
    def __init__(self):
        """Initialize the web navigator."""
        super().__init__()
        self.current_url = None
        self.history = []
        
    def navigate_to(self, url: str, base_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Navigate to a URL and parse the page content.
        
        Args:
            url: The URL to navigate to (can be relative)
            base_url: Optional base URL for resolving relative URLs
            
        Returns:
            Parsed page content
        """
        # Resolve relative URLs
        full_url = url
        if not url.startswith(('http://', 'https://')):
            if base_url or self.current_url:
                full_url = urllib.parse.urljoin(base_url or self.current_url, url)
            else:
                return {"error": "Cannot resolve relative URL without a base URL"}
        
        try:
            logger.info(f"Navigating to {full_url}")
            response = self.session.get(full_url)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract main content
            main_content = soup.find("main") or soup.find("article") or soup.find("div", class_="content") or soup.find("body")
            
            # Extract links
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                text = a.get_text().strip()
                if text and href:  # Only include non-empty links
                    links.append({
                        "text": text,
                        "url": href
                    })
            
            # Update navigation state
            self.current_url = full_url
            if full_url not in self.history:
                self.history.append(full_url)
            
            # Return structured data
            return {
                "url": full_url,
                "title": soup.title.string if soup.title else "No title",
                "content": main_content.get_text("\n", strip=True) if main_content else "",
                "links": links[:20],  # Limit to 20 links to avoid overwhelming data
                "html": str(main_content) if main_content else ""
            }
            
        except Exception as e:
            return self._handle_request_error(e, full_url)

# Create a navigator instance
web_navigator = WebNavigator()

# --- Tool Definitions ---

@tool_definition(name="navigate", description="Navigate to a web page")
def navigate(url: str) -> Dict[str, Any]:
    """
    Navigate to a web page and extract its content.
    
    Args:
        url: The URL to navigate to (can be absolute or relative)
        
    Returns:
        Parsed content from the web page
    """
    return web_navigator.navigate_to(url)

@tool_definition(name="current_page", description="Get content from the current page")
def current_page() -> Dict[str, Any]:
    """
    Get content from the current page.
    
    Returns:
        Parsed content from the current page or an error if no page has been visited
    """
    if not web_navigator.current_url:
        return {"error": "No page has been visited yet. Use 'navigate' first."}
    return web_navigator.navigate_to(web_navigator.current_url)

@tool_definition(name="browse_history", description="Get the browsing history")
def browse_history() -> List[str]:
    """
    Get the list of visited URLs.
    
    Returns:
        List of previously visited URLs
    """
    return web_navigator.history

@tool_definition(name="extract_links", description="Extract all links from the current page")
def extract_links() -> List[Dict[str, str]]:
    """
    Extract all links from the current page.
    
    Returns:
        List of links with text and URL
    """
    page_data = current_page()
    return page_data.get("links", []) 