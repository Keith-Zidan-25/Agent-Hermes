import json
import requests
import os

def search_local_news(query: str) -> str:
    """Searches the public web for recent news articles, community posts, 
    and public reports related to specific local issues within a target area.

    This tool is the primary data ingestion source for the Harvester Agent, 
    designed to identify and gather raw text data about community problems 
    (e.g., crime, infrastructure failures, environmental issues).

    Args:
        query (str): The specific search phrase to execute. This should be 
                     highly targeted to the local area and issue type 
                     (e.g., "pothole reports in [City Name]" or 
                     "recent theft statistics [Neighborhood]").

    Returns:
        str: A JSON-formatted string containing a summarized list of the 
             top 5 relevant search results. Each result includes the 
             'title', a brief 'snippet' (summary), and the source 'link'.
             
             Example of the returned structure:
             [
                 {"title": "Local news title 1", "snippet": "A brief summary...", "link": "url1"},
                 {"title": "Local news title 2", "snippet": "Another summary...", "link": "url2"},
                 ...
             ]
             
    Raises:
        requests.exceptions.RequestException: If the API call fails or the response status is poor.
    """
    
    serper_api_key = os.getenv('SERPER_API_KEY')
    url = os.getenv('SERPER_URL')
    
    payload = json.dumps({"q": query}) 
    headers = {'X-API-KEY': serper_api_key, 'Content-Type': 'application/json'}

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
    except Exception as e:
        return f"Error calling API: {e}"

    snippets = []
    for result in data.get('organic', [])[:5]:
        snippet = {
            "title": result.get('title'),
            "snippet": result.get('snippet'),
            "link": result.get('link')
        }
        snippets.append(snippet)

    return json.dumps(snippets)