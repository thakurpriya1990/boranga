import logging

from django.contrib.auth.signals import user_logged_in
from django.db import transaction

from boranga.components.occurrence.models import (
    OccurrenceReportReferral,
    OCRExternalRefereeInvite,
)

logger = logging.getLogger(__name__)


@transaction.atomic
def ocr_process_ocr_external_referee_invite(sender, user, request, **kwargs):
    """
    Check if the user logging in has an external referee invite and if so, process it.
    """
    logger.info(
        "user_logged_in_signal running ocr_process_external_referee_invite function"
    )
    logger.info("Checking if there are any external referee invites for user: %s", user)
    if not OCRExternalRefereeInvite.objects.filter(
        archived=False, email=user.email, datetime_first_logged_in__isnull=True
    ).exists():
        return

    logger.info("External occurrence report referee invite found for user: %s", user)

    ocr_external_referee_invite = OCRExternalRefereeInvite.objects.get(email=user.email)
    ocr_external_referee_invite.datetime_first_logged_in = user.last_login
    logger.info(
        "Saving datetime_first_logged_in for occurrence report external referee invite: %s",
        ocr_external_referee_invite,
    )
    ocr_external_referee_invite.save()

    OccurrenceReportReferral.objects.create(
        occurrence_report=ocr_external_referee_invite.occurrence_report,
        referral=user.id,
        sent_by=ocr_external_referee_invite.sent_by,
        text=ocr_external_referee_invite.invite_text,
        assigned_officer=ocr_external_referee_invite.sent_by,
        is_external=True,
    )


user_logged_in.connect(ocr_process_ocr_external_referee_invite)
