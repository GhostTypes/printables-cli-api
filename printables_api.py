import requests
import cloudscraper
from bs4 import BeautifulSoup, NavigableString
import json
import argparse
import time


def search_models(search_term: str, limit: int = 5, ordering: str = "best_match", debug: bool = False):
    """
    Searches Printables.com for models using the GraphQL API.
    
    Args:
        search_term: The search query
        limit: Maximum number of results to return
        ordering: Search ordering - one of: "best_match", "popular", "latest", "rating", "makes_count"
        debug: Enable debug output
    """
    api_url = "https://api.printables.com/graphql/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    
    query = """
    query SearchModels($query: String!, $limit: Int, $ordering: SearchChoicesEnum) {
      result: searchPrints2(query: $query, printType: print, limit: $limit, ordering: $ordering) {
        items { ...Model __typename }
      }
    }
    fragment AvatarUser on UserType { id handle publicUsername __typename }
    fragment Model on PrintType { 
        id name slug ratingAvg likesCount downloadCount datePublished 
        user { ...AvatarUser __typename } 
        image { filePath } 
        __typename 
    }
    """
    # Validate ordering parameter
    valid_orderings = ["best_match", "popular", "latest", "rating", "makes_count"]
    if ordering not in valid_orderings:
        raise ValueError(f"Invalid ordering '{ordering}'. Must be one of: {', '.join(valid_orderings)}")
    
    variables = {"query": search_term, "limit": limit, "ordering": ordering}
    payload = {"operationName": "SearchModels", "query": query, "variables": variables}
    
    if debug:
        print(f"Searching for '{search_term}' (limit: {limit}, ordering: {ordering})...")
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and data.get('data').get('result'):
            return data['data']['result']['items']
    except requests.exceptions.RequestException as e:
        print(f"Request failed during search: {e}")
    return []

def get_real_download_url(file_id: str, model_id: str, file_type: str, debug: bool = False):
    """
    Performs the GetDownloadLink mutation to get a temporary direct download URL.
    """
    api_url = "https://api.printables.com/graphql/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

    query = """
    mutation GetDownloadLink($id: ID!, $modelId: ID!, $fileType: DownloadFileTypeEnum!, $source: DownloadSourceEnum!) {
      getDownloadLink(id: $id, printId: $modelId, fileType: $fileType, source: $source) {
        ok
        errors {
          ...Error
          __typename
        }
        output {
          link
          count
          ttl
          __typename
        }
        __typename
      }
    }
    fragment Error on ErrorType {
      field
      messages
      __typename
    }
    """
    variables = {"id": file_id, "modelId": model_id, "fileType": file_type, "source": "model_detail"}
    payload = {"operationName": "GetDownloadLink", "query": query, "variables": variables}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if debug:
            print(f"    -> GraphQL response for file {file_id}: {data}")
        
        if 'data' in data:
            download_data = data['data'].get('getDownloadLink')
            if download_data:
                if download_data.get('ok') and download_data.get('output', {}).get('link'):
                    return download_data['output']['link']
                elif download_data.get('errors'):
                    if debug:
                        print(f"    -> GraphQL errors for file {file_id}: {download_data['errors']}")
                else:
                    if debug:
                        print(f"    -> No valid download link returned for file {file_id}")
        elif 'errors' in data:
            if debug:
                print(f"    -> GraphQL query errors for file {file_id}: {data['errors']}")
            
    except requests.exceptions.RequestException as e:
        if debug:
            print(f"    -> Request failed for file ID {file_id}: {e}")
    return None

def get_model_files(model_id_str: str, debug: bool = False):
    """
    Fetches the file list and then gets the real download URL for each file.
    """
    api_url = "https://api.printables.com/graphql/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    
    operation_name = "ModelFiles"
    graphql_query = """
    query ModelFiles($id: ID!) {
      model: print(id: $id) {
        id
        filesType
        gcodes { ...GcodeDetail __typename }
        stls { ...StlDetail __typename }
        slas { ...SlaDetail __typename }
        otherFiles { ...OtherFileDetail __typename }
        __typename
      }
    }
    fragment GcodeDetail on GCodeType { id created name folder note printer { id name __typename } excludeFromTotalSum printDuration layerHeight nozzleDiameter material { id name __typename } weight fileSize filePreviewPath rawDataPrinter order __typename }
    fragment OtherFileDetail on OtherFileType { id created name folder note fileSize filePreviewPath order __typename }
    fragment SlaDetail on SLAType { id created name folder note expTime firstExpTime printer { id name __typename } printDuration layerHeight usedMaterial fileSize filePreviewPath order __typename }
    fragment StlDetail on STLType { id created name folder note fileSize filePreviewPath order __typename }
    """
    variables = {"id": model_id_str}
    payload = {"operationName": operation_name, "query": graphql_query, "variables": variables}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and data.get('data', {}).get('model'):
            model_files = data['data']['model']
            all_files_with_links = []
            
            supported_file_types = {'stls': 'stl', 'gcodes': 'gcode'} 
            unsupported_file_types = {'slas': 'sla', 'otherFiles': 'other'}
            
            for list_name, api_type in supported_file_types.items():
                if model_files.get(list_name):
                    for file_item in model_files[list_name]:
                        file_id = file_item.get('id')
                        file_name = file_item.get('name')
                        if debug:
                            print(f"    -> Fetching download link for: {file_name}")
                        
                        real_url = get_real_download_url(file_id, model_id_str, api_type, debug)
                        all_files_with_links.append({
                            "name": file_name,
                            "download_url": real_url,
                            "size_bytes": file_item.get('fileSize'),
                            "file_type": api_type
                        })
                        time.sleep(0.5)
            
            # Log "unsupported" file types found (for future implementation/testing)
            for list_name in unsupported_file_types:
                if model_files.get(list_name):
                    count = len(model_files[list_name])
                    if debug:
                        print(f"    -> Found {count} {list_name} files (not yet supported)")
            return all_files_with_links
    except requests.exceptions.RequestException as e:
        print(f"Request failed fetching file list for model {model_id_str}: {e}")
    return []

def get_model_description(model_url: str, debug: bool = False):
    """
    Scrapes and cleans the model description from its page using cloudscraper.
    """
    if debug:
        print(f"    -> Fetching description from: {model_url}")
    
    # Add retry logic for network issues
    max_retries = 3
    for attempt in range(max_retries):
        try:
            scraper = cloudscraper.create_scraper(browser='chrome',delay=1,)
            
            response = scraper.get(model_url, timeout=20)  # Increased timeout
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            description_div = soup.find('div', class_='user-inserted')
            
            if not description_div: 
                return "Description not found on this page."
            
            content_container = description_div.find('body') or description_div

            clean_description = []
            for tag in content_container.find_all(['h3', 'p']):
                if tag.name == 'h3':
                    clean_description.append(f"\n## {tag.get_text(strip=True)}")
                elif tag.name == 'p':
                    p_parts = [item.string if isinstance(item, NavigableString) else f"[{item.get_text(strip=True)}]({item.get('href', '')})" if item.name == 'a' else "\n" if item.name == 'br' else '' for item in tag.contents]
                    clean_description.append("".join(filter(None, p_parts)).strip())
            
            description_text = "\n".join(clean_description)
            if debug:
                print(f"    -> Description fetched successfully ({len(description_text)} characters)")
            return description_text
            
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            if debug:
                print(f"    -> Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))  # Exponential backoff
                continue
        except requests.exceptions.RequestException as e:
            if debug:
                print(f"    -> Request error on attempt {attempt + 1}: {e}")
            return f"Error: Could not fetch model page after {attempt + 1} attempts. {e}"
        except Exception as e:
            if debug:
                print(f"    -> Unexpected error: {e}")
            return f"Error: Failed to parse model page. {e}"
    
    return f"Error: Could not fetch model page after {max_retries} attempts due to network issues."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Printables.com and fetch model data.")
    parser.add_argument("search_term", type=str, help="The term to search for.")
    parser.add_argument("-l", "--limit", type=int, default=5, help="Number of results to fetch (default: 5).")
    parser.add_argument("-o", "--ordering", type=str, default="best_match", 
                       choices=["best_match", "popular", "latest", "rating", "makes_count"],
                       help="Search ordering (default: best_match).")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output for detailed logging.")
    args = parser.parse_args()

    search_results = search_models(args.search_term, args.limit, args.ordering, args.debug)
    
    if not search_results:
        print("No models found. Exiting.")
        exit()

    all_models_data = {}
    if args.debug:
        print(f"\nFound {len(search_results)} models. Fetching details for each...")

    for i, model in enumerate(search_results):
        model_id_str = model.get('id')
        if not model_id_str: continue
        
        model_slug = model.get('slug')
        model_url = f"https://www.printables.com/model/{model_id_str}-{model_slug}"
        
        if args.debug:
            print(f"({i+1}/{len(search_results)}) Processing: {model.get('name')} ({model_url})")
        
        main_image_url = None
        if (image_info := model.get('image')) and image_info.get('filePath'):
            main_image_url = "https://media.printables.com/" + image_info['filePath']
            
        description = get_model_description(model_url, args.debug)
        files = get_model_files(model_id_str, args.debug)
        
        all_models_data[model_id_str] = {
            "name": model.get('name'),
            "url": model_url,
            "main_image_url": main_image_url,
            "author": model.get('user', {}).get('publicUsername'),
            "stats": {
                "likes": model.get('likesCount'),
                "downloads": model.get('downloadCount'),
                "rating": model.get('ratingAvg'),
                "published_date": model.get('datePublished')
            },
            "description": description,
            "files": files,
        }
        time.sleep(1)

    output_filename = f"{args.search_term.replace(' ', '_')}_results.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(all_models_data, f, ensure_ascii=False, indent=4)
        
    print(f"\nDone! All data saved to {output_filename}")
