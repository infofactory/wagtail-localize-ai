from django.conf import settings
from any_llm import AnyLLM


def get_ai_providers() -> dict:
    providers = getattr(settings, "AI_PROVIDERS", {})
    if isinstance(providers, dict):
        return providers
    return {}


def get_provider_config(provider_key: str) -> dict:
    providers = get_ai_providers()
    config = providers.get(provider_key, {})
    if isinstance(config, dict):
        return config
    return {}


def get_provider_kwargs(provider_key: str, *, exclude_private: bool = True) -> dict:
    config = get_provider_config(provider_key)
    kwargs = {}
    for key, value in config.items():
        if exclude_private and key.startswith("_"):
            continue
        kwargs[key] = value
    return kwargs


def get_provider_name(provider_key: str) -> str:
    """Returns the any-llm provider name for a given key.

    Falls back to the key itself for backward compatibility when _provider is not set.
    """
    config = get_provider_config(provider_key)
    name = config.get("_provider")
    if isinstance(name, str) and name.strip():
        return name.strip()
    return provider_key


def get_provider_display_name(provider_key: str) -> str:
    config = get_provider_config(provider_key)
    name = config.get("_name")
    if isinstance(name, str) and name.strip():
        return name.strip()
    return provider_key


def normalize_model_identifier(provider_key: str, model: str) -> str:
    """Normalizes model identifier to provider:model format expected by any-llm."""
    provider = get_provider_name(provider_key)
    if ":" in model:
        return model
    if "/" in model:
        return model.replace("/", ":", 1)
    return f"{provider}:{model}"


def get_llm_client(provider_key: str):
    provider = get_provider_name(provider_key)
    provider_kwargs = get_provider_kwargs(provider_key, exclude_private=True)
    return AnyLLM.create(provider, **provider_kwargs)
