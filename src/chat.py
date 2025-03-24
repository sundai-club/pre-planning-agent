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
        
    

    plan_prompt ="""You are a helpful planning assistant. We need to produce a plan in JSON format that an agentic AI platform can follow.
        Based on the following user intent, create a structured plan: 
        User Intent: {user_intent}
        Web search results: {search_results}

        Decompose the user intent carefully and create a step by step list of requirements and constraints that should be followed by the agentic system in a step wise manner.
        The final plan should be a valid JSON plan that can be executed by the agentic AI platform in the following format:
        You only have access to one tool: web_search

        ```json
            {{"input" : "input",
            "requirements" : "[{{"name" : "name", "description" : "description", "is_mandatory" : "true"}}, {{"name" : "name", "description" : "description", "is_mandatory" : "true"}}]",
            "tools" : "[{{"type" : "type"}}]",
            "is_mandatory" : "true"
            }}
        ```

        Output:
        """.format(user_intent=user_intent, search_results=search_results)

    # Generate two different plan options using different temperature values for variety.
    try:
        plan_option_1 = ai.generate(plan_prompt, temperature=0.2)
        plan_option_2 = ai.generate(plan_prompt, temperature=0.4)
        plan_option_1 = parse_response(plan_option_1)
        plan_option_2 = parse_response(plan_option_2)
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
    In case the user asks to add a new requirement, do not modify the existing requirements.
    ```json
        {{"input" : "input",
        "requirements" : "[{{"name" : "name", "description" : "description", "is_mandatory" : "true"}}]",
        "tools" : "[{{"type" : "type"}}]",
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
