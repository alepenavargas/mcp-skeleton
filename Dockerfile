FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry==1.7.1

# Copy project files
COPY pyproject.toml ./
COPY app/ ./app/

# Configure Poetry to not use virtual environments in Docker
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Expose the default port
EXPOSE 9090

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MCP_NAME="MCP-Skeleton"
ENV MCP_DESCRIPTION="MCP Skeleton Server"
ENV MCP_PORT=9090
ENV MCP_LOG_LEVEL=INFO

# Run the MCP server
CMD ["python", "-m", "app"] 