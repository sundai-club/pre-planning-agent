from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.schema import *
from src.chat import get_plan, refine_plan
from src.maestro_executor import execute_task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/get_plan", response_model=GetPlanResponse)
def get_plan_endpoint(request: GetPlanRequest):
    plan = get_plan(request.user_intent)
    return GetPlanResponse(**plan)

@app.post("/refine_plan", response_model=RefinePlanResponse)
async def refine_plan_endpoint(request: RefinePlanRequest):
    refined_plan = refine_plan(request.current_plan, request.suggestion)
    return RefinePlanResponse(**refined_plan)


@app.post("/execute_plan", response_model=PlanExecuteResponse)
async def execute_plan(request: PlanExecuteRequest):
    result = execute_task(request.plan)
    return PlanExecuteResponse(result=result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)