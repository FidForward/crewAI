#!/usr/bin/env python
from .crew import ClaygentCrew
from .api import app
import sys

def run():
    """
    Run the crew for employee and picture finding, and language detection.
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
    
    # Run employee and picture finder
    employee_picture_result = crew_instance.run_employee_and_picture_finder(inputs)
    
    # Run language detector
    # print("\nRunning language detector...")
    # language_result = crew_instance.run_language_detector(inputs)
    # print("Language detector result:", language_result)
    
    return {
        "employee_picture_result": employee_picture_result,
        #"language_result": language_result,
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
        crew_instance.train(n_iterations=int(sys.argv[2]), filename=sys.argv[3], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        crew_instance = ClaygentCrew()
        crew_instance.replay(task_id=sys.argv[2])
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
        crew_instance.test(n_iterations=int(sys.argv[2]), openai_model_name=sys.argv[3], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    globals()[sys.argv[1]]()
