from django.urls import reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from .views import AiTranslationLogViewSet

translation_logs_viewset = AiTranslationLogViewSet()
@hooks.register("register_admin_viewset")
def register_viewset():
    return translation_logs_viewset

@hooks.register("register_reports_menu_item")
def register_reports_menu_item():
    return MenuItem(
        label=translation_logs_viewset.menu_label,
        url=reverse(translation_logs_viewset.get_url_name('index')),
        icon_name=translation_logs_viewset.icon,
        order=9001
    )