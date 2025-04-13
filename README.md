# MCP Skeleton

A flexible and modular framework for building MCP (Model Context Protocol) servers in Python. This skeleton provides a solid foundation for creating various MCP implementations, including web scrapers, API clients, data processors, and more.

## Features

- **Modular Architecture**: Easily extend with custom tools and functionality
- **Dynamic Tool Loading**: Automatically discover and register tools
- **Ready-to-Use Tools**: Built-in HTTP, Web, and API tools
- **Configurable**: Configure through environment variables or code
- **Docker Support**: Ready for containerized deployment
- **SSE Transport**: Uses MCP Server-Sent Events for standard communication

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)

### Installation

1. Clone the repository or copy the skeleton:

```bash
# Option 1: Clone the repo
git clone https://github.com/your-username/mcp-skeleton.git
cd mcp-skeleton

# Option 2: Copy the skeleton to your project
cp -r /path/to/mcp_skeleton your-project/
cd your-project
```

2. Install dependencies:

```bash
poetry install
```

### Running the Server

You can run the server directly with Poetry:

```bash
poetry run python -m app
```

Or activate the Poetry environment first:

```bash
poetry shell
python -m app
```

The server will start on port 9090 by default. You can access:
- SSE endpoint: http://localhost:9090/sse
- Health check: http://localhost:9090/ping

### Docker

Build and run with Docker:

```bash
docker build -t mcp-skeleton .
docker run -p 9090:9090 mcp-skeleton
```

Or use Docker Compose:

```bash
docker-compose up
```

## Configuration

The MCP server can be configured through environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| MCP_NAME | Server name | MCP-Skeleton |
| MCP_DESCRIPTION | Server description | Generic MCP Server |
| MCP_PORT | Port to run on | 9090 |
| MCP_LOG_LEVEL | Logging level | INFO |
| MCP_TOOL_MODULES | Comma-separated list of tool modules | app.tools.http_tools,app.tools.web_tools,app.tools.api_tools |
| API_BASE_URL | Base URL for API tools | None |
| API_KEY | API key for authentication | None |

You can set these in a `.env` file or pass them directly when running the server.

## Customizing the Framework

### Creating Custom Tools

1. Create a new module in the `app/tools` directory:

```python
# app/tools/custom_tools.py
from app import BaseClient, tool_definition

class CustomClient(BaseClient):
    """Custom client implementation."""
    
    def __init__(self):
        super().__init__()
        # Add custom initialization
    
    def custom_method(self, param1, param2):
        # Implement custom functionality
        return {"result": "success"}

# Create client instance
custom_client = CustomClient()

# Define tools
@tool_definition(name="custom_tool", description="Description of your custom tool")
def custom_tool(param1: str, param2: int = 0):
    """
    Documentation for your custom tool.
    
    Args:
        param1: First parameter
        param2: Second parameter
        
    Returns:
        Custom result
    """
    return custom_client.custom_method(param1, param2)
```

2. The tool will be automatically discovered and registered when the server starts.

### Extending Base Classes

You can extend the base classes to add custom functionality:

```python
# Your custom module
from app import BaseClient

class EnhancedClient(BaseClient):
    """Enhanced client with additional features."""
    
    def __init__(self):
        super().__init__()
        # Add custom initialization
        
    def additional_method(self):
        # Implement additional functionality
        pass
```

## Examples

### Web Navigation MCP

Here's how to use the skeleton to create a web navigation MCP:

```python
# In app/__init__.py or a custom module
from app import config

# Update configuration
config.name = "MCP-Navigator"
config.description = "Web Navigation MCP Server"

# The tools will be registered automatically
# Just run the server and it will have web navigation functionality
```

### API Integration MCP

For an API integration MCP:

```python
# In app/__init__.py or a custom module
from app import config

# Update configuration
config.name = "MCP-API"
config.description = "API Integration MCP Server"

# Set API configuration
os.environ["API_BASE_URL"] = "https://api.example.com"
os.environ["API_KEY"] = "your-api-key"

# Create custom API tools if needed
```

## Advanced Features

### Using the Tool Registry

The tool registry provides a way to programmatically manage tools:

```python
from app import tool_registry

# Register a tool manually
def my_tool():
    return {"result": "success"}
    
tool_registry.register_tool(my_tool, "custom_name")

# Register a resource
def get_resource():
    return {"resource": "data"}
    
tool_registry.register_resource("resource://my_resource", get_resource)
```

### Creating Custom Resources

Resources in MCP provide a way to expose data to the client:

```python
from app import mcp

@mcp.resource("resource://my_data")
def get_my_data():
    """Provide custom data as a resource."""
    return {
        "key1": "value1",
        "key2": "value2"
    }
```

## Project Structure

```
mcp_skeleton/
├── app/                    # Main application package
│   ├── __init__.py         # Core framework code
│   ├── __main__.py         # Entry point
│   ├── tool_loader.py      # Dynamic tool loading
│   └── tools/              # Tool modules
│       ├── __init__.py     # Package initialization
│       ├── api_tools.py    # API integration tools
│       ├── http_tools.py   # HTTP request tools
│       └── web_tools.py    # Web navigation tools
├── tests/                  # Test directory
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── pyproject.toml          # Poetry configuration
└── README.md               # Documentation
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 