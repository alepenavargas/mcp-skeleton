"""
API Tools for MCP Skeleton

This module provides tools for working with common API patterns.
"""

import os
from typing import Dict, Any, List, Optional, Union

from app import BaseClient, tool_definition, config

class APIClient(BaseClient):
    """Base client for API integrations."""
    
    def __init__(self, base_url: str = None, api_key: str = None, api_key_header: str = "Authorization"):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for API requests
            api_key: API key for authentication
            api_key_header: Header name for the API key
        """
        super().__init__()
        self.base_url = base_url or os.environ.get("API_BASE_URL", "")
        self.api_key = api_key or os.environ.get("API_KEY", "")
        self.api_key_header = api_key_header
        
        # Set up default headers if API key is provided
        if self.api_key:
            self.session.headers.update({
                self.api_key_header: self.api_key
            })
    
    def build_url(self, endpoint: str) -> str:
        """
        Build a full URL from the endpoint.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Full URL for the API request
        """
        if endpoint.startswith(('http://', 'https://')):
            return endpoint
        
        # Make sure there's a single slash between base_url and endpoint
        base = self.base_url.rstrip('/')
        clean_endpoint = endpoint.lstrip('/')
        return f"{base}/{clean_endpoint}"
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            API response data
        """
        url = self.build_url(endpoint)
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_request_error(e, url)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: API endpoint
            data: Request payload
            
        Returns:
            API response data
        """
        url = self.build_url(endpoint)
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_request_error(e, url)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a PUT request to the API.
        
        Args:
            endpoint: API endpoint
            data: Request payload
            
        Returns:
            API response data
        """
        url = self.build_url(endpoint)
        try:
            response = self.session.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_request_error(e, url)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Make a DELETE request to the API.
        
        Args:
            endpoint: API endpoint
            
        Returns:
            API response data
        """
        url = self.build_url(endpoint)
        try:
            response = self.session.delete(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_request_error(e, url)

# Create an API client instance
# This can be customized or extended for specific APIs
api_client = APIClient()

# --- Tool Definitions ---

@tool_definition(name="api_get", description="Make a GET request to an API endpoint")
def api_get(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Make a GET request to an API endpoint.
    
    Args:
        endpoint: API endpoint (path relative to base URL or full URL)
        params: Optional query parameters
        
    Returns:
        API response data
    """
    return api_client.get(endpoint, params)

@tool_definition(name="api_post", description="Make a POST request to an API endpoint")
def api_post(
    endpoint: str,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Make a POST request to an API endpoint.
    
    Args:
        endpoint: API endpoint (path relative to base URL or full URL)
        data: Request payload
        
    Returns:
        API response data
    """
    return api_client.post(endpoint, data)

@tool_definition(name="api_put", description="Make a PUT request to an API endpoint")
def api_put(
    endpoint: str,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Make a PUT request to an API endpoint.
    
    Args:
        endpoint: API endpoint (path relative to base URL or full URL)
        data: Request payload
        
    Returns:
        API response data
    """
    return api_client.put(endpoint, data)

@tool_definition(name="api_delete", description="Make a DELETE request to an API endpoint")
def api_delete(
    endpoint: str
) -> Dict[str, Any]:
    """
    Make a DELETE request to an API endpoint.
    
    Args:
        endpoint: API endpoint (path relative to base URL or full URL)
        
    Returns:
        API response data
    """
    return api_client.delete(endpoint) 