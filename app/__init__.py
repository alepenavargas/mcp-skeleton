"""
MCP Skeleton - Framework for building Model Context Protocol servers

This module provides a flexible and modular foundation for creating MCP servers
that can be used for various use cases, including web navigation, API integration,
data processing, and more.
"""

import os
import sys
import logging
import importlib
from typing import Dict, Any, List, Optional, Type, Callable

import requests
from starlette.routing import Route
from starlette.responses import PlainTextResponse
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import BaseModel, create_model

# Load environment variables from .env file
load_dotenv()

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp-skeleton")

# --- Configuration ---
class MCPConfig:
    """Central configuration class for the MCP server."""
    
    def __init__(self):
        """Initialize configuration with default values and environment overrides."""
        self.name = os.environ.get("MCP_NAME", "MCP-Skeleton")
        self.description = os.environ.get("MCP_DESCRIPTION", "Generic MCP Server")
        self.port = int(os.environ.get("MCP_PORT", 9090))
        self.log_level = os.environ.get("MCP_LOG_LEVEL", "INFO")
        self.additional_config = {}
        
    def add_config(self, key: str, value: Any) -> None:
        """Add a custom configuration value."""
        self.additional_config[key] = value
        
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with an optional default."""
        return self.additional_config.get(key, default)
    
    def load_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Load configuration from a dictionary."""
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.add_config(key, value)
    
    def as_dict(self) -> Dict[str, Any]:
        """Return configuration as a dictionary."""
        config_dict = {
            "name": self.name,
            "description": self.description,
            "port": self.port,
            "log_level": self.log_level
        }
        config_dict.update(self.additional_config)
        return config_dict

# Initialize config
config = MCPConfig()

# Initialize MCP Server
mcp = FastMCP(
    name=config.name,
    description=config.description
)

# --- Base Client Class ---
class BaseClient:
    """Base client class for external service integrations."""
    
    def __init__(self):
        """Initialize the client with common functionality."""
        self.session = requests.Session()
        
    def _handle_request_error(self, error: Exception, url: str) -> Dict[str, Any]:
        """Common error handling for HTTP requests."""
        logger.error(f"Error in request to {url}: {str(error)}")
        return {"error": str(error), "url": url}

# --- Tool Registry ---
class ToolRegistry:
    """Registry for managing and dynamically loading tools."""
    
    def __init__(self, mcp_instance: FastMCP):
        """Initialize the registry with an MCP instance."""
        self.mcp = mcp_instance
        self.registered_tools = {}
        self.tool_modules = []
        
    def register_tool(self, func: Callable, name: Optional[str] = None) -> Callable:
        """Register a function as an MCP tool."""
        tool_name = name or func.__name__
        self.registered_tools[tool_name] = func
        
        # Register with MCP
        return self.mcp.tool()(func)
    
    def register_resource(self, path: str, func: Callable) -> Callable:
        """Register a function as an MCP resource."""
        return self.mcp.resource(path)(func)
    
    def load_tools_from_module(self, module_name: str) -> None:
        """Dynamically load tools from a module."""
        try:
            module = importlib.import_module(module_name)
            self.tool_modules.append(module)
            
            # Find and register all functions with tool_definition attribute
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and hasattr(attr, 'tool_definition'):
                    self.register_tool(attr, attr.tool_definition.get('name'))
                    
            logger.info(f"Loaded tools from module: {module_name}")
            
        except ImportError as e:
            logger.error(f"Error loading tool module {module_name}: {e}")

# Initialize tool registry
tool_registry = ToolRegistry(mcp)

# --- Healthcheck Endpoint ---
async def ping_response(request):
    """Endpoint to verify the server is running."""
    return PlainTextResponse("pong")

# --- Utility Decorators ---
def tool_definition(**kwargs):
    """Decorator to mark a function as a tool and define its properties."""
    def decorator(func):
        func.tool_definition = kwargs
        return func
    return decorator

# --- App Factory ---
def create_app():
    """Create and configure the MCP SSE application."""
    # Set MCP port environment variable
    os.environ["MCP_HTTP_PORT"] = str(config.port)
    
    # Create the SSE app
    app = mcp.sse_app()
    
    # Add healthcheck endpoint
    app.routes.append(
        Route("/ping", endpoint=ping_response, methods=["GET"])
    )
    
    return app 