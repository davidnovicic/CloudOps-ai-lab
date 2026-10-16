
import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load local development settings from .env, if present.
load_dotenv()


@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str | None
    openrouter_model_id: str | None


def get_settings() -> Settings:
    """Read application settings from environment variables."""
    return Settings(
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
        openrouter_model_id=os.getenv("OPENROUTER_MODEL_ID"),
    )
