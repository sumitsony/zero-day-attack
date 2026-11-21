"""
LLM provider configuration and unified client factory.

Loads keys from .env (python-dotenv). All providers are OpenAI-compatible,
so one client handles them all. Switch providers by changing --provider.

CAVEATS
-------
- Free tiers are rate-limited. Not for production.
- Model IDs change; check provider docs if a model 404s.
"""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")


@dataclass
class ProviderConfig:
    base_url: str
    api_key_env: str | None
    default_model: str
    note: str = ""


PROVIDERS: dict[str, ProviderConfig] = {
    "ollama": ProviderConfig(
        base_url="http://localhost:11434/v1",
        api_key_env=None,
        default_model="llama3.2",
        note="local, unlimited, baseline",
    ),
    "gemini": ProviderConfig(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key_env="GEMINI_API_KEY",
        default_model="gemini-2.5-flash",
        note="free tier, best quality",
    ),
    "groq": ProviderConfig(
        base_url="https://api.groq.com/openai/v1",
        api_key_env="GROQ_API_KEY",
        default_model="llama-3.3-70b-versatile",
        note="free tier, fastest",
    ),
    "mistral": ProviderConfig(
        base_url="https://api.mistral.ai/v1",
        api_key_env="MISTRAL_API_KEY",
        default_model="mistral-small-latest",
        note="free mode",
    ),
    "cohere": ProviderConfig(
        base_url="https://api.cohere.ai/compatibility/v1",
        api_key_env="COHERE_API_KEY",
        default_model="command-r7b-12-2024",
        note="trial key, 1000 calls/month",
    ),
    "zai": ProviderConfig(
    base_url="https://api.z.ai/api/paas/v4",
    api_key_env="ZAI_API_KEY",
    default_model="glm-4.7-flash",
    note="free tier: input/output/cache free, 200K context",
    ),
}


def get_client(provider: str):
    from openai import OpenAI

    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider '{provider}'. Choose from {list(PROVIDERS)}")
    cfg = PROVIDERS[provider]

    if cfg.api_key_env:
        key = os.environ.get(cfg.api_key_env)
        if not key:
            raise RuntimeError(
                f"Missing {cfg.api_key_env} in environment/.env for provider '{provider}'."
            )
    else:
        key = "ollama"

    return OpenAI(base_url=cfg.base_url, api_key=key)


def generate(provider: str, prompt: str, model: str | None = None) -> str:
    cfg = PROVIDERS[provider]
    resp = get_client(provider).chat.completions.create(
        model=model or cfg.default_model,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content