import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from boranga.components.conservation_status.models import (
    ConservationChangeCode,
    ConservationStatus,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delist conservation statuses that have expired."

    def handle(self, *args, **options):
        logger.info(f"Running command {__name__}")

        expired_conservation_statuses = ConservationStatus.objects.filter(
            effective_to__lt=timezone.now(),
            processing_status=ConservationStatus.PROCESSING_STATUS_APPROVED,
        )
        delisted_change_code = ConservationChangeCode.get_delisted_change_code()

        logger.info(
            "Found {} conservation statuses where effective_to__lt=timezone.now() and processing_status={}".format(
                expired_conservation_statuses.count(),
                ConservationStatus.PROCESSING_STATUS_APPROVED,
            )
        )

        for conservation_status in expired_conservation_statuses:
            conservation_status.change_code = delisted_change_code
            conservation_status.processing_status = (
                ConservationStatus.CUSTOMER_STATUS_CLOSED
            )
            conservation_status.save()

        logger.info(
            "Delisted {} conservation statuses.".format(
                expired_conservation_statuses.count()
            )
        )

        logger.info(f"Finished Running command {__name__}")
