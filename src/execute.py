import os
import json
import argparse
from query_decomposer import decompose_query
from web_search import search_all_subqueries, save_search_results

def decompose_and_search(query: str, num_subqueries: int = 5, results_per_query: int = 3, output: str = "search_results.json"):

    # Set up argument parser
    # parser = argparse.ArgumentParser(description="Decompose complex queries, perform web searches, and summarize results")
    # parser.add_argument("--query", type=str, help="Complex query to decompose and search")
    # parser.add_argument("--num-subqueries", type=int, default=5, help="Number of sub-queries to generate")
    # parser.add_argument("--results-per-query", type=int, default=3, help="Number of search results per sub-query")
    # parser.add_argument("--output", type=str, default="search_results.json", help="Output JSON file for search results")
    
    # args = parser.parse_args()
    
    # Get the query from command line or user input
    # query = args.query
    if not query:
        query = input("Enter your complex query: ")
    
    # Step 1: Decompose the query
    print("\nDecomposing query...")
    subqueries = decompose_query(query=query, num_subqueries=num_subqueries)
    
    # Debug: Print the subqueries to verify we're getting multiple queries
    print("\nGenerated search terms:")
    for i, sub_query in enumerate(subqueries, 1):
        print(f"{i}. {sub_query}")
    
    # Debug: Verify the subqueries list structure
    print(f"\nType of subqueries: {type(subqueries)}")
    print(f"Number of subqueries: {len(subqueries)}")
    
    # Step 2: Search using each subquery and summarize results
    print("\nPerforming searches and generating summaries...")
    search_results = search_all_subqueries(subqueries, results_per_query=results_per_query)
    
    # Debug: Verify the search results structure
    print(f"\nType of search_results: {type(search_results)}")
    print(f"Number of keys in search_results: {len(search_results)}")
    print(f"Keys in search_results: {list(search_results.keys())}")
    
    # Step 3: Save results to JSON
    # save_search_results(search_results, output)
    
    # Step 4: Summary and display sample of the JSON output
    print("\nSearch and summarization process complete!")
    print(f"- Original query: {query}")
    print(f"- Decomposed into {len(subqueries)} search terms")
    # print(f"- JSON results saved to {args.output}")
    
    # Print the full JSON output structure (for debugging)
    # print("\nFull JSON output structure:")
    return json.dumps(search_results, indent=2)

if __name__ == "__main__":
    # Check for environment variables
    if not os.getenv('TOGETHER_API_KEY'):
        print("Warning: TOGETHER_API_KEY environment variable is not set")
    
    if not os.getenv('BRAVE_API_KEY'):
        print("Warning: BRAVE_API_KEY environment variable is not set")
    
