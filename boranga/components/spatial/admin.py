from django.contrib import admin

from .models import GeoserverUrl, TileLayer


class TileLayerInline(admin.TabularInline):
    model = TileLayer
    extra = 0
    fields = (
        "display_title",
        "layer_name",
        "layer_title",
        "geoserver_url",
        "is_satellite_background",
        "is_streets_background",
        "is_external",
        "is_internal",
        "visible",
    )
    ordering = ("display_title", "layer_name")
    list_filter = (
        "is_satellite_background",
        "is_streets_background",
        "is_external",
        "is_internal",
        "visible",
    )
    list_editable = ("is_external", "is_internal", "visible")
    list_display_links = ("display_title", "layer_name")
    verbose_name = "Tile Layer for this Geoserver"
    verbose_name_plural = "Tile Layers for this Geoserver"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("geoserver_url")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "geoserver_url":
            kwargs["queryset"] = GeoserverUrl.objects.order_by("url")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "layer_name":
            formfield.widget.attrs["size"] = 50
        return formfield

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields["geoserver_url"].widget.can_add_related = False
        formset.form.base_fields["geoserver_url"].widget.can_change_related = False
        formset.form.base_fields["geoserver_url"].widget.can_delete_related = False
        return formset

    def has_add_permission(self, request, ob=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(GeoserverUrl)
class GeoserverUrlAdmin(admin.ModelAdmin):
    list_display = ("url", "wms_version")
    search_fields = ("url",)
    ordering = ("url",)

    inlines = [TileLayerInline]


@admin.register(TileLayer)
class TileLayerAdmin(admin.ModelAdmin):
    list_display = (
        "display_title",
        "layer_name",
        "layer_title",
        "geoserver_url",
        "is_satellite_background",
        "is_streets_background",
        "is_external",
        "is_internal",
        "visible",
    )
    search_fields = ("display_title", "layer_name", "layer_title", "geoserver_url__url")
    ordering = ("display_title", "layer_name")
    list_filter = (
        "is_satellite_background",
        "is_streets_background",
        "is_external",
        "is_internal",
        "visible",
    )
    list_editable = ("is_external", "is_internal", "visible")
    list_display_links = ("display_title", "layer_name")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "display_title",
                    "layer_name",
                    "layer_title",
                    "geoserver_url",
                    "is_satellite_background",
                    "is_streets_background",
                    "is_external",
                    "is_internal",
                    "visible",
                )
            },
        ),
    )
