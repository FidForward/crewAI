# Claygent Crew

Welcome to the Claygent Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling.

To install the dependencies:

```bash
crewai install
```

## Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/claygent/config/agents.yaml` to define your agents
- Modify `src/claygent/config/tasks.yaml` to define your tasks
- Modify `src/claygent/crew.py` to add your own logic, tools and specific args
- Modify `src/claygent/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ cd claygent/
$ crewai run
```

This command initializes the claygent Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Using the Exposed API

The Claygent Crew exposes an API that allows you to interact with the AI agents and execute tasks:

1. Start the API server:
   ```bash
   cd claygent/src/claygent
   uvicorn main:app --reload
   ```

2. The API exposes a single endpoint: `/run_task`

3. To execute a task, send a POST request to `http://localhost:8000/` with a JSON body containing `task_name` and `input_data`.

4. The API will return a JSON response with the results of the task execution.

Example using cURL:
```bash
curl -X POST http://localhost:8000/ -H "Content-Type: application/json" -d '{
"task_name": "linkedin_scraper",
"input_data": {
"full_name": "John Doe",
"company": "Example Corp",
"email": "john.doe@example.com"
}
}'
```

## Understanding Your Crew

The claygent Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Claygent Crew or crewAI:
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
