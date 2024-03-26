import logging
import re
import json

from django.conf import settings
from django.contrib.gis.geos import Polygon, Point
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from ledger_api_client.ledger_models import EmailUserRO as EmailUser  # , Document
from boranga.components.occurrence.models import (
    OccurrenceReportGeometry,
    OccurrenceReport,
    OccurrenceReportUserAction,
)
from boranga.components.occurrence.email import (
    send_external_submit_email_notification,
    send_submit_email_notification,
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
        == OccurrenceReportGeometry.objects.filter(occurrence_report=instance).count()
    ):
        # No feature to save and no feature to delete
        logger.warn(f"OccurrenceReport geometry has no features to save or delete")
        return

    action = request.data.get("action", None)

    geometry_ids = []
    for feature in geometry.get("features"):
        allowed_geometry_types = ["Polygon", "Point"]
        geometry_type = feature.get("geometry").get("type")
        # check if feature is a polygon, continue if not
        if geometry_type not in allowed_geometry_types:
            logger.warn(
                f"OccurrenceReport: {instance} contains a feature that is not a {' or '.join(allowed_geometry_types)}: {feature}"
            )
            continue

        # Create a Polygon object from the open layers feature
        polygon = Polygon(feature.get("geometry").get("coordinates")[0]) if geometry_type == "Polygon" else None
        point = Point(feature.get("geometry").get("coordinates")) if geometry_type == "Point" else None

        geometry_data = {
            "occurrence_report_id": instance.id,
            "polygon": polygon,
            "point": point,
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
            serializer = OccurrenceReportGeometrySaveSerializer(
                geometry, data=geometry_data
            )
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
        OccurrenceReportGeometry.objects.filter(occurrence_report=instance)
        .exclude(Q(id__in=geometry_ids) | Q(locked=True) | ~Q(drawn_by=request.user.id))
        .delete()
    )
    if deleted_geometries[0] > 0:
        logger.info(
            f"Deleted OccurrenceReport geometries: {deleted_geometries} for {instance}"
        )


def ocr_proposal_submit(ocr_proposal, request):
    with transaction.atomic():
        if ocr_proposal.can_user_edit:
            ocr_proposal.submitter = request.user.id
            ocr_proposal.lodgement_date = timezone.now()
            # if (ocr_proposal.amendment_requests):
            #     qs = ocr_proposal.amendment_requests.filter(status = "requested")
            #     if (qs):
            #         for q in qs:
            #             q.status = 'amended'
            #             q.save()

            # Create a log entry for the proposal
            ocr_proposal.log_user_action(
                OccurrenceReportUserAction.ACTION_LODGE_PROPOSAL.format(
                    ocr_proposal.id
                ),
                request,
            )
            # Create a log entry for the organisation
            # proposal.applicant.log_user_action(ProposalUserAction.ACTION_LODGE_APPLICATION.format(ocr_proposal.id),request)
            applicant_field = getattr(ocr_proposal, ocr_proposal.applicant_field)
            # TODO handle the error "'EmailUserRO' object has no attribute 'log_user_action'" for below
            # applicant_field.log_user_action(ConservationStatusUserAction.ACTION_LODGE_PROPOSAL.format(ocr_proposal.id),request)

            ret1 = send_submit_email_notification(request, ocr_proposal)
            ret2 = send_external_submit_email_notification(request, ocr_proposal)

            # cs_proposal.save_form_tabs(request)
            if ret1 and ret2:
                ocr_proposal.processing_status = "with_assessor"
                ocr_proposal.customer_status = "with_assessor"
                # cs_proposal.documents.all().update(can_delete=False)
                ocr_proposal.save()
            else:
                raise ValidationError(
                    "An error occurred while submitting occurrence report proposal (Submit email notifications failed)"
                )

            return ocr_proposal

        else:
            raise ValidationError("You can't edit this report at this moment")

def save_document(request, instance, comms_instance, document_type, input_name=None):
    if "filename" in request.data and input_name:
        filename = request.data.get("filename")
        _file = request.data.get("_file")

        if document_type == "shapefile_document":
            document = instance.shapefile_documents.get_or_create(
                input_name=input_name, name=filename
            )[0]

        document._file = _file
        document.save()

@transaction.atomic
def process_shapefile_document(request, instance, *args, **kwargs):
    action = request.data.get("action")
    input_name = request.data.get("input_name")
    document_type = "shapefile_document"
    request.data.get("document_id")
    comms_instance = None

    if action == "list":
        pass
    elif action == "delete":
        # TODO:
        delete_document(
            request, instance, comms_instance, document_type, input_name
        )
    elif action == "cancel":
        # TODO:
        deleted = cancel_document(
            request, instance, comms_instance, document_type, input_name
        )
    elif action == "save":
        save_document(request, instance, comms_instance, document_type, input_name)
    else:
        raise ValidationError(f"Invalid action {action} for shapefile document")

    documents_qs = instance.shapefile_documents

    returned_file_data = [
        dict(
            url=d.path,
            id=d.id,
            name=d.name,
        )
        for d in documents_qs.filter(input_name=input_name)
        if d._file
    ]
    return {"filedata": returned_file_data}
