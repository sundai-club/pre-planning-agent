import os
from together import Together
from src.utils import parse_response

# Initialize the Together client
client = Together()

def decompose_query(query, num_subqueries=5):
    # Build the chat prompt properly with updated instructions for web search
    messages = [
        {
            "role": "system",
            "content": "You are a specialized tool that breaks down complex user queries into atomic search terms optimized for web search engines."
        },
        {
            "role": "user",
            "content": """Decompose the following query into exactly {num_subqueries} atomic search terms.

Guidelines:
- Create search terms, not questions (avoid words like "what", "how", "why")
- Each search term should focus on ONE specific aspect only
- Use concise, keyword-focused language optimized for search engines
- Avoid conjunctions (and, or, but) within each search term
- Format each search term on a new line with a dash
- Ensure all search terms together cover all aspects of the original query
- Should be plain text

Query to decompose:
{query}

Provide your response in the following format: 

```json
{{
    "search_queries": "["query1", "query2", "query3"]"
}}
```

Output:""".format(num_subqueries=num_subqueries, query=query)
        }
    ]
    
    # Use Together's Chat Completion endpoint
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=messages,
        max_tokens=2048,  
    )
    
    # Extract response content
    content = response.choices[0].message.content
    print(content)
    sub_queries = parse_response(content)["search_queries"]

    print(sub_queries)
    
    sub_queries = sub_queries[:num_subqueries]
    
    optimized_queries = []
    for q in sub_queries:
        q = q.replace("?", "")
        question_words = ["what", "how", "why", "when", "where", "who", "which", "can", "does", "is", "are"]
        for word in question_words:
            if q.lower().startswith(word + " "):
                q = q[len(word)+1:]
        q = q.strip()
        if q and not q[0].isupper() and q[0].isalpha():
            q = q[0].upper() + q[1:]
        optimized_queries.append(q)
    
    return optimized_queries
