# CloudOps AI Lab

A cloud operations and AI agent demonstration project combining Python, FastAPI, hosted language models, automated testing, and infrastructure-as-code planning.

## Project Overview

CloudOps AI Lab demonstrates how an AI-assisted operations service can analyze server resource metrics and return a concise health assessment.

The current implementation uses synthetic server metrics and a deterministic analysis tool. A hosted language model, accessed through OpenRouter's OpenAI-compatible API, interprets the request, calls the analysis tool, and produces a final response.

**Current status:** Local API operational, hosted AI integration working, and 13 automated tests passing.

## Architecture

```text
Client / FastAPI Swagger UI
             |
             v
        FastAPI API
             |
             v
    Request Validation
             |
             v
     Hosted AI Agent
             |
             v
       OpenRouter API
             |
             v
   Health Analysis Tool
             |
             v
     Structured Findings
             |
             v
        API Response
```

### Technology Stack

- **Python** — application development
- **FastAPI** — HTTP API and interactive documentation
- **Pydantic** — request validation
- **smolagents** — AI agent and tool orchestration
- **OpenRouter** — hosted language model access
- **pytest** — automated testing
- **python-dotenv** — local environment configuration
- **Terraform** — planned infrastructure-as-code component

## API Endpoints

| Method | Endpoint            | Purpose                           |
| ------ | ------------------- | --------------------------------- |
| GET    | `/`                 | Basic application information     |
| GET    | `/health`           | Application health check          |
| POST   | `/agent/analyze`    | Deterministic health analysis     |
| POST   | `/agent/analyze-ai` | Hosted AI-powered health analysis |
| GET    | `/docs`             | Interactive API documentation     |

### Example Request

Send a POST request to `/agent/analyze-ai` with:

```json
{
  "server_name": "web-server-01",
  "cpu_percent": 52,
  "memory_percent": 20,
  "disk_percent": 30
}
```

The API validates the request and returns an analysis based on the supplied metrics.

The metrics in this example are synthetic and do not represent a live server.

## Local Setup

### Prerequisites

- Python compatible with the project's dependencies
- Git
- An OpenRouter API key for the hosted AI endpoint

### 1. Create and activate a virtual environment

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

Install the dependencies listed in the project's dependency file once it has been created.

If the project does not yet have a `requirements.txt` or equivalent dependency manifest, that is a planned next step.

### 3. Configure environment variables

Create a `.env` file in the project root:

```dotenv
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL_ID=openrouter/free
```

Replace the placeholder with your own API key. Never commit a real key to version control.

The application loads local environment settings using `python-dotenv`.

### 4. Start the API

From the project root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

Use the Swagger interface to test the available endpoints.

## Automated Tests

Run the test suite from the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The current suite contains 13 passing tests covering API behavior, request validation, health-analysis logic, and hosted AI endpoint handling.

The hosted AI endpoint tests use controlled test doubles where appropriate, so passing tests do not guarantee that an external model provider is always available.

## Logging and Observability

The application logs HTTP request methods, paths, status codes, and durations. The hosted AI integration also records model metadata when the provider returns it.

Example request log:

```text
INFO cloudops HTTP request method=POST path=/agent/analyze-ai status_code=200 duration_ms=...
```

API keys, authorization headers, and full request bodies should not be written to routine application logs.

When deployed to AWS, centralized logging, retention, and ingestion costs will need to be configured deliberately.

## Security and Limitations

- Server metrics are supplied by the API client; the application does not currently collect metrics from real servers.
- The health-analysis tool validates resource percentages and applies predefined thresholds.
- The agent is restricted to the configured analysis tool and is not intended to execute arbitrary shell commands or modify infrastructure.
- OpenRouter credentials belong in local environment configuration, not source code.
- `.env` and `.venv/` should remain excluded through `.gitignore`.
- The project does not currently provision or manage AWS resources.

## Roadmap

1. Complete dependency management and local documentation.
2. Add continuous integration to run automated tests.
3. Design AWS infrastructure using Terraform.
4. Deploy the API using a cost-conscious AWS architecture.
5. Configure centralized logging, monitoring, and secret management.
6. Explore a controlled integration with real infrastructure metrics.
7. Document architecture decisions, security controls, and operational trade-offs.

## Project Goal

CloudOps AI Lab is intended as a portfolio project demonstrating practical skills in Python API development, AI integration, automated testing, operational observability, cloud architecture, and infrastructure as code.
