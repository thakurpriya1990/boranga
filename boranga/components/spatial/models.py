from django.db import models


class GeoserverUrl(models.Model):
    url = models.CharField(max_length=255, unique=True)
    wms_version = models.CharField(max_length=10, default="1.3.0")

    class Meta:
        app_label = "boranga"
        ordering = ["url"]
        verbose_name = "Geoserver URL"
        verbose_name_plural = "Geoserver URLs"

    def __str__(self):
        return self.url

    @property
    def get_capabilities_url(self):
        return f"{self.url}/?SERVICE=WMS&VERSION={self.wms_version}&REQUEST=GetCapabilities"


class TileLayer(models.Model):
    geoserver_url = models.ForeignKey(
        GeoserverUrl, on_delete=models.CASCADE, null=False, blank=False
    )
    layer_name = models.CharField(
        max_length=255, unique=True, null=False, blank=False
    )  # Name of the layer in Geoserver
    layer_title = models.CharField(max_length=255)  # Title of the layer
    display_title = models.CharField(
        max_length=255
    )  # Title to display in the layer switcher
    is_satellite_background = models.BooleanField(
        default=False
    )  # Whether the layer is the satellite background layer (mutually exclusive with is_streets_background)
    is_streets_background = models.BooleanField(
        default=False
    )  # Whether the layer is the streets background layer (mutually exclusive with is_satellite_background)
    is_external = models.BooleanField(
        default=True
    )  # Whether the layer is available for external use
    is_internal = models.BooleanField(
        default=True
    )  # Whether the layer is available for internal use
    visible = models.BooleanField(
        default=False
    )  # Whether the layer is visible by default
    disabled = models.BooleanField(
        default=False
    )  # Whether the layer is disabled and won't be used by the map component

    class Meta:
        app_label = "boranga"
        ordering = ["display_title", "layer_name"]
        verbose_name = "Geoserver Tile Layer"
        verbose_name_plural = "Geoserver Tile Layers"
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    ~models.Q(
                        ("is_satellite_background", True),
                        ("is_streets_background", True),
                    ),
                ),
                name="tilelayer_is_either_satellite_or_streets_background_or_neither",
            ),
        ]

    def __str__(self):
        return self.layer_name

    # @property
    # def layer_url(self):
    #     return f"{self.geoserver_url.url}/{self.layer_name}"
