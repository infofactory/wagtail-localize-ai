from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.views.generic import IndexView, InspectView
from wagtail.admin.ui.tables import DateColumn, BooleanColumn
from .models import TranslationLog
from django.utils.translation import gettext_lazy as _

class AiTranslationLogIndexView(IndexView):

    def get_edit_url(self, instance):
        return None

    def get_delete_url(self, instance):
        return None

    def get_add_url(self):
        return None

class AiTranslationLogInspectView(InspectView):

    def get_edit_url(self):
        return None

    def get_delete_url(self):
        return None

class AiTranslationLogViewSet(ModelViewSet):
    model = TranslationLog
    icon = "history"
    menu_label = _("AI Translation Logs")
    add_to_admin_menu = False
    list_display = ["provider", "model", "input_tokens", "output_tokens", DateColumn('timestamp'), BooleanColumn('status')]
    list_filter = ["provider", "model"]
    add_to_reference_index = False

    copy_view_enabled = False
    inspect_view_enabled = True
    inspect_view_fields = ["timestamp", "provider", "model", "input_tokens", "output_tokens", "error"]

    index_view_class = AiTranslationLogIndexView
    inspect_view_class = AiTranslationLogInspectView

    form_fields = []

    permission_policy = None
