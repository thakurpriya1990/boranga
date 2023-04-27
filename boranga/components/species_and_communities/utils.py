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
from boranga.components.species_and_communities.email import (
    send_species_create_email_notification, 
    send_community_create_email_notification, 
    send_user_species_create_email_notification,
    send_user_community_create_email_notification,
    send_species_rename_email_notification,
)

from boranga.components.species_and_communities.models import(
    Species,
    Community,
    GroupType,
    SpeciesUserAction,
    CommunityUserAction,
)

from boranga.components.conservation_status.models import(
    ConservationStatusUserAction,
    ConservationStatus,
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

                
                ret1 = send_species_create_email_notification(request, species_instance)
                ret2 = send_user_species_create_email_notification(request, species_instance)

                if ret1 and ret2:
                    species_instance.processing_status = 'current'
                    # species_instance.documents.all().update(can_delete=False)
                    species_instance.save()
                else:
                    raise ValidationError('An error occurred while submitting proposal (Submit email notifications failed)')
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

                
                ret1 = send_community_create_email_notification(request, community_instance)
                ret2 = send_user_community_create_email_notification(request, community_instance)

                if ret1 and ret2:
                    community_instance.processing_status = 'current'
                    # community_instance.documents.all().update(can_delete=False)
                    community_instance.save()
                else:
                    raise ValidationError('An error occurred while submitting proposal (Submit email notifications failed)')
                
                return community_instance

            else:
                raise ValidationError('You can\'t submit this community at this moment')

def combine_species_original_submit(species_instance,request):
        with transaction.atomic():
            if species_instance.processing_status == 'current':
                species_instance.processing_status = 'historical'
                species_instance.save()
                 # change current active conservation status of the original species to inactive
                try:
                    if species_instance.processing_status == 'historical':
                        species_cons_status = ConservationStatus.objects.get(species=species_instance, processing_status='approved')
                        if species_cons_status:
                            species_cons_status.customer_status='closed'
                            species_cons_status.processing_status='closed'
                            species_cons_status.save()
                            #add the log_user_action
                            species_cons_status.log_user_action(ConservationStatusUserAction.ACTION_CLOSE_CONSERVATIONSTATUS.format(species_cons_status.conservation_status_number),request)
                except ConservationStatus.DoesNotExist:
                    pass
                
                return species_instance

            else:
                raise ValidationError('You can\'t submit this species at this moment')

def rename_species_original_submit(species_instance,request):
        with transaction.atomic():
            if species_instance.processing_status == 'current':
                species_instance.processing_status = 'historical'
                species_instance.save()
                #  send the rename species email notification
                send_species_rename_email_notification(request, species_instance)

                 # change current active conservation status of the original species to inactive
                try:
                    if species_instance.processing_status == 'historical':
                        species_cons_status = ConservationStatus.objects.get(species=species_instance, processing_status='approved')
                        if species_cons_status:
                            species_cons_status.customer_status='closed'
                            species_cons_status.processing_status='closed'
                            species_cons_status.save()
                            #add the log_user_action
                            species_cons_status.log_user_action(ConservationStatusUserAction.ACTION_CLOSE_CONSERVATIONSTATUS.format(species_cons_status.conservation_status_number),request)
                except ConservationStatus.DoesNotExist:
                    pass
                
                return species_instance

            else:
                raise ValidationError('You can\'t submit this species at this moment')