import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import yaml

@CrewBase
class ClaygentCrew():
	"""Claygent crew"""

	def __init__(self):
		self.load_config()

	def load_config(self):
		config_dir = os.path.join(os.path.dirname(__file__), 'config')
		with open(os.path.join(config_dir, 'agents.yaml'), 'r') as f:
			self.agents_config = yaml.safe_load(f)
		with open(os.path.join(config_dir, 'tasks.yaml'), 'r') as f:
			self.tasks_config = yaml.safe_load(f)

	@agent
	def people_researcher(self) -> Agent:
		return Agent(
			role=self.agents_config['people_researcher']['role'],
			goal=self.agents_config['people_researcher']['goal'],
			backstory=self.agents_config['people_researcher']['backstory'],
			llm=self.agents_config['people_researcher']['llm'],
			verbose=True,
			tools=[SerperDevTool(n_results=10)],
			max_iter=5
		)

	@agent
	def image_finder(self) -> Agent:
		return Agent(
			role=self.agents_config['image_finder']['role'],
			goal=self.agents_config['image_finder']['goal'],
			backstory=self.agents_config['image_finder']['backstory'],
			llm=self.agents_config['image_finder']['llm'],
			verbose=True,
			tools=[SerperDevTool(search_url="https://google.serper.dev/images", n_results=10)],
			max_iter=5
		)

	@task
	def linkedin_scraper_task(self) -> Task:
		return Task(
			description=self.tasks_config['linkedin_scraper']['description'],
			expected_output=self.tasks_config['linkedin_scraper']['expected_output'],
			agent=self.people_researcher()
		)
  
	@task
	def employee_scraper_task(self) -> Task:
		return Task(
			description=self.tasks_config['employee_scraper']['description'],
			expected_output=self.tasks_config['employee_scraper']['expected_output'],
			agent=self.people_researcher()
		)

	@task
	def language_detector_task(self) -> Task:
		return Task(
			description=self.tasks_config['language_detector']['description'],
			expected_output=self.tasks_config['language_detector']['expected_output'],
			agent=self.people_researcher()
		)

	@task
	def hr_detector_task(self) -> Task:
		return Task(
			description=self.tasks_config['human_resources_detector']['description'],
			expected_output=self.tasks_config['human_resources_detector']['expected_output'],
			agent=self.people_researcher()
		)

	@task
	def profile_picture_finder_task(self) -> Task:
		return Task(
			description=self.tasks_config['profile_picture_finder']['description'],
			expected_output=self.tasks_config['profile_picture_finder']['expected_output'],
			agent=self.image_finder()
		)

	@crew
	def linkedin_crew(self) -> Crew:
		"""Creates the LinkedIn scraper crew"""
		return Crew(
				agents=[self.people_researcher()],
				tasks=[self.linkedin_scraper_task()],
				process=Process.sequential,
				verbose=True,
			)

	@crew
	def employee_crew(self) -> Crew:
		"""Creates the employee scraper crew"""
		return Crew(
				agents=[self.people_researcher()],
				tasks=[self.employee_scraper_task()],
				process=Process.sequential,
				verbose=True,
			)

	@crew
	def language_detector_crew(self) -> Crew:
		"""Creates the language detector crew"""
		return Crew(
				agents=[self.people_researcher()],
				tasks=[self.language_detector_task()],
				process=Process.sequential,
				verbose=True,
			)

	@crew
	def hr_detector_crew(self) -> Crew:
		"""Creates the HR detector crew"""
		return Crew(
				agents=[self.people_researcher()],
				tasks=[self.hr_detector_task()],
				process=Process.sequential,
				verbose=True,
			)

	@crew
	def profile_picture_crew(self) -> Crew:
		"""Creates the profile picture finder crew"""
		return Crew(
				agents=[self.image_finder()],
				tasks=[self.profile_picture_finder_task()],
				process=Process.sequential,
				verbose=True,
			)

	@crew
	def employee_and_picture_crew(self) -> Crew:
		"""Creates a crew that scrapes employees and then finds their profile pictures"""
		return Crew(
			agents=[self.people_researcher(), self.image_finder()],
			tasks=[
				self.employee_scraper_task(),
				self.profile_picture_finder_task()
			],
			process=Process.sequential,
			verbose=True,
		)

	def run_linkedin_scraper(self, inputs: dict):
		crew = self.linkedin_crew()
		result = crew.kickoff(inputs=inputs)
		return result.raw if result else None

	def run_employee_scraper(self, inputs: dict):
		crew = self.employee_crew()
		result = crew.kickoff(inputs=inputs)
		return result.raw if result else None

	def run_language_detector(self, inputs: dict):
		crew = self.language_detector_crew()
		result = crew.kickoff(inputs=inputs)
		return result.raw if result else None

	def run_hr_detector(self, inputs: dict):
		crew = self.hr_detector_crew()
		result = crew.kickoff(inputs=inputs)
		return result.raw if result else None

	def run_profile_picture_finder(self, inputs: dict):
		crew = self.profile_picture_crew()
		result = crew.kickoff(inputs=inputs)
		return result.raw if result else None

	def run_employee_and_picture_finder(self, inputs: dict):
		crew = self.employee_and_picture_crew()
		result = crew.kickoff(inputs=inputs)
		return result.raw if result else None

	def run_task(self, task_name, inputs):
		if task_name == "linkedin_scraper":
			return self.run_linkedin_scraper(inputs)
		elif task_name == "employee_scraper":
			return self.run_employee_scraper(inputs)
		elif task_name == "language_detector":
			return self.run_language_detector(inputs)
		elif task_name == "hr_detector":
			return self.run_hr_detector(inputs)
		elif task_name == "profile_picture_finder":
			return self.run_profile_picture_finder(inputs)
		elif task_name == "employee_and_picture_finder":
			return self.run_employee_and_picture_finder(inputs)
		else:
			raise ValueError(f"Unknown task: {task_name}")

	def train(self, n_iterations, filename, inputs):
		# Implement training logic
		pass

	def replay(self, task_id):
		# Implement replay logic
		pass

	def test(self, n_iterations, openai_model_name, inputs):
		# Implement test logic
		pass
