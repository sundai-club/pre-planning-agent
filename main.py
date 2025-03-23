from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/get_plan")
async def get_plan(user_task: str):
    return {"plan": "plan"}

@app.get("/refine_plan")
async def refine_plan(plan: str):
    return {"refined_plan": "refined_plan"}


@app.get("/execute_plan")
async def execute_plan(refined_plan: str):
    return {"result": "result"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)