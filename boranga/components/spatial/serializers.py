from rest_framework import serializers

from boranga import settings
from boranga.components.spatial.models import GeoserverUrl, Proxy, TileLayer


class GeoserverUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoserverUrl
        fields = "__all__"


class TileLayerSerializer(serializers.ModelSerializer):
    geoserver_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TileLayer
        fields = "__all__"

    def get_geoserver_url(self, obj):
        return obj.geoserver_url.url


class ProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = Proxy
        fields = "__all__"
