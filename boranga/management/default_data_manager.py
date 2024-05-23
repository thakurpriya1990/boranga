import logging

from django.conf import settings
from ledger_api_client.managed_models import SystemGroup

from boranga.components.conservation_status.models import ConservationChangeCode

logger = logging.getLogger(__name__)


class DefaultDataManager:
    def __init__(self):
        for group_name in settings.GROUP_NAME_CHOICES:
            try:
                group, created = SystemGroup.objects.get_or_create(name=group_name)
                if created:
                    logger.info(f"Created SystemGroup: {group}")
            except Exception as e:
                logger.error(f"{e}, SystemGroup: {group_name}")

        # Delete any groups that are not in the settings.GROUP_NAME_CHOICES
        for sg in SystemGroup.objects.exclude(
            name__in=[group_name for group_name in settings.GROUP_NAME_CHOICES]
        ):
            sg.systemgrouppermission_set.all().delete()
            sg.delete()

        for conservation_change_code in settings.CONSERVATION_CHANGE_CODES:
            try:
                conservation_change_code_obj, created = (
                    ConservationChangeCode.objects.get_or_create(
                        code=conservation_change_code["code"],
                        defaults={"label": conservation_change_code["label"]},
                    )
                )
                if created:
                    logger.info(
                        f"Created ConservationChangeCode: {conservation_change_code_obj}"
                    )
            except Exception as e:
                logger.error(f"{e}, ConservationChangeCode: {conservation_change_code}")
