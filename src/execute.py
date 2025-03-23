import os
import json
import argparse
from src.query_decomposer import decompose_query
from src.web_search import search_all_subqueries

def decompose_and_search(query: str, num_subqueries: int = 5, results_per_query: int = 3, output: str = "search_results.json"):

    if not query:
        query = input("Enter your complex query: ")
    
    subqueries = decompose_query(query=query, num_subqueries=num_subqueries)
    search_results = search_all_subqueries(subqueries, results_per_query=results_per_query)
        
    return json.dumps(search_results, indent=2)