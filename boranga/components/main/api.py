import logging
import re

import pyproj
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Q
from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters
from rest_framework import views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from boranga import helpers
from boranga.components.main.models import AbstractOrderedList, HelpTextEntry
from boranga.components.main.serializers import (
    AbstractOrderedListSerializer,
    ContentTypeSerializer,
    HelpTextEntrySerializer,
)
from boranga.components.occurrence.models import Datum
from boranga.permissions import IsInternal

logger = logging.getLogger(__name__)


class HelpTextEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HelpTextEntry.objects.active()
    serializer_class = HelpTextEntrySerializer
    lookup_field = "section_id"

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            return qs.exclude(authenticated_users_only=True).exclude(
                internal_users_only=True
            )
        if not helpers.is_internal(self.request):
            return qs.exclude(internal_users_only=True)
        return qs


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentType.objects.filter(app_label="boranga")
    serializer_class = ContentTypeSerializer
    permission_classes = [IsInternal]
    filter_backends = [filters.DjangoFilterBackend, rest_framework_filters.SearchFilter]
    filterset_fields = ["app_label", "model"]
    search_fields = ["^model"]

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def ocr_bulk_import_content_types(self, request):
        """Returns a list of content types that are allowed to be imported in the ocr bulk importer"""
        content_types = (
            ContentType.objects.filter(
                app_label="boranga",
            )
            .filter(
                Q(model__startswith="occurrencereport")
                | Q(model__startswith="ocr")
                | Q(model__iexact="occurrence")
                | Q(model__iexact="submitterinformation")
            )
            .exclude(
                model__in=[
                    "occurrencereportproposalrequest",
                    "occurrencereportdeclineddetails",
                    "occurrencereportshapefiledocument",
                ]
            )
            .exclude(model__icontains="amendment")
            .exclude(model__icontains="bulkimport")
            .exclude(model__icontains="referral")
            .exclude(model__icontains="referee")
            .exclude(model__icontains="occurrencereportlog")
            .exclude(model__icontains="useraction")
        )
        serializer = self.get_serializer(content_types, many=True)
        return Response(serializer.data)


class RetrieveActionLoggingViewsetMixin:
    """Mixin to automatically log user actions when a user retrieves an instance.

    will scan the instance provided for the fields listed in settings
    use the first one it finds. If it doesn't find one it will raise an AttributeError.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.log_user_action(
            settings.ACTION_VIEW.format(
                instance._meta.verbose_name.title(),
                helpers.get_instance_identifier(instance),
            ),
            request,
        )
        request.user.log_user_action(
            settings.ACTION_VIEW.format(
                instance._meta.verbose_name.title(),
                helpers.get_instance_identifier(instance),
            ),
            request,
        )
        return super().retrieve(request, *args, **kwargs)


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
    cache_key = settings.CACHE_KEY_EPSG_CODES.format(
        **{"auth_name": auth_name, "pj_type": pj_type}
    )
    codes = cache.get(cache_key)

    if not codes:
        srids = [
            str(s)
            for s in Datum.objects.filter(archived=False).values_list("srid", flat=True)
        ]
        codes = [c for c in pyproj.get_codes(auth_name, pj_type) if c in srids]
        cache.set(cache_key, codes, timeout=settings.CACHE_TIMEOUT_24_HOURS)

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


class GetListItems(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, model_name, *args, **kwargs):
        try:
            model = apps.get_model(AbstractOrderedList.Meta.app_label, model_name)
        except LookupError:
            raise Http404

        if not issubclass(model, AbstractOrderedList):
            raise ValueError(
                f"Model {AbstractOrderedList.Meta.app_label}.{model_name} is not an instance of AbstractOrderedList"
            )

        serializer = AbstractOrderedListSerializer(model.objects.active(), many=True)

        return Response(serializer.data)
