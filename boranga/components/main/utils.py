import json
import logging
from datetime import datetime

import pytz
import requests
from django.conf import settings
from django.db import connection
from django.db.models import Q
from ledger_api_client.ledger_models import EmailUserRO
from ledger_api_client.managed_models import SystemGroup
from rest_framework import serializers

from boranga.components.main.serializers import EmailUserROSerializerForReferral
from boranga.settings import GROUP_NAME_CHOICES

logger = logging.getLogger(__name__)


def retrieve_department_users():
    dep_users = (
        EmailUserRO.objects.filter(Q(email__endswith="@dbca.wa.gov.au"))
        .exclude(Q(first_name=""), Q(last_name=""))
        .order_by("first_name")
    )
    serialiser = EmailUserROSerializerForReferral(dep_users, many=True)
    return serialiser.data


def get_department_user(email):
    res = requests.get(
        f"{settings.CMS_URL}/api/users?email={email}",
        auth=(settings.LEDGER_USER, settings.LEDGER_PASS),
        verify=False,
    )
    res.raise_for_status()
    data = json.loads(res.content).get("objects")
    if len(data) > 0:
        return data[0]
    else:
        return None


def to_local_tz(_date):
    local_tz = pytz.timezone(settings.TIME_ZONE)
    return _date.astimezone(local_tz)


def check_db_connection():
    """check connection to DB exists, connect if no connection exists"""
    try:
        if not connection.is_usable():
            connection.connect()
    except Exception as e:
        logger.error(f"Error connecting to DB: {e}")
        connection.connect()


def handle_validation_error(e):
    if hasattr(e, "error_dict"):
        raise serializers.ValidationError(repr(e.error_dict))
    else:
        if hasattr(e, "message"):
            raise serializers.ValidationError(e.message)
        else:
            raise


def validate_threat_request(request):
    data = json.loads(request.data.get("data"))

    required_fields = {"threat_category_id":"Threat Category","current_impact":"Current Impact","date_observed":"Date Observed"}
    missing_required = []

    for i in required_fields:
        if not i in data or not data[i]:
            missing_required.append(required_fields[i])

    if missing_required:
        raise serializers.ValidationError(
            "Missing required values for Threat - " + ", ".join(missing_required)
        )

    # data observed must not be in the future
    try:
        if (
            "date_observed" in data
            and data["date_observed"]
            and datetime.strptime(data["date_observed"], "%Y-%m-%d") > datetime.now()
        ):
            raise serializers.ValidationError(
                "Date observed value invalid - must be on or before the current date"
            )
    except:
        raise serializers.ValidationError(
                "Date observed value invalid - must be on or before the current date"
            )
    return True


def get_geometry_source(geometry_obj):
    from boranga.components.occurrence.models import OccurrenceReportGeometry

    source = ""

    if not geometry_obj.drawn_by:
        source = "Unknown"
    # TODO not sure if checking for submitter is right for 'Applicant' as Assessor could be the submitter as well?
    elif isinstance(
        geometry_obj, OccurrenceReportGeometry
    ) and geometry_obj.drawn_by in [
        geometry_obj.occurrence_report.submitter,
    ]:
        # Polygon drawn by submitter
        source = "Applicant"
    else:
        # System group names, e.g. boranga_assessor
        system_groups = SystemGroup.objects.filter(
            name__in=[x for x in GROUP_NAME_CHOICES]
        )
        # System groups member ids
        system_group_member = list(
            {
                itm
                for group in system_groups
                for itm in group.get_system_group_member_ids()
            }
        )
        if geometry_obj.drawn_by in system_group_member:
            # Polygon drawn by assessor
            source = "Assessor"

    return source
