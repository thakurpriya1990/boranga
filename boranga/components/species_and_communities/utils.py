import re
from django.db import transaction, IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
#from preserialize.serialize import serialize
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
import traceback
import os
from copy import deepcopy
from datetime import datetime
import time
from boranga.components.conservation_status.email import send_external_submit_email_notification,send_submit_email_notification
from boranga.components.species_and_communities.models import(
    Species,
    Community,
    GroupType,
    SpeciesUserAction,
    CommunityUserAction,
)


import logging
logger = logging.getLogger(__name__)

def species_form_submit(species_instance,request):
        with transaction.atomic():
            if species_instance.can_user_edit:
                species_instance.submitter = request.user.id
                species_instance.lodgement_date = timezone.now()
                # Create a log entry for the proposal
                species_instance.log_user_action(SpeciesUserAction.ACTION_CREATE_SPECIES.format(species_instance.species_number),request)
                # Create a log entry for the organisation
                #proposal.applicant.log_user_action(ProposalUserAction.ACTION_LODGE_APPLICATION.format(proposal.id),request)
                applicant_field=getattr(species_instance, species_instance.applicant_field)
                # TODO handle the error "'EmailUserRO' object has no attribute 'log_user_action'" for below
                #applicant_field.log_user_action(ConservationStatusUserAction.ACTION_LODGE_PROPOSAL.format(cs_proposal.id),request)

                
                # ret1 = send_submit_email_notification(request, species_instance)
                # ret2 = send_external_submit_email_notification(request, species_instance)

                # if ret1 and ret2:
                #     species_instance.processing_status = 'current'
                #     #cs_proposal.documents.all().update(can_delete=False)
                #     species_instance.save()
                # else:
                #     raise ValidationError('An error occurred while submitting proposal (Submit email notifications failed)')
                
                species_instance.processing_status = 'current'
                # species_instance.documents.all().update(can_delete=False)
                species_instance.save()
                
                return species_instance

            else:
                raise ValidationError('You can\'t submit this species at this moment')

def community_form_submit(community_instance,request):
        with transaction.atomic():
            if community_instance.can_user_edit:
                community_instance.submitter = request.user.id
                community_instance.lodgement_date = timezone.now()
                # Create a log entry for the proposal
                community_instance.log_user_action(CommunityUserAction.ACTION_CREATE_COMMUNITY.format(community_instance.community_number),request)
                # Create a log entry for the organisation
                #proposal.applicant.log_user_action(ProposalUserAction.ACTION_LODGE_APPLICATION.format(proposal.id),request)
                applicant_field=getattr(community_instance, community_instance.applicant_field)
                # TODO handle the error "'EmailUserRO' object has no attribute 'log_user_action'" for below
                #applicant_field.log_user_action(ConservationStatusUserAction.ACTION_LODGE_PROPOSAL.format(cs_proposal.id),request)

                
                # ret1 = send_submit_email_notification(request, community_instance)
                # ret2 = send_external_submit_email_notification(request, community_instance)

                # if ret1 and ret2:
                #     community_instance.processing_status = 'current'
                #     #community_instance.documents.all().update(can_delete=False)
                #     community_instance.save()
                # else:
                #     raise ValidationError('An error occurred while submitting form (Submit email notifications failed)')
                
                community_instance.processing_status = 'current'
                # community_instance.documents.all().update(can_delete=False)
                community_instance.save()
                
                return community_instance

            else:
                raise ValidationError('You can\'t submit this community at this moment')