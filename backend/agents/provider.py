import os
import logging
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv

logger = logging.getLogger("campaign.agents")
load_dotenv()

def _provider_name() -> str:
    provider = os.getenv("AI_PROVIDER", "ollama").strip().lower()
    if provider not in {"ollama", "gemini"}:
        raise ValueError(
            f"Unsupported AI_PROVIDER '{provider}'. Expected 'ollama' or 'gemini'."
        )
    return provider


@lru_cache(maxsize=None)
def get_chat_model(model_role: str) -> Any:
    """Build the configured chat model for an agent role."""
    provider = _provider_name()

    if provider == "ollama":
        from langchain_ollama import ChatOllama

        model = os.getenv("OLLAMA_MODEL", "gemma4:12b")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        num_ctx = int(os.getenv("OLLAMA_NUM_CTX", "8192"))
        num_predict = int(os.getenv("OLLAMA_NUM_PREDICT", "2048"))
        logger.info(
            "LLM provider ready: role=%s provider=ollama model=%s base_url=%s num_ctx=%d num_predict=%d",
            model_role,
            model,
            base_url,
            num_ctx,
            num_predict,
        )
        return ChatOllama(
            model=model,
            base_url=base_url,
            reasoning=False,
            num_ctx=num_ctx,
            num_predict=num_predict,
            temperature=float(os.getenv("OLLAMA_TEMPERATURE", "0.1")),
            keep_alive=os.getenv("OLLAMA_KEEP_ALIVE", "10m"),
        )

    from langchain_google_genai import ChatGoogleGenerativeAI

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    logger.info("LLM provider ready: role=%s provider=gemini model=%s", model_role, model)
    return ChatGoogleGenerativeAI(
        model=model,
        api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"),
    )
