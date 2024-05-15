from django.contrib import admin

from boranga.components.users import models


class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("email_user", "organisation", "position", "user_category")


class ExternalContributorBlacklistAdmin(admin.ModelAdmin):
    list_display = ("email", "reason", "datetime_created", "datetime_updated")


admin.site.register(models.UserCategory, UserCategoryAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(
    models.ExternalContributorBlacklist, ExternalContributorBlacklistAdmin
)
