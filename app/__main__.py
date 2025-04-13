"""
Main entry point for the MCP Skeleton server.
"""

import os
import logging
import uvicorn

from app import create_app, config, logger
from app.tool_loader import auto_discover_and_load_tools

def main():
    """
    Main function to start the MCP server.
    """
    # Get configuration values
    port = config.port
    
    # Discover and load tools
    loaded_tools = auto_discover_and_load_tools()
    logger.info(f"Loaded {loaded_tools} tool modules")
    
    # Create the application
    app = create_app()
    
    # Log startup information
    logger.info(f"Starting {config.name} on port {port}")
    logger.info(f"SSE endpoint: http://localhost:{port}/sse")
    logger.info(f"Health check: http://localhost:{port}/ping")
    
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=config.log_level.lower())

if __name__ == "__main__":
    main() 