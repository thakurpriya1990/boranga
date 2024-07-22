from django.contrib.gis import admin

from boranga.admin import DeleteProtectedModelAdmin
from boranga.components.main.models import FileExtensionWhitelist, Document
from django.apps import apps
from django import forms


class ModelForm(forms.ModelForm):
    choices = (("all","all",),) + tuple(
            map(lambda m: (m,m), filter(lambda m: Document in apps.get_app_config('boranga').models[m].__bases__, apps.get_app_config('boranga').models))
        ) 

    model = forms.ChoiceField(choices=choices)

class FileExtensionWhitelistAdmin(DeleteProtectedModelAdmin):
    fields = ("name","model","compressed",)
    list_display = ("name","model","compressed",)
    form = ModelForm


admin.site.register(FileExtensionWhitelist, FileExtensionWhitelistAdmin)
