from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.admin.panels import FieldPanel, FieldRowPanel

from wagtail_localize_ai.utils import get_ai_providers, get_provider_display_name


class TranslationLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now, editable=False, verbose_name=_("Created"))
    provider = models.CharField(max_length=512, verbose_name=_("Provider"))
    model = models.CharField(max_length=512, verbose_name=_("Model"))

    input_tokens = models.IntegerField(verbose_name=_("Input Tokens"))
    output_tokens = models.IntegerField(verbose_name=_("Output Tokens"))

    error = models.TextField(null=True, blank=True, verbose_name=_("Error"))

    @property
    def status(self):
        return not bool(self.error)

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.provider} - {self.model}"

    class Meta:
        verbose_name = _("AI Translation Log")
        verbose_name_plural = _("AI Translation Logs")

def get_providers():
    return (
        (provider_key, get_provider_display_name(provider_key))
        for provider_key in get_ai_providers()
    )

@register_setting(icon='site')
class AITranslatorSettings(BaseGenericSetting):
    provider = models.CharField(max_length=512, verbose_name=_("Provider"), choices=get_providers)
    model = models.CharField(max_length=512, verbose_name=_("Model"))

    prompt = models.TextField(
        default="",
        blank=True,
        verbose_name=_("Style prompt"),
        help_text=_("Give instructions to the AI about the style, how to translate certain things or other informations about the website you're translating."),
    )

    panels = [
        FieldRowPanel([
            FieldPanel('provider'),
            FieldPanel('model'),
        ]),
        FieldPanel('prompt'),
    ]

    class Meta:
        verbose_name = _("AI Translator")
        verbose_name_plural = _("AI Translator")
