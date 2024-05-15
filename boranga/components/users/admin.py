from django.contrib import admin

from boranga.components.users import models


class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("email_user", "organisation", "position", "user_category")


admin.site.register(models.UserCategory, UserCategoryAdmin)
admin.site.register(models.Profile, ProfileAdmin)
