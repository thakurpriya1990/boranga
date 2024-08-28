import logging

from django.core.management.base import BaseCommand

from boranga.components.occurrence.models import OccurrenceReportBulkImportTask

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Pre process the OCR bulk import tasks"

    def handle(self, *args, **options):
        logger.info(f"Running command {__name__}")

        # Check if there are already any tasks running and return if so
        if OccurrenceReportBulkImportTask.objects.filter(
            processing_status=OccurrenceReportBulkImportTask.PROCESSING_STATUS_STARTED
        ).exists():
            logger.info("There is already a task running, returning")
            return

        # Get the next task to process
        task = (
            OccurrenceReportBulkImportTask.objects.filter(
                processing_status=OccurrenceReportBulkImportTask.PROCESSING_STATUS_QUEUED,
                _file__isnull=False,
                rows__isnull=True,
            )
            .order_by("datetime_queued")
            .first()
        )

        if task is None:
            logger.info("No tasks to process, returning")
            return

        # Process the task
        task.count_rows()

        logger.info(f"OCR Bulk Import Task {task.id} has {task.rows} rows.")

        return
