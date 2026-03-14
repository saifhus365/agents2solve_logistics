"""
Configuration & environment variable loading.

Loads API keys from .env file and validates they are present.
"""

import os
import sys
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()


def get_nvidia_api_key() -> str:
    """Get and validate the NVIDIA API key."""
    key = os.environ.get("NVIDIA_API_KEY", "")
    if not key or not key.startswith("nvapi-"):
        print(
            "ERROR: NVIDIA_API_KEY not found or invalid.\n"
            "Please set it in your .env file (starts with 'nvapi-').\n"
            "Get a free key at: https://build.nvidia.com"
        )
        sys.exit(1)
    return key


def get_tavily_api_key() -> str | None:
    """Get the Tavily API key (optional)."""
    key = os.environ.get("TAVILY_API_KEY", "")
    if key and key.startswith("tvly-"):
        return key
    return None


# Validate on import
NVIDIA_API_KEY = get_nvidia_api_key()
TAVILY_API_KEY = get_tavily_api_key()

# Model configuration
MODEL_ID = "mistralai/mistral-large-3-675b-instruct-2512"
MODEL_TEMPERATURE = 0.6
MODEL_MAX_TOKENS = 2048
