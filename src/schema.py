from pydantic import BaseModel

class GetPlanRequest(BaseModel):
    user_intent: str

class GetPlanResponse(BaseModel):
    plan_option_1: dict
    plan_option_2: dict

class RefinePlanRequest(BaseModel):
    current_plan: dict
    suggestion: str


class RefinePlanResponse(BaseModel):
    updated_plan: dict

class PlanExecuteRequest(BaseModel):
    plan: dict

class PlanExecuteResponse(BaseModel):
    result: str