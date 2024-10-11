#!/usr/bin/env python
from .crew import ClaygentCrew
from .api import app
import sys

def run():
    """
    Run the crew for LinkedIn, employee scraping, language detection, and HR detection.
    """
    inputs = {
        'full_name': 'Afonso Pinheiro',
        'company': 'Pleez',
        'email': 'afonso.pinheiro@trypleez.com',
        'ceo_name': 'Afonso Pinheiro',
        'company_url': 'https://www.trypleez.com',
        'country': 'Portugal',
    }
    
    crew_instance = ClaygentCrew()
    
    # Run LinkedIn scraper
    print("Running LinkedIn scraper...")
    linkedin_result = crew_instance.run_linkedin_scraper(inputs)
    print("LinkedIn scraper result:", linkedin_result)
    
    # Run employee scraper
    print("\nRunning employee scraper...")
    employee_result = crew_instance.run_employee_scraper(inputs)
    print("Employee scraper result:", employee_result)
    
    # Run language detector
    print("\nRunning language detector...")
    language_result = crew_instance.run_language_detector(inputs)
    print("Language detector result:", language_result)
    
    # Run HR detector
    print("\nRunning HR detector...")
    hr_result = crew_instance.run_hr_detector(inputs)
    print("HR detector result:", hr_result)
    
    return {
        "linkedin_result": linkedin_result,
        "employee_result": employee_result,
        "language_result": language_result,
        "hr_result": hr_result
    }

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'full_name': 'John Doe',
        'company': 'Example Corp',
        'email': 'john.doe@example.com',
        'company_url': 'https://www.example.com',
        'ceo_name': 'John Doe',
        'country': 'United States',
    }
    try:
        crew_instance = ClaygentCrew()
        crew_instance.train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        crew_instance = ClaygentCrew()
        crew_instance.replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'full_name': 'John Doe',
        'company': 'Example Corp',
        'email': 'john.doe@example.com',
        'company_url': 'https://www.example.com',
        'country': 'United States',
    }
    try:
        crew_instance = ClaygentCrew()
        crew_instance.test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    globals()[sys.argv[1]]()
