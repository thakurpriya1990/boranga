from django.contrib import admin

from boranga.admin import DeleteProtectedModelAdmin
from boranga.components.users import models


class SubmitterCategoryAdmin(DeleteProtectedModelAdmin):
    list_display = ("name", "visible_to")


class SubmitterInformationAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation", "position", "submitter_category")


class ExternalContributorBlacklistAdmin(admin.ModelAdmin):
    list_display = ("email", "reason", "datetime_created", "datetime_updated")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


admin.site.register(models.SubmitterCategory, SubmitterCategoryAdmin)
admin.site.register(models.SubmitterInformation, SubmitterInformationAdmin)
admin.site.register(
    models.ExternalContributorBlacklist, ExternalContributorBlacklistAdmin
)
