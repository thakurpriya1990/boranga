from django.contrib.gis import admin

from boranga.components.main.models import UserSystemSettings


class UserSystemSettingsAdmin(admin.ModelAdmin):
    list_display = ["user", "area_of_interest"]


admin.site.register(UserSystemSettings, UserSystemSettingsAdmin)
