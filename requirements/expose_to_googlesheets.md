# Requirement overview
I want to expose the current claygent/src/claygent app into a Google Sheets function.

# Feature requirements
- Using either FastAPI or Flask (whatever is better for this case)
- Take into account the structure of the folders of this CrewAI implementation (https://github.com/crewAIInc/crewAI)
- There is already some code available that does the same thing in https://github.com/kno2gether/crewai-examples/tree/8fb8aad307ce7d25de841bbb977771a078f399ca/stock_analysis. You can see its main.py and /static and /templates folder for the specifics on implementing FastAPI on it
- The input for exposed endpoint should be the inputs needed for claygent/src/claygent/config/tasks.yaml

# Relevant docs

## main.py sample with Fast API
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from datetime import datetime
import os
from crewai import Crew
from textwrap import dedent
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()


from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
templates = Jinja2Templates(directory="templates")
analysis_status = {} 
app.mount("/static", StaticFiles(directory="static"), name="static")

class CompanyData(BaseModel):
    company: str


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/status/{company}")
async def get_status(company: str):
    status = analysis_status.get(company, "Not Started")
    return {"status": status}

@app.get("/result/{company}")
async def get_result(company: str):
    safe_company_name = "".join(x for x in company if x.isalnum())
    filename = f"{safe_company_name}_latest.txt"  # Assuming you save it with this pattern
    if os.path.exists(filename):
        with open(filename, "r") as file:
            content = file.read()
        return {"result": content}
    return {"result": "Analysis not complete or file not found"}

@app.post("/analyze/")
async def analyze_company(company_data: CompanyData, background_tasks: BackgroundTasks):
    # Immediate response to user
    company = company_data.company
    message = f"I've started the agent to work on {company}"

    # Add the actual work to background tasks
    background_tasks.add_task(run_analysis, company)

    return {"message": message}

async def run_analysis(company):
    analysis_status[company] = "In Progress"
    try:
        financial_crew = FinancialCrew(company)
        result = financial_crew.run()

        # Ensure valid filename and handle file writing appropriately
        safe_company_name = "".join(x for x in company if x.isalnum())
        filename = f"{safe_company_name}_latest.txt"

        # Consider using an async file writer if you're handling large files or a high load
        with open(filename, "w") as file:
            file.write(result)
        analysis_status[company] = "Complete"

    except Exception as e:
        # Add logging or more sophisticated error handling here
        print(f"An error occurred: {e}")

class FinancialCrew:
  def __init__(self, company):
    self.company = company

  def run(self):
    agents = StockAnalysisAgents()
    tasks = StockAnalysisTasks()

    research_analyst_agent = agents.research_analyst()
    financial_analyst_agent = agents.financial_analyst()
    investment_advisor_agent = agents.investment_advisor()

    research_task = tasks.research(research_analyst_agent, self.company)
    financial_task = tasks.financial_analysis(financial_analyst_agent)
    filings_task = tasks.filings_analysis(financial_analyst_agent)
    recommend_task = tasks.recommend(investment_advisor_agent)

    crew = Crew(
      agents=[
        research_analyst_agent,
        financial_analyst_agent,
        investment_advisor_agent
      ],
      tasks=[
        research_task,
        financial_task,
        filings_task,
        recommend_task
      ],
      verbose=True
    )

    result = crew.kickoff()
    return result

# Current file structure
CREWAI/
├── .cache/
├── .github/
├── .venv/
├── .vscode/
├── claygent/
│   └── src/
│       └── claygent/
│           ├── __pycache__/
│           ├── config/
│           │   ├── agents.yaml
│           │   └── tasks.yaml
│           ├── tools/
│           │   └── __init__.py
│           ├── __init__.py
│           ├── crew.py
│           └── main.py
├── docs/
├── requirements/
│   └── expose_to_go.txt
├── src/
├── tests/
├── .editorconfig
├── .gitignore
├── .pre-commit-config.yaml
├── crewAI.excalidraw
├── LICENSE
├── mkdocs.yml
├── poetry.lock
└── pyproject.toml