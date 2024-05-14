from copy import deepcopy

from django.contrib.gis import admin
from ledger_api_client.admin import SystemGroupAdmin
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from ledger_api_client.managed_models import SystemGroup

from boranga import helpers as boranga_helpers

admin.site.index_template = "admin-index.html"
admin.autodiscover()


@admin.register(EmailUser)
class EmailUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    ordering = ("email",)
    search_fields = ("id", "email", "first_name", "last_name")

    def has_change_permission(self, request, obj=None):
        if obj is None:  # and obj.status > 1:
            return True
        return None

    def has_delete_permission(self, request, obj=None):
        return None


class CustomSystemGroupAdmin(SystemGroupAdmin):
    """
    Overriding the SystemGroupAdmin from ledger.accounts.admin,
    to remove ledger_permissions selection field for DjangoAdmin SystemGroup on Admin page
    """

    filter_horizontal = ("permissions",)

    def get_fieldsets(self, request, obj=None):
        """Remove the ledger_permissions checkbox from the Admin page, if user is DjangoAdmin and NOT superuser"""
        fieldsets = super(SystemGroupAdmin, self).get_fieldsets(request, obj)
        if not obj:
            return fieldsets
        if request.user.is_superuser:
            return fieldsets
        elif boranga_helpers.is_django_admin(request):
            fieldsets = deepcopy(fieldsets)
            for fieldset in fieldsets:
                if "permissions" in fieldset[1]["fields"]:
                    if type(fieldset[1]["fields"]) is tuple:
                        fieldset[1]["fields"] = list(fieldset[1]["fields"])
                    fieldset[1]["fields"].remove("permissions")

        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        elif boranga_helpers.is_django_admin(request):
            return ["name"]  # make fields readonly when editing an existing object


admin.site.unregister(SystemGroup)
admin.site.register(SystemGroup, CustomSystemGroupAdmin)
