"""
Tool Loader for MCP Skeleton

This module provides functionality to load and register tools dynamically.
"""

import importlib
import inspect
import logging
import os
import sys
from typing import List, Optional

from app import tool_registry, logger

def load_tool_modules(module_paths: Optional[List[str]] = None) -> int:
    """
    Load tool modules and register their tools.
    
    Args:
        module_paths: List of module paths to load. If None, uses environment variable.
        
    Returns:
        Number of modules loaded
    """
    if module_paths is None:
        # Get module paths from environment variable
        module_paths_str = os.environ.get("MCP_TOOL_MODULES", "app.tools.http_tools,app.tools.web_tools,app.tools.api_tools")
        module_paths = module_paths_str.split(",") if module_paths_str else []
    
    loaded_count = 0
    for module_path in module_paths:
        try:
            tool_registry.load_tools_from_module(module_path.strip())
            loaded_count += 1
        except Exception as e:
            logger.error(f"Failed to load tool module {module_path}: {e}")
    
    logger.info(f"Loaded {loaded_count} tool modules")
    return loaded_count

def discover_tool_modules(package_path: str = "app.tools") -> List[str]:
    """
    Discover all tool modules in a package.
    
    Args:
        package_path: Package path to scan for modules
        
    Returns:
        List of discovered module paths
    """
    discovered_modules = []
    
    try:
        package = importlib.import_module(package_path)
        package_dir = os.path.dirname(inspect.getfile(package))
        
        # Find Python files
        for file in os.listdir(package_dir):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = file[:-3]  # Remove .py extension
                full_module_path = f"{package_path}.{module_name}"
                discovered_modules.append(full_module_path)
                
        logger.info(f"Discovered {len(discovered_modules)} tool modules in {package_path}")
        
    except (ImportError, FileNotFoundError) as e:
        logger.error(f"Error discovering modules in {package_path}: {e}")
    
    return discovered_modules

def auto_discover_and_load_tools() -> int:
    """
    Automatically discover and load all tool modules.
    
    Returns:
        Number of modules loaded
    """
    module_paths = discover_tool_modules()
    return load_tool_modules(module_paths) 