from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from boranga.components.spatial.models import TileLayer
from boranga.components.spatial.serializers import TileLayerSerializer

from boranga.helpers import is_customer, is_internal


class TileLayerViewSet(viewsets.ModelViewSet):
    """
    A simple ModelViewSet for listing or retrieving tile layers.
    """

    queryset = TileLayer.objects.none()
    serializer_class = TileLayerSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TileLayerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = TileLayer.objects.all()
        tile_layer = get_object_or_404(queryset, pk=pk)
        serializer = TileLayerSerializer(tile_layer)
        return Response(serializer.data)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TileLayer.objects.none()
        if is_customer(self.request):
            return TileLayer.objects.filter(is_external=True).order_by("id")
        elif is_internal(self.request):
            return TileLayer.objects.filter(is_internal=True).order_by("id")
        else:
            raise ValueError("User is not a customer or internal user")
