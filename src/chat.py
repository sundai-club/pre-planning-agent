from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from together_api import TogetherAI

app = FastAPI()


# Request and Response Models
class GetPlanRequest(BaseModel):
    user_intent: str


class GetPlanResponse(BaseModel):
    plan_option_1: str
    plan_option_2: str


class RefinePlanRequest(BaseModel):
    current_plan: str
    suggestion: str


class RefinePlanResponse(BaseModel):
    updated_plan: str


# Endpoint to generate two plan options
@app.post("/get_plan", response_model=GetPlanResponse)
def get_plan(request: GetPlanRequest):
    """
    Generate two JSON-based plan options based on the provided user intent.
    The plan output is structured for an agentic AI platform.
    """
    # Instantiate your LLM client (make sure your TogetherAI __init__ handles API keys appropriately)
    ai = TogetherAI()

    plan_prompt = (
        "You are a helpful planning assistant. We need to produce a plan in JSON format that an agentic AI platform can follow.\n"
        "Based on the following user intent, create a structured plan: \n\n"
        f"User Intent: {request.user_intent}\n\n"
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
        "- \"context\": object\n"
        "- \"tools\": array of objects (e.g., {\"type\": \"web_search\"} or {\"type\": \"file_search\")\n\n"
        "Make sure your JSON is well-formed and does not include extra commentary outside the JSON.\n"
    )

    # Generate two different plan options using different temperature values for variety.
    try:
        plan_option_1 = ai.generate(plan_prompt, temperature=0.2)
        plan_option_2 = ai.generate(plan_prompt, temperature=0.4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {e}")

    return GetPlanResponse(plan_option_1=plan_option_1, plan_option_2=plan_option_2)


# Endpoint to refine an existing plan based on a suggestion
@app.post("/refine_plan", response_model=RefinePlanResponse)
def refine_plan(request: RefinePlanRequest):
    """
    Refine a given JSON plan based on a user-provided suggestion.
    The returned plan maintains the structure required by the agentic AI platform.
    """
    ai = TogetherAI()

    refine_prompt = (
        "You are a helpful planning assistant. We have a current JSON plan and a user suggestion. "
        "Revise the plan accordingly, ensuring it remains valid JSON with the required keys:\n"
        "  - \"input\"\n"
        "  - \"requirements\" (array of objects with 'name' and 'description')\n"
        "  - \"context\" (object)\n"
        "  - \"tools\" (array of objects)\n\n"
        "Here is the current plan (JSON):\n"
        f"{request.current_plan}\n\n"
        "User Suggestion:\n"
        f"{request.suggestion}\n\n"
        "Return only valid JSON, no extra commentary."
    )

    try:
        updated_plan = ai.generate(refine_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {e}")

    return RefinePlanResponse(updated_plan=updated_plan)


# Optional: root endpoint for a simple health-check
@app.get("/")
def read_root():
    return {"message": "Agentic AI pre-planner API is running."}
