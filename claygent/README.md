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
   uvicorn src.claygent.main:app --reload
   ```

2. The API exposes two endpoints:
   - `/linkedin_scraper`: For LinkedIn scraping tasks
   - `/employee_scraper`: For employee scraping tasks

3. To execute a task, send a POST request to the appropriate endpoint with the required JSON body.

4. The API will return a JSON response with the results of the task execution.

Examples using cURL:

For LinkedIn scraper:
```bash
curl -X POST http://localhost:8000/linkedin_scraper -H "Content-Type: application/json" -d '{
"full_name": "John Doe",
"company": "Example Corp",
"email": "john.doe@example.com"
}'
```
For Employee scraper:
```bash
curl -X POST http://localhost:8000/employee_scraper -H "Content-Type: application/json" -d '{
"company": "Example Corp"
}'
```

To expose the local API, in a new terminal window start ngrok:
   ```bash
   ngrok http 8000
   ```

## Google Sheets Integration with Clasp

This project uses Clasp to manage the Google Apps Script for Google Sheets integration. Follow these steps to set up and push your Clasp files:

1. Install Clasp globally if you haven't already:
   ```bash
   npm install -g @google/clasp
   ```

2. Navigate to the Google Apps Script directory:
   ```bash
   cd src/claygent/sheets
   ```

3. Login to your Google account:
   ```bash
   clasp login
   ```

4. If you're connecting to an existing Google Apps Script project, clone it:
   ```bash
   clasp clone <scriptId>
   ```
   Replace `<scriptId>` with your actual script ID from the script's URL.

   If you're creating a new script, use:
   ```bash
   clasp create --title "Claygent Sheets Integration" --rootDir .
   ```

5. Push your local files to the Google Apps Script project:
   ```bash
   clasp push
   ```

6. To open the script in the Google Apps Script editor:
   ```bash
   clasp open
   ```

Remember to update the `API_BASE_URL` in your `Code.js` file with your ngrok URL before pushing changes.

Note: Make sure to add `.clasp.json` to your `.gitignore` file to avoid committing sensitive information.

After making changes to your local script files, always remember to push the changes using `clasp push` from the `src/claygent/sheets` directory.

## Understanding Your Crew

The claygent Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Claygent Crew or crewAI:
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.