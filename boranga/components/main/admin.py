from typing import Any

from django import forms
from django.apps import apps
from django.contrib.gis import admin
from django.http import HttpRequest

from boranga.admin import (
    ArchivableModelAdminMixin,
    CsvExportMixin,
    DeleteProtectedModelAdmin,
)
from boranga.components.main.models import (
    Document,
    FileExtensionWhitelist,
    HelpTextEntry,
    UserSystemSettings,
)


class UserSystemSettingsAdmin(admin.ModelAdmin):
    list_display = ["user", "area_of_interest"]


class ModelForm(forms.ModelForm):
    choices = (
        (
            "all",
            "all",
        ),
    ) + tuple(
        map(
            lambda m: (m, m),
            filter(
                lambda m: Document
                in apps.get_app_config("boranga").models[m].__bases__,
                apps.get_app_config("boranga").models,
            ),
        )
    )

    model = forms.ChoiceField(choices=choices)


class FileExtensionWhitelistAdmin(DeleteProtectedModelAdmin):
    fields = (
        "name",
        "model",
        "compressed",
    )
    list_display = (
        "name",
        "model",
        "compressed",
    )
    form = ModelForm


class HelpTextEntryAdmin(
    CsvExportMixin, ArchivableModelAdminMixin, DeleteProtectedModelAdmin
):
    list_display = [
        "section_id",
        "text",
        "icon_with_popover",
        "authenticated_users_only",
        "internal_users_only",
    ]

    def get_readonly_fields(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> list[str] | tuple[Any, ...]:
        fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            return list(fields) + ["section_id"]
        return fields


admin.site.register(FileExtensionWhitelist, FileExtensionWhitelistAdmin)
admin.site.register(UserSystemSettings, UserSystemSettingsAdmin)
admin.site.register(HelpTextEntry, HelpTextEntryAdmin)
