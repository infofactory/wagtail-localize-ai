# Wagtail Localize AI Translator
A machine translator for Wagtail Localize that uses LiteLLM for translation

## Prerequisites
- Python 3.9+
- a Wagtail project with Wagtail Localize correctly configured


## Dependencies
- [Wagtail Localize](https://github.com/wagtail/wagtail-localize)
- [litellm](https://github.com/litellm/litellm)

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
Each provider is a key, the value will be a dict of kwargs that will be passed to the completion function.
You can also add a `_name` key to provide a verbose name of the provider.

You can find all providers and their kwargs in the [litellm documentation](https://docs.litellm.ai/docs/providers)

Here are some examples for the most popular providers:

#### OpenAI
```python
AI_PROVIDERS = {
    "openai": {
        "_name": "OpenAI",
        "api_key": "sk-...",
        "base_url": "https://api.openai.com/v1", # Optional
        "organization": "org-...", # Optional
    }
}
```

#### Anthropic
```python
AI_PROVIDERS = {
    "anthropic": {
        "_name": "Anthropic",
        "api_key": "sk-...",
    }
}
```

#### Azure OpenAI
```python
AI_PROVIDERS = {
    "azure": {
        "_name": "Azure OpenAI",
        "api_key": "sk-...",
        "base_url": "https://...",
        "api_version": "2023-03-15-preview", # Optional
    }
}
```

#### Azure AI
```python
AI_PROVIDERS = {
    "azure_ai": {
        "_name": "Azure AI",
        "api_key": "sk-...",
        "base_url": "https://...",
    }
}
```

#### Vertex AI
```python
AI_PROVIDERS = {
    "vertex_ai": {
        "_name": "Vertex AI",
        "vertex_project": 'project-...',
        "vertex_location": 'europe-west8',
    }
}

# Load the google cloud
with open("path/to/vertex_ai_service_account.json") as f:
    AI_PROVIDERS["vertex_ai"]["vertex_credentials"] = json.load(f)
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
