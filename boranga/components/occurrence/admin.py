from django.contrib.gis import admin, forms
import nested_admin

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
    OccurrenceTenure,
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


class OccurrenceTenureInline(nested_admin.NestedTabularInline):
    model = OccurrenceTenure
    extra = 0
    verbose_name = "Occurrence Geometry Tenure Area"
    verbose_name_plural = "Occurrence Geometry Tenure Areas"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "tenure_area_id",
                    "status",
                    "owner_name",
                    "owner_count",
                    "purpose",
                    "significant_to_occurrence",
                    "comments",
                )
            },
        ),
    )

    readonly_fields = ["tenure_area_id"]


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


class OccurrenceGeometryInlineForm(forms.ModelForm):
    geometry = forms.GeometryField(widget=forms.OSMWidget(attrs={"display_raw": False}))

    class Meta:
        model = OccurrenceGeometry
        fields = "__all__"


class OccurrenceGeometryInline(nested_admin.NestedStackedInline):
    model = OccurrenceGeometry
    form = OccurrenceGeometryInlineForm
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

    inlines = [OccurrenceTenureInline]


@admin.register(OccurrenceReport)
class OccurrenceReportAdmin(admin.ModelAdmin):
    inlines = [OccurrenceReportGeometryInline]


@admin.register(Occurrence)
class OccurrenceAdmin(nested_admin.NestedModelAdmin):
    inlines = [OccurrenceGeometryInline]


@admin.register(OccurrenceTenure)
class OccurrenceTenureAdmin(nested_admin.NestedModelAdmin):
    model = OccurrenceTenure

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "status",
                        "occurrence",
                        "significant_to_occurrence",
                        "purpose",
                        "comments",
                    ),
                )
            },
        ),
        (
            "Cadastre Spatial Identification",
            {
                "fields": (
                    ("tenure_area_id",),
                    (
                        "typename",
                        "featureid",
                    ),
                )
            },
        ),
        (
            "Cadastre Owner Information",
            {
                "fields": (
                    (
                        "owner_name",
                        "owner_count",
                    ),
                )
            },
        ),
        (
            "Occurrence Geometry",
            {
                "fields": (
                    "occurrence_geometry",
                    "geometry",
                )
            },
        ),
    )

    readonly_fields = ["typename", "featureid", "geometry", "occurrence"]
    list_filter = ("status", "significant_to_occurrence", "purpose")

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
