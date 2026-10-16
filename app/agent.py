
from app.config import get_settings

from smolagents import OpenAIModel, ToolCallingAgent

from app.tools import analyze_server_health

import logging

logger = logging.getLogger(__name__)


def run_health_agent(
    server_name: str,
    cpu_percent: float,
    memory_percent: float,
    disk_percent: float,
) -> dict:
    """Run the existing deterministic health-analysis demo."""
    result = analyze_server_health(
        server_name,
        cpu_percent,
        memory_percent,
        disk_percent,
    )
    return {
        "agent": "CloudOps Health Agent",
        "mode": "deterministic_demo",
        "analysis": result,
    }


def run_llm_health_agent(
    server_name: str,
    cpu_percent: float,
    memory_percent: float,
    disk_percent: float,
) -> dict:
    """Analyze server metrics using a hosted language model."""
    
    settings = get_settings()
    api_key = settings.openrouter_api_key
    model_id = settings.openrouter_model_id

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not configured.")

    if not model_id:
        raise RuntimeError("OPENROUTER_MODEL_ID is not configured.")

    model = OpenAIModel(
        model_id=model_id,
        api_base="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.1,
        max_tokens=1000,
    )

    
    actual_models = []

    original_create = model.client.chat.completions.create

    def tracked_create(*args, **kwargs):
        response = original_create(*args, **kwargs)

        actual_model = getattr(response, "model", None)
        if actual_model:
            actual_models.append(actual_model)
            logger.info(
                "OpenRouter returned model: %s",
                actual_model,
            )

        return response

    model.client.chat.completions.create = tracked_create


    agent = ToolCallingAgent(
        tools=[analyze_server_health],
        model=model,
        max_steps=4,
        instructions=(
            "You are a server health analysis assistant. "
            "Call analyze_server_health exactly once using the supplied "
            "server name and numeric metrics. Base your conclusions on "
            "the tool result. Then provide a concise final answer. "
            "Do not invent measurements, claim to access real servers, "
            "or change infrastructure."
        ),
    )

    task = (
        f"Analyze the following supplied metrics for server {server_name!r}: "
        f"CPU={cpu_percent}%, memory={memory_percent}%, "
        f"disk={disk_percent}%. Use the health-analysis tool and "
        "summarize its findings."
    )

    result = agent.run(task)

    return {
    "agent": "CloudOps Health Agent",
    "mode": "hosted_llm",
    "requested_model": model_id,
    "model": actual_models[-1] if actual_models else None,
    "models_used": actual_models,
    "analysis": str(result),
}
