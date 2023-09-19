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
    ObservationMethod,
    PlantCountMethod,
    PlantCountAccuracy,
    CountedSubject,
    PlantCondition,
    PrimaryDetectionMethod,
    SecondarySign,
    ReproductiveMaturity,
    DeathReason,
    AnimalHealth,
    IdentificationCertainty,
    SampleType,
    SampleDestination,
    PermitType,
    )


# Each of the following models will be available to Django Admin.
admin.site.register(LandForm)
admin.site.register(RockType)
admin.site.register(SoilType)
admin.site.register(SoilColour)
admin.site.register(SoilCondition)
admin.site.register(Drainage)
admin.site.register(Intensity)
admin.site.register(ObservationMethod)
admin.site.register(PlantCountMethod)
admin.site.register(PlantCountAccuracy)
admin.site.register(CountedSubject)
admin.site.register(PlantCondition)
admin.site.register(PrimaryDetectionMethod)
admin.site.register(SecondarySign)
admin.site.register(ReproductiveMaturity)
admin.site.register(DeathReason)
admin.site.register(AnimalHealth)
admin.site.register(IdentificationCertainty)
admin.site.register(SampleType)
admin.site.register(SampleDestination)
admin.site.register(PermitType)