from django.db.models.signals import post_delete, pre_save, post_save, m2m_changed
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from boranga.components.conservation_status.models import (
    ConservationStatusReferral,
    ConservationStatus
)

import logging
logger = logging.getLogger(__name__)


# class ConservationStatusReferralListener(object):
#     """
#     Event listener for ConservationStatusReferral
#     """

#     @staticmethod
#     @receiver(pre_save, sender=ConservationStatusReferral)
#     def _pre_save(sender, instance, **kwargs):
#         if instance.pk:
#             original_instance = ConservationStatusReferral.objects.get(pk=instance.pk)
#             setattr(instance, "_original_instance", original_instance)

#         elif hasattr(instance, "_original_instance"):
#             delattr(instance, "_original_instance")

#     @staticmethod
#     @receiver(post_save, sender=ConservationStatusReferral)
#     def _post_save(sender, instance, **kwargs):
#         import ipdb; ipdb.set_trace()
#         original_instance = getattr(instance, "_original_instance") if hasattr(instance, "_original_instance") else None
#         if original_instance:
#             # Check if the proposal attached to the referral outstanding referrals
#             outstanding  = instance.conservation_status.referrals.filter(processing_status='with_referral')
#             if len(outstanding) == 0:
#                 instance.conservation_status.processing_status = 'with_assessor'
#                 instance.conservation_status.save()