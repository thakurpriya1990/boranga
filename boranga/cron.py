# Currently no cron jobs are defined here but this file is kept for future use.
import logging

from django import conf
from django.core import management
import django_cron

log = logging.getLogger(__name__)

class CronJobFetchNomosTaxonDataDaily(django_cron.CronJobBase):
    """Cron Job for the Catalogue Scanner."""
    RUN_ON_DAYS = [0, 1, 2, 3, 4, 5, 6]
    RUN_AT_TIMES = ['20:00']
    schedule = django_cron.Schedule(run_on_days=RUN_ON_DAYS,run_at_times=RUN_AT_TIMES)
    code = "boranga.fetch_nomos_data"

    def do(self) -> None:
        """Perform the Scanner Cron Job."""
        # Log
        log.info("Fetch Nomos Taxon Data cron job triggered, running...")

        # Run Management Command
        management.call_command("fetch_nomos_blob_data")
        return "Job Completed Successfully"