from typing import List
import concurrent
from django.utils.translation import gettext_lazy as _, get_language_info
from django.conf import settings

from wagtail.models import Locale

from wagtail_localize.machine_translators.base import BaseMachineTranslator
from wagtail_localize.strings import StringValue

from wagtail_localize_ai.models import AITranslatorSettings, TranslationLog
from litellm import completion

class AITranslator(BaseMachineTranslator):
    display_name = _("AI Translator")

    def translate(self, source_locale: Locale, target_locale: Locale, strings: List[StringValue]) -> List[StringValue]:
        source_language = get_language_info(source_locale.language_code)[
            "name"
        ]
        target_language = get_language_info(target_locale.language_code)[
            "name"
        ]

        translator_settings = AITranslatorSettings.load()

        translation_log = TranslationLog(
            provider=translator_settings.provider,
            model=translator_settings.model,
            input_tokens=0,
            output_tokens=0,
            error=None,
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            executor_results = list(
                executor.map(translate_text, strings, [source_language] * len(strings), [target_language] * len(strings))
            )
        
        results = {}
        error = ""
        for result in executor_results:
            if "usage" in result:
                translation_log.input_tokens += result["usage"]["input_tokens"]
                translation_log.output_tokens += result["usage"]["output_tokens"]
            if "error" in result:
                error += result["error"] + "\n"
                continue
            results.update(result["result"])
        
        translation_log.error = error
        translation_log.save()

        return results

    def can_translate(self, source_locale: Locale, target_locale: Locale):
        translator_settings = AITranslatorSettings.load()
        if not translator_settings:
            return False
        has_provider = translator_settings.provider
        has_model = translator_settings.model
        not_same_language = source_locale.language_code != target_locale.language_code

        return has_provider and has_model and not_same_language

def translate_text(text: StringValue, source_language: str, target_language: str):
    translator_settings = AITranslatorSettings.load()

    provider = translator_settings.provider
    model = translator_settings.model
    if not model or not provider:
        return {
            "error": _("No provider or model configured"),
        }
    
    style_prompt = translator_settings.prompt
    
    SYSTEM_PROMPT = (
        "You are a translator that translates text from "
        f"{source_language} to {target_language}.\n"
        "Keep the structure intact. Only translate the text.\n"
        "Reply with just the translated text, HTML, or any other format without any wrapper or fence of any kind.\n"
        "- Do not add any additional text or HTML\n"
        "- Only inline HTML tags are allowed\n"
        "- Keep all attributes of the tags when present\n"
        "- If the text is slugified, keep it slugified"
    )

    if style_prompt:
        SYSTEM_PROMPT += f"\n\n#Style Instructions  \n{style_prompt}"
    
    SYSTEM_PROMPT += f"\n\nTranslate the following text to {target_language}."

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {"role": "user", "content": text.get_translatable_html()},
    ]

    provider_kwargs = {}

    for key, value in settings.AI_PROVIDERS[provider].items():
        # Skip all kwargs that start with an underscore
        if key.startswith("_"):
            continue
        provider_kwargs[key] = value

    try:
        response = completion(
            model=f"{provider}/{model}",
            temperature=0,
            messages=messages,
            **provider_kwargs
        )
    except Exception as e:
        return {
            "error": str(e),
        }
    
    usage = {
        "input_tokens": response["usage"]["prompt_tokens"],
        "output_tokens": response["usage"]["completion_tokens"],
    }

    if response["choices"][0]["message"]["content"].strip() == "":
        return {
            "error": _("Translation failed"),
            "usage": usage
        }
    
    return {
        "result": {
            text: StringValue.from_translated_html(response["choices"][0]["message"]["content"]),
        },
        "usage": usage,
    }