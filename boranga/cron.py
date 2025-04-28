import logging

import django_cron
from django.core import management

log = logging.getLogger(__name__)


class CronJobFetchNomosTaxonDataDaily(django_cron.CronJobBase):
    RUN_ON_DAYS = [0, 1, 2, 3, 4, 5, 6]
    RUN_AT_TIMES = ["20:00"]
    schedule = django_cron.Schedule(
        run_weekly_on_days=RUN_ON_DAYS, run_at_times=RUN_AT_TIMES
    )
    code = "boranga.fetch_nomos_data"

    def do(self) -> None:
        log.info("Fetch Nomos Taxon Data cron job triggered, running...")
        management.call_command("fetch_nomos_blob_data")
        return "Job Completed Successfully"


class CronJobOCRPreProcessBulkImportTasks(django_cron.CronJobBase):
    schedule = django_cron.Schedule(
        run_weekly_on_days=[0, 1, 2, 3, 4, 5, 6], run_every_mins=2
    )
    code = "boranga.ocr_pre_process_bulk_import_tasks"

    def do(self) -> None:
        log.info("OCR Pre-process Bulk Import Tasks cron job triggered, running...")
        management.call_command("ocr_pre_process_bulk_import_tasks")
        return "Job Completed Successfully"


class CronJobOCRProcessBulkImportQueue(django_cron.CronJobBase):
    schedule = django_cron.Schedule(
        run_weekly_on_days=[0, 1, 2, 3, 4, 5, 6], run_every_mins=5
    )
    code = "boranga.ocr_process_bulk_import_queue"

    def do(self) -> None:
        log.info("OCR Process Bulk Import Tasks cron job triggered, running...")
        management.call_command("ocr_process_bulk_import_queue")
        return "Job Completed Successfully"
