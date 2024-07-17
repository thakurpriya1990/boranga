from django.contrib import admin

from .models import SystemEmail


@admin.register(SystemEmail)
class SystemEmailAdmin(admin.ModelAdmin):
    fields = ["key", "email"]
    readonly_fields = ["key"]
    ordering = ["key", "email"]
