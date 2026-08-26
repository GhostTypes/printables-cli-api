<div align="center">
  <h1>Printables CLI API</h1>
  <p>A command-line utility to search for 3D models on printables.com and export their detailed information to a JSON file</p>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/github/stars/GhostTypes/printables-cli-api?style=for-the-badge">
</p>

---

<div align="center">
  <h2>Core Features</h2>
</div>

<div align="center">
<table>
  <tr>
    <th>Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Model Search</td>
    <td>Executes a search on Printables.com using its GraphQL API to find relevant models based on a keyword.</td>
  </tr>
  <tr>
    <td>Detailed Data Retrieval</td>
    <td>Scrapes the model's public page for detailed descriptions and fetches metadata like author, likes, and download counts via API.</td>
  </tr>
  <tr>
    <td>Download Link Generation</td>
    <td>Retrieves a list of all associated files (STL, G-Code) and generates temporary direct download links for each one.</td>
  </tr>
  <tr>
    <td>JSON Data Export</td>
    <td>Aggregates all collected information into a well-structured JSON file for easy parsing and use in other applications.</td>
  </tr>
</table>
</div>

---

<div align="center">
  <h2>Model Search</h2>
</div>

<p align="center">
This tool allows for precise searching of the Printables.com model database directly from the command line.
</p>

<div align="center">
<table>
  <tr>
    <th>Sub-Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Keyword Search</td>
    <td>Allows users to specify any search term to find matching models.</td>
  </tr>
  <tr>
    <td>Result Limiting</td>
    <td>Provides a command-line argument to limit the number of results to process.</td>
  </tr>
</table>
</div>

---

<div align="center">
  <h2>Detailed Data Retrieval</h2>
</div>

<p align="center">
The script gathers comprehensive information for each model found, combining API data with web scraping.
</p>

<div align="center">
<table>
  <tr>
    <th>Sub-Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Description Scraping</td>
    <td>Utilizes cloudscraper to parse the complete model description, including headers and links, from its HTML page.</td>
  </tr>
  <tr>
    <td>Metadata Fetching</td>
    <td>Retrieves key statistics including likes, downloads, average rating, and publication date via the GraphQL API.</td>
  </tr>
  <tr>
    <td>Author Information</td>
    <td>Captures the public username of the model's creator.</td>
  </tr>
  <tr>
    <td>Main Image URL</td>
    <td>Extracts the URL for the model's primary image.</td>
  </tr>
</table>
</div>

---

<div align="center">
  <h2>Download Link Generation</h2>
</div>

<p align="center">
For each model, the script identifies all downloadable files and obtains direct access links.
</p>

<div align="center">
<table>
  <tr>
    <th>Sub-Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>File Manifest</td>
    <td>Fetches a complete list of files associated with a model, specifically supporting STL and G-Code types.</td>
  </tr>
  <tr>
    <td>Direct URL Generation</td>
    <td>Interacts with the GraphQL API to generate a temporary, direct download URL for each individual file.</td>
  </tr>
</table>
</div>

---

<div align="center">
  <h2>JSON Data Export</h2>
</div>

<p align="center">
All retrieved data is saved locally in a clean, machine-readable format.
</p>

<div align="center">
<table>
  <tr>
    <th>Sub-Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Structured Output</td>
    <td>Organizes all fetched data, including metadata, description, and file lists, into a single JSON object per model.</td>
  </tr>
  <tr>
    <td>File Naming</td>
    <td>Automatically names the output file based on the initial search term (e.g., search_term_results.json).</td>
  </tr>
</table>
</div>

---

<div align="center">
  <h2>Getting Started</h2>
</div>

<p align="center">
Follow these instructions to set up and run the project on your local machine.
</p>

<div align="center">

### Prerequisites

  - Python 3.8+
  - pip (Python package installer)

</div>

---

<div align="center">
  <h2>Installation</h2>
</div>

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
    ```

---

## What's new

- Gallery image scraping: the script now scrapes all images from a model's page (cover + gallery) and includes them in the JSON output under the image_urls key. The API-provided cover image remains available as main_image_url; if the API cover is missing, the first scraped image is used as a fallback.

- Example JSON keys added:

```json
"main_image_url": "https://media.printables.com/..",
"image_urls": [
  "https://media.printables.com/..",
  "https://media.printables.com/.."
]
```

These changes improve the richness of output and make it easier to download or preview all images associated with a model.

---

## Contributors

- Jacob Robertson (https://github.com/JacRob32)

If you'd like to add additional contributors, fork the repo and open a PR.

