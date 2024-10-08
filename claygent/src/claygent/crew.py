import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class ClaygentCrew():
	"""Claygent crew"""

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			tools=[SerperDevTool(n_results=3)],
			max_iter=2,
			openai_api_key=os.getenv("OPENAI_API_KEY")
		)

	@task
	def linkedin_scraper_task(self) -> Task:
		return Task(
			config=self.tasks_config['linkedin_scraper'],
				verbose=True
		)
  
	@task
	def employee_scraper_task(self) -> Task:
		return Task(
			config=self.tasks_config['employee_scraper'],
				verbose=True
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Claygent crew"""
		return Crew(
			agents=[self.researcher()],
			tasks=[self.linkedin_scraper_task(), self.employee_scraper_task()],
			process=Process.sequential,
   			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

	def run_task(self, task_name: str, inputs: dict):
		crew = self.crew()
		result = crew.kickoff(inputs=inputs)
		
		# Extract raw results from tasks
		task_results = {
			'linkedin_scraper': None,
			'employee_scraper': None
		}
		
		for task in result.tasks_output:
			if task.name == 'linkedin_scraper_task':
				task_results['linkedin_scraper'] = task.raw
			elif task.name == 'employee_scraper_task':
				task_results['employee_scraper'] = task.raw
		
		return task_results