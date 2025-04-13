"""
HTTP Tools for MCP Skeleton

This module provides common HTTP request tools that can be used by MCP applications.
"""

import json
from typing import Dict, Any, Optional, List

import requests
from app import BaseClient, tool_definition

class HTTPClient(BaseClient):
    """Client for making HTTP requests."""
    
    def __init__(self):
        """Initialize the HTTP client."""
        super().__init__()
        
    def make_request(
        self, 
        method: str, 
        url: str, 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            url: URL for the request
            params: Query parameters
            headers: Request headers
            data: Form data to send
            json_data: JSON data to send
            
        Returns:
            Response data or error information
        """
        try:
            # Prepare request kwargs
            kwargs = {}
            if params:
                kwargs['params'] = params
            if headers:
                kwargs['headers'] = headers
            if data:
                kwargs['data'] = data
            if json_data:
                kwargs['json'] = json_data
                
            # Make the request
            response = self.session.request(method.upper(), url, **kwargs)
            response.raise_for_status()
            
            # Parse response
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                return {
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'data': response.json(),
                    'url': url
                }
            else:
                return {
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'text': response.text,
                    'url': url
                }
                
        except requests.exceptions.RequestException as e:
            return self._handle_request_error(e, url)

# Create a client instance
http_client = HTTPClient()

# --- Tool Definitions ---

@tool_definition(name="http_get", description="Make an HTTP GET request to a URL")
def http_get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Make an HTTP GET request.
    
    Args:
        url: The URL to request
        params: Optional query parameters
        headers: Optional HTTP headers
        
    Returns:
        The HTTP response data
    """
    return http_client.make_request("GET", url, params=params, headers=headers)

@tool_definition(name="http_post", description="Make an HTTP POST request to a URL")
def http_post(
    url: str,
    data: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Make an HTTP POST request.
    
    Args:
        url: The URL to request
        data: Form data to send
        json_data: JSON data to send
        params: Optional query parameters
        headers: Optional HTTP headers
        
    Returns:
        The HTTP response data
    """
    return http_client.make_request(
        "POST", 
        url, 
        params=params, 
        headers=headers, 
        data=data, 
        json_data=json_data
    )

@tool_definition(name="http_put", description="Make an HTTP PUT request to a URL")
def http_put(
    url: str,
    data: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Make an HTTP PUT request.
    
    Args:
        url: The URL to request
        data: Form data to send
        json_data: JSON data to send
        params: Optional query parameters
        headers: Optional HTTP headers
        
    Returns:
        The HTTP response data
    """
    return http_client.make_request(
        "PUT", 
        url, 
        params=params, 
        headers=headers, 
        data=data, 
        json_data=json_data
    )

@tool_definition(name="http_delete", description="Make an HTTP DELETE request to a URL")
def http_delete(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Make an HTTP DELETE request.
    
    Args:
        url: The URL to request
        params: Optional query parameters
        headers: Optional HTTP headers
        
    Returns:
        The HTTP response data
    """
    return http_client.make_request("DELETE", url, params=params, headers=headers) 