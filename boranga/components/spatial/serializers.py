from rest_framework import serializers

from boranga.components.spatial.models import TileLayer


class TileLayerSerializer(serializers.ModelSerializer):
    geoserver_url = serializers.StringRelatedField()

    class Meta:
        model = TileLayer
        fields = "__all__"
