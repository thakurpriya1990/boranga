import logging
import re
import json

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry, Polygon
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from ledger_api_client.ledger_models import EmailUserRO as EmailUser  # , Document
from boranga.components.occurrence.models import (
    OccurrenceReportGeometry,
    OccurrenceReport,
)
from boranga.components.occurrence.serializers import (
    OccurrenceReportGeometrySaveSerializer,
)

logger = logging.getLogger(__name__)


def save_geometry(request, instance, geometry_data):
    logger.info(f"\n\n\nSaving Occurrence Report geometry")

    if not geometry_data:
        logger.warn(f"No Occurrence Report geometry to save")
        return
    
    geometry = json.loads(geometry_data)
    if (
        0 == len(geometry["features"])
        and 0
        == OccurrenceReportGeometry.objects.filter(occurrence_report = instance).count()
    ):
        # No feature to save and no feature to delete
        logger.warn(f"OccurrenceReport geometry has no features to save or delete")
        return

    action = request.data.get("action", None)

    geometry_ids = []
    for feature in geometry.get("features"):
        # check if feature is a polygon, continue if not
        if feature.get("geometry").get("type") != "Polygon":
            logger.warn(
                f"OccurrenceReport: {instance} contains a feature that is not a polygon: {feature}"
            )
            continue

        # Create a Polygon object from the open layers feature
        polygon = Polygon(feature.get("geometry").get("coordinates")[0])

        geometry_data = {
            "occurrence_report_id": instance.id,
            "polygon": polygon,
            # "intersects": True,  # probably redunant now that we are not allowing non-intersecting geometries
        }
        if feature.get("id"):
            logger.info(
                f"Updating existing OccurrenceReport geometry: {feature.get('id')} for Report: {instance}"
            )
            try:
                geometry = OccurrenceReportGeometry.objects.get(id=feature.get("id"))
            except OccurrenceReportGeometry.DoesNotExist:
                logger.warn(
                    f"OccurrenceReport geometry does not exist: {feature.get('id')}"
                )
                continue
            geometry_data["drawn_by"] = geometry.drawn_by
            geometry_data["locked"] = (
                action in ["submit"]
                and geometry.drawn_by == request.user.id
                or geometry.locked
            )
            serializer = OccurrenceReportGeometrySaveSerializer(geometry, data=geometry_data)
        else:
            logger.info(f"Creating new geometry for OccurrenceReport: {instance}")
            geometry_data["drawn_by"] = request.user.id
            geometry_data["locked"] = action in ["submit"]
            serializer = OccurrenceReportGeometrySaveSerializer(data=geometry_data)
    
        serializer.is_valid(raise_exception=True)
        ocr_geometry_instance = serializer.save()
        logger.info(f"Saved OccurrenceReport geometry: {ocr_geometry_instance}")
        geometry_ids.append(ocr_geometry_instance.id)
    
    # Remove any ocr geometries from the db that are no longer in the ocr_geometry that was submitted
    # Prevent deletion of polygons that are locked after status change (e.g. after submit)
    # or have been drawn by another user
    deleted_geometries = (
        OccurrenceReportGeometry.objects.filter(occurrence_report = instance)
        .exclude(Q(id__in=geometry_ids) | Q(locked=True) | ~Q(drawn_by=request.user.id))
        .delete()
    )
    if deleted_geometries[0] > 0:
        logger.info(
            f"Deleted OccurrenceReport geometries: {deleted_geometries} for {instance}"
        )

