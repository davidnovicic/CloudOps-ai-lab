
import logging
import time

from app.config import get_settings

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


from app.agent import run_health_agent, run_llm_health_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("cloudops")

app = FastAPI(
    title="CloudOps AI Lab",
    description="A cloud infrastructure and AI agent demonstration project",
    version="0.3.0",
)

#logging
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "Unhandled request error method=%s path=%s",
            request.method,
            request.url.path,
        )
        raise

    duration_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "HTTP request method=%s path=%s status_code=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    return response


#guardrail
class HealthAnalysisRequest(BaseModel):
    server_name: str = Field(min_length=1, max_length=100)
    cpu_percent: float = Field(ge=0, le=100)
    memory_percent: float = Field(ge=0, le=100)
    disk_percent: float = Field(ge=0, le=100)


@app.get("/")
def root():
    return {
        "project": "CloudOps AI Lab",
        "status": "running",
        "message": "Welcome to the CloudOps AI Lab API",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/agent/analyze")
def analyze(request: HealthAnalysisRequest):
    return run_health_agent(
        server_name=request.server_name,
        cpu_percent=request.cpu_percent,
        memory_percent=request.memory_percent,
        disk_percent=request.disk_percent,
    )


@app.post("/agent/analyze-ai")
def analyze_with_ai(request: HealthAnalysisRequest):
    settings = get_settings()

    if not settings.openrouter_api_key or not settings.openrouter_model_id:
        raise HTTPException(
        status_code=503,
        detail=(
            "Hosted AI is not configured. Set the OpenRouter "
            "API key and model ID in the environment."
        ),
        )

    try:
        return run_llm_health_agent(
            server_name=request.server_name,
            cpu_percent=request.cpu_percent,
            memory_percent=request.memory_percent,
            disk_percent=request.disk_percent,
        )
    except Exception as exc:
        logger.exception("Hosted AI request failed")
        
        raise HTTPException(
            status_code=502,
            detail="The hosted AI request failed. Check the model ID, "
            "API key, provider availability, and server logs.",
        ) from exc
