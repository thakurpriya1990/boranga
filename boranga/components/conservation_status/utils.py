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
from boranga.components.conservation_status.models import(
    ConservationStatus,
    ConservationList,
    Species,
    Community,
    GroupType,
    ConservationStatusUserAction,
)


import logging
logger = logging.getLogger(__name__)

def cs_proposal_submit(cs_proposal,request):
        with transaction.atomic():
            if cs_proposal.can_user_edit:
                cs_proposal.submitter = request.user.id
                cs_proposal.lodgement_date = timezone.now()
                if (cs_proposal.amendment_requests):
                    qs = cs_proposal.amendment_requests.filter(status = "requested")
                    if (qs):
                        for q in qs:
                            q.status = 'amended'
                            q.save()

                # Create a log entry for the proposal
                cs_proposal.log_user_action(ConservationStatusUserAction.ACTION_LODGE_PROPOSAL.format(cs_proposal.id),request)
                # Create a log entry for the organisation
                #proposal.applicant.log_user_action(ProposalUserAction.ACTION_LODGE_APPLICATION.format(proposal.id),request)
                applicant_field=getattr(cs_proposal, cs_proposal.applicant_field)
                # TODO handle the error "'EmailUserRO' object has no attribute 'log_user_action'" for below
                #applicant_field.log_user_action(ConservationStatusUserAction.ACTION_LODGE_PROPOSAL.format(cs_proposal.id),request)

                
                ret1 = send_submit_email_notification(request, cs_proposal)
                ret2 = send_external_submit_email_notification(request, cs_proposal)

                #cs_proposal.save_form_tabs(request)
                if ret1 and ret2:
                    cs_proposal.processing_status = 'with_assessor'
                    cs_proposal.customer_status = 'with_assessor'
                    #cs_proposal.documents.all().update(can_delete=False)
                    cs_proposal.save()
                else:
                    raise ValidationError('An error occurred while submitting proposal (Submit email notifications failed)')
                
                return cs_proposal

            else:
                raise ValidationError('You can\'t edit this proposal at this moment')
