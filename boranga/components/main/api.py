import logging

from django.conf import settings
from django.core.cache import cache
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


def get_cached_epsg_codes(auth_name="EPSG", pj_type="GEODETIC_CRS"):
    # TODO: This is a temporary solution to get the geodetic datums for australia
    cool_codes = ["4203", "4202", "7844", "9309", "4283", "4326"]

    cache_key = settings.CACHE_KEY_EPSG_CODES.format(
        **{"auth_name": auth_name, "pj_type": pj_type}
    )
    if cache.get(cache_key):
        return cache.get(cache_key)

    import pyproj

    codes = [c for c in pyproj.get_codes(auth_name, pj_type) if c in cool_codes]
    cache.set(cache_key, codes, timeout=60 * 60 * 24)

    return codes


def search_datums(search):
    import pyproj

    codes = get_cached_epsg_codes()

    geodetic_crs = [
        {"id": int(c), "name": f"EPSG:{c} - {pyproj.CRS.from_string(c).name}"}
        for c in codes
    ]

    datums = [c for c in geodetic_crs if f"{search}".lower() in c["name"].lower()]

    return datums


class DatumSearchMixing:
    @action(detail=False, methods=["get"], url_path="epsg-code-datums")
    def get_epsg_code_datums(self, request):
        search = request.GET.get("search", None)

        return Response(search_datums(search))
