from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from claygent.crew import ClaygentCrew
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Load tasks configuration
with open('config/tasks.yaml', 'r') as file:
    tasks_config = yaml.safe_load(file)

class LinkedInScraperInput(BaseModel):
    full_name: str
    company: str
    email: str

class EmployeeScraperInput(BaseModel):
    company: str
    full_name: str
    email: str

@app.post("/linkedin_scraper")
async def linkedin_scraper(input_data: LinkedInScraperInput):
    try:
        crew_instance = ClaygentCrew()
        result = crew_instance.run_task("linkedin_scraper", input_data.dict())
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/employee_scraper")
async def employee_scraper(input_data: EmployeeScraperInput):
    try:
        crew_instance = ClaygentCrew()
        result = crew_instance.run_task("employee_scraper", input_data.dict())
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)