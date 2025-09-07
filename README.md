# Printables CLI API

A command-line utility to search for 3D models on printables.com and export their detailed information to a JSON file 📂.

## 🎯 Core Features

| Feature                    | Description                                                                                                                   |
| :------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| Model Search               | Executes a search on Printables.com using its GraphQL API to find relevant models based on a keyword.                           |
| Detailed Data Retrieval    | Scrapes the model's public page for detailed descriptions and fetches metadata like author, likes, and download counts via API. |
| Download Link Generation   | Retrieves a list of all associated files (STL, G-Code) and generates temporary direct download links for each one.            |
| JSON Data Export           | Aggregates all collected information into a well-structured JSON file for easy parsing and use in other applications.           |

## 🔎 Model Search

This tool allows for precise searching of the Printables.com model database directly from the command line.

| Sub-Feature         | Description                                                                 |
| :------------------ | :-------------------------------------------------------------------------- |
| Keyword Search      | Allows users to specify any search term to find matching models.            |
| Result Limiting     | Provides a command-line argument to limit the number of results to process. |

## 📊 Detailed Data Retrieval

The script gathers comprehensive information for each model found, combining API data with web scraping.

| Sub-Feature           | Description                                                                                                    |
| :-------------------- | :------------------------------------------------------------------------------------------------------------- |
| Description Scraping  | Utilizes `cloudscraper` to parse the complete model description, including headers and links, from its HTML page. |
| Metadata Fetching     | Retrieves key statistics including likes, downloads, average rating, and publication date via the GraphQL API. |
| Author Information    | Captures the public username of the model's creator.                                                            |
| Main Image URL        | Extracts the URL for the model's primary image.                                                                 |

## 🔗 Download Link Generation

For each model, the script identifies all downloadable files and obtains direct access links.

| Sub-Feature           | Description                                                                                             |
| :-------------------- | :------------------------------------------------------------------------------------------------------ |
| File Manifest         | Fetches a complete list of files associated with a model, specifically supporting STL and G-Code types. |
| Direct URL Generation | Interacts with the GraphQL API to generate a temporary, direct download URL for each individual file.   |

## 💾 JSON Data Export

All retrieved data is saved locally in a clean, machine-readable format.

| Sub-Feature       | Description                                                                                                    |
| :---------------- | :------------------------------------------------------------------------------------------------------------- |
| Structured Output | Organizes all fetched data, including metadata, description, and file lists, into a single JSON object per model. |
| File Naming       | Automatically names the output file based on the initial search term (e.g., `search_term_results.json`).       |

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

  - Python 3.8+
  - pip (Python package installer)

### Installation

1.  Clone the repository (replace with your actual repository URL)

    ```bash
    git clone https://github.com/GhostTypes/printables-cli-api.git
    ```

2.  Navigate to the project directory

    ```bash
    cd printables-cli-api
    ```

3.  Install the required dependencies

    ```bash
    pip install requests cloudscraper beautifulsoup4
    ```

4.  Run the script with a search term

    ```bash
    # Basic usage: search for "Calibration Cube" and fetch the top 5 results
    python printables_api.py "Calibration Cube"

    # Advanced usage: search for "Benchy", limit to 3 results, and enable debug output
    python printables_api.py "Benchy" --limit 3 --debug
