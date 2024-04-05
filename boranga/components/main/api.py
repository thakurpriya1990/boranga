import logging

from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from boranga.components.main.models import GlobalSettings
from boranga.components.main.serializers import (
    GlobalSettingsSerializer,
)
from boranga import helpers

logger = logging.getLogger("payment_checkout")


class GlobalSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GlobalSettings.objects.none()
    serializer_class = GlobalSettingsSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = GlobalSettings.objects.all().order_by("id")
            return qs


class UserActionLoggingViewset(viewsets.ModelViewSet):
    """Class that extends the ModelViewSet to log the common user actions

    will scan the instance provided for the fields listed in settings
    use the first one it finds. If it doesn't find one it will raise an AttributeError.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.log_user_action(
            settings.ACTION_VIEW.format(
                instance._meta.verbose_name.title(),  # pylint: disable=protected-access
                helpers.get_instance_identifier(instance),
            ),
            request,
        )
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        instance = response.data.serializer.instance
        instance.log_user_action(
            settings.ACTION_CREATE.format(
                instance._meta.verbose_name.title(),  # pylint: disable=protected-acces
                helpers.get_instance_identifier(instance),
            ),
            request,
        )
        return response

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.log_user_action(
            settings.ACTION_UPDATE.format(
                instance._meta.verbose_name.title(),  # pylint: disable=protected-access
                helpers.get_instance_identifier(instance),
            ),
            request,
        )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.log_user_action(
            settings.ACTION_DESTROY.format(
                instance._meta.verbose_name.title(),  # pylint: disable=protected-access
                helpers.get_instance_identifier(instance),
            ),
            request,
        )
        return super().destroy(request, *args, **kwargs)


def search_datums(search):
    import pyproj

    name = pyproj.CRS.from_string("EPSG:4326").name
    datum_list = [{"id": 4326, "name": name}]
    return datum_list

class DatumSearchMixing:
    @action(detail=False, methods=["get"], url_path="epsg-code-datums")
    def get_epsg_code_datums(self, request):
        search = request.GET.get("search", None)

        return Response(search_datums(search))
