from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .crew import ClaygentCrew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

class LinkedInScraperInput(BaseModel):
    full_name: str
    company: str
    email: str

class EmployeeScraperInput(BaseModel):
    company: str
    company_url: str
    ceo_name: str

class LanguageDetectorInput(BaseModel):
    full_name: str
    company: str
    email: str

@app.post("/linkedin_scraper")
async def linkedin_scraper(input_data: LinkedInScraperInput):
    try:
        crew_instance = ClaygentCrew()
        result = crew_instance.run_linkedin_scraper(input_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/employee_scraper")
async def employee_scraper(input_data: EmployeeScraperInput):
    try:
        crew_instance = ClaygentCrew()
        result = crew_instance.run_employee_scraper(input_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/language_detector")
async def language_detector(input_data: LanguageDetectorInput):
    try:
        crew_instance = ClaygentCrew()
        result = crew_instance.run_language_detector(input_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)