# Wagtail Localize AI Translator
A machine translator for Wagtail Localize that uses Any-LLM for translation

## Prerequisites
- Python 3.11+
- a Wagtail project with Wagtail Localize correctly configured


## Dependencies
- [Wagtail Localize](https://github.com/wagtail/wagtail-localize)
- [any-llm-sdk](https://pypi.org/project/any-llm-sdk/)

## Installation
Install the package using pip:

```bash
pip install wagtail-localize-ai
```
In your `settings.py` file,
- Add `wagtail_localize_ai` to your `INSTALLED_APPS`
- Add `wagtail.contrib.settings` to your `INSTALLED_APPS` (used to setup model and prompt)
- Setup `WAGTAILLOCALIZE_MACHINE_TRANSLATOR` like this:
    ```python
    WAGTAILLOCALIZE_MACHINE_TRANSLATOR = {
        "CLASS": "wagtail_localize_ai.translator.AITranslator",
    }
    ```

Then, run `python manage.py migrate wagtail_localize_ai` to create the required database tables

### Setting up providers

To set up providers add to your `settings.py` file a dict called `AI_PROVIDERS`.  
Each entry is an arbitrary key identifying the provider instance, with a dict of configuration.

Reserved keys (all start with `_`):
- `_name`: display name shown in the Wagtail admin
- `_provider`: any-llm provider name (e.g. `openai`, `anthropic`). Defaults to the entry key, so you can omit it when the key matches the provider name.

All other keys are passed as kwargs to `AnyLLM.create(provider, **kwargs)`.

You can find supported providers and their kwargs in the [any-llm documentation](https://pypi.org/project/any-llm-sdk/).

Having multiple instances of the same provider (e.g. different API keys or endpoints) is supported:
```python
AI_PROVIDERS = {
    "openai_main": {
        "_name": "OpenAI (main)",
        "_provider": "openai",
        "api_key": "sk-...",
    },
    "openai_secondary": {
        "_name": "OpenAI (secondary)",
        "_provider": "openai",
        "api_key": "sk-other-...",
        "api_base": "https://my-proxy.example.com/v1",
    },
}
```

Here are some examples for the most popular providers:

#### OpenAI
```python
AI_PROVIDERS = {
    "openai": {
        "_name": "OpenAI",
        "api_key": "sk-...",
        "organization": "org-...",  # Optional
        "api_base": "https://api.openai.com/v1",  # Optional
    }
}
```

#### Anthropic
```python
AI_PROVIDERS = {
    "anthropic": {
        "_name": "Anthropic",
        "api_key": "sk-ant-...",
    }
}
```

#### Azure OpenAI
Provider key: `azureopenai` (OpenAI-compatible Azure endpoint).
```python
AI_PROVIDERS = {
    "azureopenai": {
        "_name": "Azure OpenAI",
        "api_key": "...",
        "api_base": "https://<resource>.openai.azure.com",
        "api_version": "preview",  # Optional, defaults to "preview"
    }
}
```

#### Azure AI
Provider key: `azure` (Azure AI Inference SDK, for models deployed on Azure AI Foundry).
```python
AI_PROVIDERS = {
    "azure": {
        "_name": "Azure AI",
        "api_key": "...",
        "api_base": "https://<model-deployment-name>.<region>.models.ai.azure.com",
    }
}
```

#### Gemini
```python
AI_PROVIDERS = {
    "gemini": {
        "_name": "Gemini",
        "api_key": "...",
    }
}
```

#### Vertex AI
Provider key: `vertexai`. `project`, `location` and `credentials` are passed directly to the Google GenAI client.

Using Application Default Credentials (e.g. `gcloud auth application-default login`):
```python
AI_PROVIDERS = {
    "vertexai": {
        "_name": "Vertex AI",
        "project": "my-gcp-project",
        "location": "europe-west8",
    }
}
```

Using a service account JSON file:
```python
from google.oauth2 import service_account

AI_PROVIDERS = {
    "vertexai": {
        "_name": "Vertex AI",
        "project": "my-gcp-project",
        "location": "europe-west8",
        "credentials": service_account.Credentials.from_service_account_file(
            "/path/to/service_account.json",
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        ),
    }
}
```

## Usage
You can set the provider, model and prompt from the AI Translator page reachable from the Settings menu entry.  
You can also see the token usage from the Logs pagea in the Reports menu entry.


## License
This project is released under the [BSD license](LICENSE).

## Contributors

<a href="https://github.com/infofactory/wagtail-localize-ai/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=infofactory/wagtail-localize-ai" />
</a>
