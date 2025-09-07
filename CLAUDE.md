# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a Python API for Printables.com with three main components:

1. **Core API (`printables_api.py`)** - Production-ready Python API that provides GraphQL-based access to Printables.com
2. **Test Scripts** - Individual test files demonstrating specific API functionality
3. **MCP Server Development** - Empty `printables-mcp/` directory for developing a Model Context Protocol server

## Architecture

### Core API Functions (`printables_api.py`)

- `search_models(search_term, limit)` - Searches Printables.com using GraphQL API
- `get_model_files(model_id)` - Retrieves downloadable files for a specific model
- `get_model_description(model_url)` - Scrapes model descriptions from web pages using cloudscraper

The API uses two different approaches:
- GraphQL API calls for structured data (search, file lists)
- Web scraping with cloudscraper for rich content (descriptions)

### Key Dependencies

- `requests` - HTTP requests to GraphQL API
- `cloudscraper` - Bypass Cloudflare protection for web scraping
- `beautifulsoup4` - HTML parsing for descriptions

### Test Structure

- `test_search.py` - Standalone search functionality test
- `test_downloads.py` - File listing and download URL generation
- `test_get_description.py` - Description scraping test

## Common Development Tasks

### Running the Main API
```bash
python printables_api.py "search_term" -l 10
```

### Running Individual Tests
```bash
python test_search.py
python test_downloads.py
python test_get_description.py
```

### MCP Server Development

**STATUS: COMPLETED** - The MCP server has been successfully developed and is located at `C:\Users\Cope\Documents\GitHub\printables-mcp-server`. 

The completed MCP server provides:
- FastMCP server setup with stdio transport
- Three main tools: `search_printables`, `get_printables_files`, `get_printables_description`
- Proper error handling and logging
- Model data formatting for MCP consumers

Reference implementation demonstrates:
- FastMCP server setup
- Async task management
- Tool registration patterns
- GraphQL API integration

### Dependencies Installation
```bash
pip install requests cloudscraper beautifulsoup4
```

For MCP server development, additional dependencies will be needed:
```bash
pip install mcp[cli]>=1.2.0 httpx>=0.25.0
```

## API Patterns

### GraphQL Query Structure
All GraphQL queries follow this pattern:
- Operation name and query definition
- Fragment definitions for reusable data structures  
- Variables for search parameters
- Error handling for API responses

### Rate Limiting
The main API includes `time.sleep(1)` between requests to be respectful to Printables.com servers.

### URL Construction
Model URLs follow the pattern: `https://www.printables.com/model/{model_id}-{model_slug}`
Download URLs: `https://www.printables.com/model/download/{file_id}`