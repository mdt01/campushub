"""One place to create an LLM client, so every lab works with any provider.

Works with any OpenAI-compatible endpoint: cloud providers, routers, or a local
Ollama server. Configure it with LLM_BASE_URL, LLM_API_KEY and LLM_MODEL.
"""
import os

from openai import OpenAI


def make_client() -> OpenAI:
    base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise SystemExit("Set LLM_API_KEY (use any text such as 'ollama' for a local model).")
    return OpenAI(base_url=base_url, api_key=api_key)


def default_model() -> str:
    model = os.getenv("LLM_MODEL")
    if not model:
        raise SystemExit("Set LLM_MODEL to a model name offered by your provider.")
    return model
