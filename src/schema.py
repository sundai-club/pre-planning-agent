from pydantic import BaseModel

class GetPlanRequest(BaseModel):
    user_intent: str

class GetPlanResponse(BaseModel):
    plan_option_1: str
    plan_option_2: str

class RefinePlanRequest(BaseModel):
    current_plan: str
    suggestion: str


class RefinePlanResponse(BaseModel):
    updated_plan: dict

class PlanExecuteRequest(BaseModel):
    plan: dict

class PlanExecuteResponse(BaseModel):
    result: str