from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from claygent.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
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
			max_iter=2
		)

	# @agent
	# def reviewer(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['reviewer'],
	# 		verbose=True
	# 	)

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

	# @task
	# def reviewer_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['reviewer_task'],
	# 		output_file='report.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the Claygent crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
   			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)