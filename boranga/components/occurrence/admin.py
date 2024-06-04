from django.contrib.gis import admin

from boranga.components.occurrence.models import (
    AnimalHealth,
    CoordinationSource,
    CountedSubject,
    Datum,
    DeathReason,
    Drainage,
    IdentificationCertainty,
    Intensity,
    LandForm,
    LocationAccuracy,
    ObservationMethod,
    Occurrence,
    OccurrenceGeometry,
    OccurrenceReportGeometry,
    OccurrenceSource,
    OccurrenceReport,
    PermitType,
    PlantCondition,
    PlantCountAccuracy,
    PlantCountMethod,
    PrimaryDetectionMethod,
    ReproductiveMaturity,
    RockType,
    SampleDestination,
    SampleType,
    SecondarySign,
    SoilColour,
    SoilCondition,
    SoilType,
    WildStatus,
)


class OccurrenceReportGeometryInline(admin.StackedInline):
    model = OccurrenceReportGeometry
    extra = 0
    verbose_name = "Occurrence Report Geometry"
    verbose_name_plural = "Occurrence Report Geometries"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "geometry",
                    "original_geometry",
                    "intersects",
                    "copied_from",
                    "drawn_by",
                    "locked",
                )
            },
        ),
    )

    readonly_fields = ["original_geometry"]


class OccurrenceGeometryInline(admin.StackedInline):
    model = OccurrenceGeometry
    extra = 0
    verbose_name = "Occurrence Geometry"
    verbose_name_plural = "Occurrence Geometries"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "geometry",
                    "original_geometry",
                    "intersects",
                    "copied_from",
                    "drawn_by",
                    "locked",
                )
            },
        ),
    )

    readonly_fields = ["original_geometry"]


@admin.register(OccurrenceReport)
class OccurrenceAdmin(admin.ModelAdmin):
    inlines = [OccurrenceReportGeometryInline]


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    inlines = [OccurrenceGeometryInline]


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
admin.site.register(Datum)
admin.site.register(CoordinationSource)
admin.site.register(LocationAccuracy)
admin.site.register(OccurrenceSource)
admin.site.register(WildStatus)
