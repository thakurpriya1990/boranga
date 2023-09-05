from django.contrib.gis import admin
from import_export.admin import ImportExportMixin
from django.db.models import Q
from boranga.components.occurrence.models import (
    LandForm,
    RockType,
    SoilType,
    SoilColour,
    SoilCondition,
    Drainage,
    Intensity,
    )


# Each of the following models will be available to Django Admin.
admin.site.register(LandForm)
admin.site.register(RockType)
admin.site.register(SoilType)
admin.site.register(SoilColour)
admin.site.register(SoilCondition)
admin.site.register(Drainage)
admin.site.register(Intensity)