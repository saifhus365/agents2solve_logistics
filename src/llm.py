"""
LLM instance factory using NVIDIA NIM API with Qwen3.5-122B-A10B.

Uses the `langchain-nvidia-ai-endpoints` package which provides ChatNVIDIA,
a LangChain-compatible chat model that connects to NVIDIA's hosted endpoints.
"""

import warnings
import httpx
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from src.config import NVIDIA_API_KEY, MODEL_ID, MODEL_TEMPERATURE, MODEL_MAX_TOKENS

# Suppress known warnings about model type and tool support
warnings.filterwarnings("ignore", message=".*is not known to support tools.*")
warnings.filterwarnings("ignore", message=".*found.*in available_models.*type is unknown.*")
warnings.filterwarnings("ignore", message=".*is not default parameter.*")


def get_llm(
    temperature: float = MODEL_TEMPERATURE,
    max_tokens: int = MODEL_MAX_TOKENS,
) -> ChatNVIDIA:
    """
    Create a ChatNVIDIA instance connected to Qwen3.5-122B-A10B on NVIDIA NIM.

    This model is a 122B-parameter Mixture-of-Experts model with 10B active
    parameters per token—strong reasoning at efficient compute cost.

    Args:
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
        max_tokens: Maximum tokens in the response

    Returns:
        A ChatNVIDIA instance ready for .invoke(), .bind_tools(), etc.
    """
    return ChatNVIDIA(
        model=MODEL_ID,
        api_key=NVIDIA_API_KEY,
        temperature=temperature,
        max_tokens=max_tokens,
    )

