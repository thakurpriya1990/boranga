from django import forms
from django.contrib import admin

from .models import GeoserverUrl, Proxy, TileLayer


class TileLayerModelForm(forms.ModelForm):
    class Meta:
        model = TileLayer
        fields = "__all__"
        help_texts = {
            "display_title": "The title to display in the layer switcher",
            "layer_name": "The name of the layer in Geoserver",
            "layer_title": "The title of the layer",
            "geoserver_url": "The Geoserver URL to which the layer belongs",
            "is_satellite_background": "Whether the layer is the satellite background layer (mutually exclusive with is_streets_background)",
            "is_streets_background": "Whether the layer is the streets background layer (mutually exclusive with is_satellite_background)",
            "is_external": "Whether the layer is available for external use",
            "is_internal": "Whether the layer is available for internal use",
            "visible": "Whether the layer is visible by default",
            "min_zoom": "The minimum zoom level at which the layer is visible",
            "max_zoom": "The maximum zoom level at which the layer is visible",
            "active": "Whether the layer is disabled and won't be used by the map component",
        }


class GeoserverUrlForm(forms.ModelForm):
    class Meta:
        model = GeoserverUrl
        fields = "__all__"
        help_texts = {
            "url": "The URL of the Geoserver",
            "wms_version": "The WMS version of the Geoserver",
        }


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
    form = GeoserverUrlForm

    list_display = ("url", "wms_version")
    search_fields = ("url",)
    ordering = ("url",)

    inlines = [TileLayerInline]


@admin.register(TileLayer)
class TileLayerAdmin(admin.ModelAdmin):
    form = TileLayerModelForm

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
        "active",
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
                    "min_zoom",
                    "max_zoom",
                    "active",
                )
            },
        ),
    )


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    list_display = ("request_path", "username", "basic_auth_enabled", "active")
    search_fields = ("request_path",)
    ordering = ("request_path",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "request_path",
                    "proxy_url",
                    "basic_auth_enabled",
                    "username",
                    "password",
                    "active",
                )
            },
        ),
    )
