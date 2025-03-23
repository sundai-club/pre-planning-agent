import requests
import os
import json
from typing import List, Dict, Any, Optional
from together import Together

# Initialize the Together client for summarization
client = Together()

def parse_brave_search_results(search_results):
    # Parse the search results
    if search_results is None:
        return None
    results = search_results.get("web", {}).get("results", [])
    if len(results) == 0:
        return None
    print(f"Found {len(results)} results")
    return results

def brave_search(query, count=10):
    # Perform a search using the Brave Search API
    base_url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": os.getenv('BRAVE_API_KEY')
    }
    params = {
        "q": query,
        "count": count,
    }
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        return parse_brave_search_results(response.json()) if response.status_code == 200 else response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def extract_useful_info(results):
    # Extract useful information from the search results
    if not results:
        return []
    
    simplified = []
    for item in results:
        simplified.append({
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "url": item.get("url", ""),
        })
    return simplified

def summarize_results(query, search_results):
    
    if not search_results:
        return "No relevant information found."
    
    # Prepare the content to summarize
    content = f"Search Query: {query}\n\n"
    
    for i, result in enumerate(search_results, 1):
        content += f"Result {i}:\n"
        content += f"Title: {result['title']}\n"
        content += f"Description: {result['description']}\n"
        content += f"URL: {result['url']}\n\n"
    
    # Create the prompt for summarization
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes search results accurately and concisely."
        },
        {
            "role": "user",
            "content": f"""I need a concise and informative summary of these search results about: {query}
            
Please synthesize the key information into a coherent paragraph that captures the main points.

{content}

Your summary should be informative, balanced, and focused on the facts presented in these results."""
        }
    ]
    
    # Get the summary from the model
    try:
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.1",
            messages=messages,
            max_tokens=400,
            temperature=0.3
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
    
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error generating summary. Please check the search results directly."

def search_all_subqueries(subqueries, results_per_query=5):
    # Initialize a dictionary to store all results
    all_results = {}
    
    # Debug: Print the number of subqueries received
    print(f"Processing {len(subqueries)} subqueries")
    
    for i, query in enumerate(subqueries, 1):
        print(f"Processing subquery {i}/{len(subqueries)}: {query}")
        results = brave_search(query, count=results_per_query)
        
        if results:
            simplified_results = extract_useful_info(results)
            
            # Get the first relevant URL (for the paragraph format)
            first_url = simplified_results[0]['url'] if simplified_results else "No URL available"
            
            print(f"Summarizing results for: {query}")
            summary = summarize_results(query, simplified_results)
            
            # Use paragraph index as the key
            paragraph_key = f"paragraph_{i}"
            all_results[paragraph_key] = {
                "query": query,
                "url": first_url,
                "summary": summary
            }
        else:
            paragraph_key = f"paragraph_{i}"
            all_results[paragraph_key] = {
                "query": query,
                "url": "No results found",
                "summary": "No results found for this query."
            }
    
    # Debug: Print the number of results created
    print(f"Created {len(all_results)} result paragraphs")
    return all_results

def save_search_results(all_results, filename="search_results.json"):
    # Save the search results to a JSON file
   
    return json.dump(all_results, indent=2, ensure_ascii=False)
    # print(f"Results saved to {filename}")
    
    # return all_results