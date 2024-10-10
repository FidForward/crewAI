#!/usr/bin/env python
import sys
from claygent.crew import ClaygentCrew

def run():
    """
    Run the crew for both LinkedIn and employee scraping.
    """
    linkedin_inputs = {
        'full_name': 'Miguel CerqueiraMartins',
        'company': 'Pleez',
        'email': 'miguel.martins@trypleez.com'
    }
    
    crew_instance = ClaygentCrew()
    
    # Run LinkedIn scraper
    print("Running LinkedIn scraper...")
    linkedin_result = crew_instance.run_linkedin_scraper(linkedin_inputs)
    print("LinkedIn scraper result:", linkedin_result)
    
    # Run employee scraper
    print("\nRunning employee scraper...")
    employee_inputs = {
        'company': 'Pleez',
        'full_name': 'Miguel Cerqueira Martins', 
        'email': 'miguel.martins@trypleez.com'
    }
    employee_result = crew_instance.run_employee_scraper(employee_inputs)
    print("Employee scraper result:", employee_result)
    
    return {
        "linkedin_result": linkedin_result,
        "employee_result": employee_result
    }

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'full_name': 'John Doe',
        'company': 'Example Corp',
        'email': 'john.doe@example.com'
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
        'email': 'john.doe@example.com'
    }
    try:
        crew_instance = ClaygentCrew()
        crew_instance.test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    globals()[sys.argv[1]]()