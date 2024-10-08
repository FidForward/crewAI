from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew import ClaygentCrew
import yaml
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Load tasks configuration
with open('config/tasks.yaml', 'r') as file:
    tasks_config = yaml.safe_load(file)

class TaskInput(BaseModel):
    task_name: str
    input_data: dict

@app.post("/run_task")
async def run_task(task_input: TaskInput):
    if task_input.task_name not in tasks_config:
        raise HTTPException(status_code=400, detail="Invalid task name")

    try:
        crew_instance = ClaygentCrew()
        results = crew_instance.run_task(task_input.task_name, task_input.input_data)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)