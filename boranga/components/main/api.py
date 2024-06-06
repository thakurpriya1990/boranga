import logging

from django.conf import settings
from django.core.cache import cache
from rest_framework import viewsets

from boranga.components.main.models import GlobalSettings
from boranga.components.main.serializers import (
    GlobalSettingsSerializer,
)
from boranga import helpers

import pyproj
import re

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


def proj4_string_from_epsg_code(code):
    # Function meant to provide ellipsoid parameters in proj4 string for proj4.js
    # Don't think this function will be used going forward,
    # because frontend datum transformation doesn't seem to be easily achievable

    ellipsoids = pyproj.get_ellps_map()
    crs = pyproj.CRS.from_string(code)
    prj = crs.to_proj4()
    prj_split = prj.split("+")

    regex = re.compile(r"(?:\+ellps=)(\w+)")
    matched = regex.search(prj)
    if not matched:
        return prj

    ellps = matched.group(1)
    ellps_params = ellipsoids.get(ellps, None)

    # Don't need description value
    ellps_params = {k: v for k, v in ellps_params.items() if k not in ["description"]}

    prj_additional_params = []
    for k, v in ellps_params.items():
        if any(f"{k}=" in p for p in prj.split("+")):
            # Ellipsoid parameter already exists in proj4 string
            continue
        prj_additional_params.append(f"{k}={v} ")

    ellps_pos = [i for i, p in enumerate(prj_split) if "ellps" in p][0]
    # Insert ellps parameters after ellps name
    prj_split = (
        prj_split[: ellps_pos + 1] + prj_additional_params + prj_split[ellps_pos + 1 :]
    )

    return "+".join(prj_split)


def get_cached_epsg_codes(auth_name="EPSG", pj_type="CRS"):
    # TODO: This is a temporary solution to get the geodetic datums for australia
    cool_codes = ["4203", "4202", "7842", "7844", "4283", "4326", "3857"]

    cache_key = settings.CACHE_KEY_EPSG_CODES.format(
        **{"auth_name": auth_name, "pj_type": pj_type, "codes": "-".join(cool_codes)}
    )

    if cache.get(cache_key):
        return cache.get(cache_key)

    codes = [c for c in pyproj.get_codes(auth_name, pj_type) if c in cool_codes]
    cache.set(cache_key, codes, timeout=60 * 60 * 24)

    return codes


def search_datums(search, codes=None):
    """Searches search-term in CRS names and returns those that match
    Can provide codes list to control which epsg codes to search in
    """

    if not codes:
        codes = get_cached_epsg_codes()

    geodetic_crs = [
        {
            "id": int(c),
            "name": f"EPSG:{c} - {pyproj.CRS.from_string(c).name}",
            # "proj4": proj4_string_from_epsg_code(c),
        }
        for c in codes
    ]

    datums = [c for c in geodetic_crs if f"{search}".lower() in c["name"].lower()]

    return datums

