from src.together_api import TogetherAI
from src.intent_classifier import get_intent
from src.execute import decompose_and_search
from src.maestro_executor import execute_task
from fastapi import HTTPException
from src.utils import parse_response

# Endpoint to generate two plan options
def get_plan(user_intent: str):
    """
    Generate two JSON-based plan options based on the provided user intent.
    The plan output is structured for an agentic AI platform.
    """
    # Instantiate your LLM client (make sure your TogetherAI __init__ handles API keys appropriately)
    ai = TogetherAI()

    # Classify the intent to do a web search
    intent = get_intent(user_intent)
    search_results = ""
    if intent.get("web_search"):
        # Decompose the query and perform web searches
        search_results = decompose_and_search(user_intent)
        
    

    plan_prompt = (
        "You are a helpful planning assistant. We need to produce a plan in JSON format that an agentic AI platform can follow.\n"
        "Based on the following user intent, create a structured plan: \n\n"
        f"User Intent: {user_intent}\n\n"
        f"Web search results: {search_results}\n\n"
        "The final call to the agentic AI might look like this:\n\n"
        "  run = client.beta.maestro.runs.create_and_poll(\n"
        "      input=\"Write a poem about hackathons\",\n"
        "      requirements=[\n"
        "          {\n"
        "              \"name\": \"length requirement\",\n"
        "              \"description\": \"The length of the poem should be exactly 5 lines\"\n"
        "          }\n"
        "      ],\n"
        "      context={\"text\": \"Psyduck is the best pokemon\"},\n"
        "      tools=[{\"type\": \"web_search\"}]\n"
        "  )\n\n"
        "Please provide a plan in **valid JSON** with the following keys:\n"
        "- \"input\": string\n"
        "- \"requirements\": array of objects with \"name\" and \"description\"\n"
        "- \"tools\": {\"type\": \"web_search\"} "
        "Make sure your JSON is well-formed and does not include extra commentary outside the JSON.\n"
    )

    # Generate two different plan options using different temperature values for variety.
    try:
        plan_option_1 = ai.generate(plan_prompt, temperature=0.2)
        plan_option_2 = ai.generate(plan_prompt, temperature=0.4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {e}")

    return {"plan_option_1": plan_option_1, "plan_option_2": plan_option_2}


# Endpoint to refine an existing plan based on a suggestion
def refine_plan(current_plan: str, suggestion: str):
    """
    Refine a given JSON plan based on a user-provided suggestion.
    The returned plan maintains the structure required by the agentic AI platform.
    """
    ai = TogetherAI()

    refine_prompt = """
    You are a helpful planning assistant. We have a current JSON plan and a user suggestion.
    Revise the plan accordingly, ensuring it remains valid JSON with the required keys:
    ```json
        {{"input" : "input",
        "requirements" : "[{{"name" : "name", "description" : "description"}}]",
        "tools" : "[{{"type" : "type"}}]"
        }}
    ```
    Here is the current plan (JSON):

    {current_plan}
    
    User Suggestion:
    
    {suggestion}
    
    Return only valid JSON, no extra commentary.
    Output:
    """.format(current_plan=current_plan, suggestion=suggestion)
    

    try:
        updated_plan = ai.generate(refine_prompt)
        updated_plan = parse_response(updated_plan)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {e}")

    return {"updated_plan": updated_plan}
