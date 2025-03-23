import os
from together import Together

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
            "content": f"""Decompose the following query into exactly {num_subqueries} atomic search terms.

Guidelines:
- Create search terms, not questions (avoid words like "what", "how", "why")
- Each search term should focus on ONE specific aspect only
- Use concise, keyword-focused language optimized for search engines
- Avoid conjunctions (and, or, but) within each search term
- Format each search term on a new line with a dash
- Ensure all search terms together cover all aspects of the original query

Query to decompose:
{query}"""
        }
    ]
    
    # Use Together's Chat Completion endpoint
    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.1",  # Lightweight, chat-capable model
        messages=messages,
        max_tokens=300,  # Increased token limit to accommodate responses
        temperature=0.5,  # Moderate temperature for consistent but varied responses
        top_p=0.9
    )
    
    # Extract response content
    content = response.choices[0].message.content
    sub_queries = [line.strip("- ").strip() for line in content.strip().splitlines() if line.strip()]
    
    # Ensure we get exactly the number of sub-queries requested
    if len(sub_queries) < num_subqueries:
        print(f"Warning: Model returned fewer than {num_subqueries} sub-queries. You may need to adjust the prompt or model parameters.")
    elif len(sub_queries) > num_subqueries:
        print(f"Warning: Model returned more than {num_subqueries} sub-queries. Using only the first {num_subqueries}.")
        sub_queries = sub_queries[:num_subqueries]
    
    # Post-process to ensure queries are search-optimized
    optimized_queries = []
    for q in sub_queries:
        # Remove question marks
        q = q.replace("?", "")
        # Remove question words at the beginning
        question_words = ["what", "how", "why", "when", "where", "who", "which", "can", "does", "is", "are"]
        for word in question_words:
            if q.lower().startswith(word + " "):
                q = q[len(word)+1:]
        # Trim and capitalize first letter if needed
        q = q.strip()
        if q and not q[0].isupper() and q[0].isalpha():
            q = q[0].upper() + q[1:]
        optimized_queries.append(q)
    
    return optimized_queries