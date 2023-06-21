import logging
import datetime
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields.jsonb import JSONField
from boranga import exceptions
from boranga.components.main.models import (
    CommunicationsLogEntry, 
    UserAction,
    Document,
    RevisionedMixin,
)
from boranga.ledger_api_utils import retrieve_email_user
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from ledger_api_client.managed_models import SystemGroup
import json
from django.db import models,transaction
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from boranga.settings import (
    GROUP_NAME_ASSESSOR,
    GROUP_NAME_APPROVER,
    GROUP_NAME_EDITOR,
)

from boranga.components.species_and_communities.models import (
    GroupType,
    Region,
    District,
    Species,
    Community,
)

logger = logging.getLogger(__name__)

class PlanType(models.Model):
    """
    Type of Plan used in Conservation Plan"
    
    """
    plan_name = models.CharField(max_length=150, blank=True, null=True)
    valid_months = models.IntegerField(null=True,blank=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return self.plan_name


class ConservationPlan(models.Model):
    """
    Each Occurence of Species or community has one or more Conservation Plans

    """
    PROCESSING_STATUS_TEMP = 'temp'
    PROCESSING_STATUS_DRAFT = 'draft'
    PROCESSING_STATUS_WITH_ASSESSOR = 'with_assessor'
    PROCESSING_STATUS_WITH_REFERRAL = 'with_referral'
    PROCESSING_STATUS_WITH_APPROVER = 'with_approver'
    PROCESSING_STATUS_READY_FOR_AGENDA = 'ready_for_agenda'
    PROCESSING_STATUS_AWAITING_APPLICANT_RESPONSE = 'awaiting_applicant_respone'
    PROCESSING_STATUS_AWAITING_ASSESSOR_RESPONSE = 'awaiting_assessor_response'
    PROCESSING_STATUS_AWAITING_RESPONSES = 'awaiting_responses'
    PROCESSING_STATUS_APPROVED = 'approved'
    PROCESSING_STATUS_DECLINED = 'declined'
    PROCESSING_STATUS_DISCARDED = 'discarded'
    PROCESSING_STATUS_CLOSED = 'closed'
    PROCESSING_STATUS_CURRENT_WAITING_REPLACEMENT = 'current_waiting_replacement'
    PROCESSING_STATUS_PARTIALLY_APPROVED = 'partially_approved'
    PROCESSING_STATUS_PARTIALLY_DECLINED = 'partially_declined'
    PROCESSING_STATUS_CHOICES = ((PROCESSING_STATUS_DRAFT, 'Draft'),
                                 (PROCESSING_STATUS_WITH_ASSESSOR, 'With Assessor'),
                                 (PROCESSING_STATUS_WITH_REFERRAL, 'With Referral'),
                                 (PROCESSING_STATUS_WITH_APPROVER, 'With Approver'),
                                 (PROCESSING_STATUS_READY_FOR_AGENDA, 'Ready For Agenda'),
                                 (PROCESSING_STATUS_AWAITING_APPLICANT_RESPONSE, 'Awaiting Applicant Response'),
                                 (PROCESSING_STATUS_AWAITING_ASSESSOR_RESPONSE, 'Awaiting Assessor Response'),
                                 (PROCESSING_STATUS_AWAITING_RESPONSES, 'Awaiting Responses'),
                                 (PROCESSING_STATUS_APPROVED, 'Approved'),
                                 (PROCESSING_STATUS_DECLINED, 'Declined'),
                                 (PROCESSING_STATUS_DISCARDED, 'Discarded'),
                                 (PROCESSING_STATUS_CLOSED, 'DeListed'),
                                 (PROCESSING_STATUS_CURRENT_WAITING_REPLACEMENT, 'Cuurent Waiting Replacement'),
                                 (PROCESSING_STATUS_PARTIALLY_APPROVED, 'Partially Approved'),
                                 (PROCESSING_STATUS_PARTIALLY_DECLINED, 'Partially Declined'),
                                )
    RECURRENCE_PATTERNS = [(1, 'Month'), (2, 'Year')]
    
    APPLICATION_TYPE_CHOICES = (
        ('new_proposal', 'New Application'),
        ('amendment', 'Amendment'),
        ('renewal', 'Renewal'),
        ('external', 'External'),
    )

    RELATED_ITEM_CHOICES = [('species', 'Species'),('community', 'Community')]

    # group_type of application
    application_type = models.ForeignKey(GroupType, on_delete=models.SET_NULL, blank=True, null=True)
    #
    proposal_type = models.CharField('Application Status Type', max_length=40, choices=APPLICATION_TYPE_CHOICES,
                                        default=APPLICATION_TYPE_CHOICES[0][0])


    conservation_plan_number = models.CharField(max_length=9, blank=True, default='')
    plan_type = models.ForeignKey(PlanType, on_delete=models.SET_NULL, blank=True, null=True)
    wa_plan_number = models.CharField(max_length=100, blank=True, null=True)
    region = models.ForeignKey(Region, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, default=None, on_delete=models.SET_NULL, null=True, blank=True)
    effective_from = models.DateTimeField(null=True, blank=True)
    effective_to = models.DateTimeField(null=True, blank=True)
    next_review_date = models.DateField(null=True,blank=True)
    recurrence_pattern = models.SmallIntegerField(choices=RECURRENCE_PATTERNS,default=1)
    recurrence_schedule = models.IntegerField(null=True,blank=True)
    comment = models.CharField(max_length=512, blank=True, null=True)
    #species related conservation status
    # species = models.ManyToManyField(Species, on_delete=models.CASCADE , null=True, blank=True)

    #communties related conservation plan
    # community = models.ManyToManyField(Community, on_delete=models.CASCADE, null=True, blank=True)
    submitter = models.IntegerField(null=True)  # EmailUserRO
    lodgement_date = models.DateTimeField(blank=True, null=True)
    old_conservation_plan = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    assigned_officer = models.IntegerField(null=True) #EmailUserRO
    assigned_approver = models.IntegerField(null=True) #EmailUserRO
    approved_by = models.IntegerField(null=True) #EmailUserRO
    processing_status = models.CharField('Processing Status', max_length=30, choices=PROCESSING_STATUS_CHOICES,
                                         default=PROCESSING_STATUS_CHOICES[0][0])
    prev_processing_status = models.CharField(max_length=30, blank=True, null=True)
    proposed_decline_status = models.BooleanField(default=False)
    deficiency_data = models.TextField(null=True, blank=True) # deficiency comment
    assessor_data = models.TextField(null=True, blank=True)  # assessor comment
    # to store the proposed start and end date of proposal
    proposed_issuance_approval = JSONField(blank=True, null=True) # Not used in boranga as created another model to store the details
    approver_comment = models.TextField(blank=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.conservation_status_number)  # TODO: is the most appropriate?

    def save(self, *args, **kwargs):
        super(ConservationPlan, self).save(*args,**kwargs)
        if self.conservation_plan_number == '':
            new_conservation_plan_id = 'CP{}'.format(str(self.pk))
            self.conservation_plan_number = new_conservation_plan_id
            self.save()
    
    @property
    def reference(self):
        return '{}-{}'.format(self.conservation_plan_number,self.conservation_plan_number) #TODO : the second parameter is lodgement.sequence no. don't know yet what for species it should be

    @property
    def group_type(self):
        return self.application_type.get_name_display() # when the form is incomplete

    @property
    def applicant(self):
        if self.submitter:
            email_user = retrieve_email_user(self.submitter)
            return "{} {}".format(
                email_user.first_name,
                email_user.last_name)

    @property
    def applicant_email(self):
        if self.submitter:
            email_user = retrieve_email_user(self.submitter)
            return self.email_user.email

    @property
    def applicant_details(self):
        if self.submitter:
            email_user = retrieve_email_user(self.submitter)
            return "{} {}\n{}".format(
                email_user.first_name,
                email_user.last_name,
                email_user.addresses.all().first())

    @property
    def applicant_address(self):
        if self.submitter:
            email_user = retrieve_email_user(self.submitter)
            return email_user.residential_address

    @property
    def applicant_id(self):
        if self.submitter:
            email_user = retrieve_email_user(self.submitter)
            return self.email_user.id

    @property
    def applicant_type(self):
        if self.submitter:
            #return self.APPLICANT_TYPE_SUBMITTER
            return 'SUB'

    @property
    def applicant_field(self):
        # if self.org_applicant:
        #     return 'org_applicant'
        # elif self.proxy_applicant:
        #     return 'proxy_applicant'
        # else:
        #     return 'submitter'
        return 'submitter'
    
    @property
    def is_assigned(self):
        return self.assigned_officer is not None
    
    @property
    def can_officer_process(self):
        """
        :return: True if the application is in one of the processable status for Assessor role.
        """
        officer_view_state = ['draft','approved','declined','temp','discarded', 'closed']
        if self.processing_status in officer_view_state:
            return False
        else:
            return True
    
    @property
    def is_discardable(self):
        """
        An application can be discarded by a customer if:
        1 - It is a draft
        2- or if the application has been pushed back to the user
        """
        return self.processing_status == 'draft' or self.processing_status == 'awaiting_applicant_response'

    @property
    def is_deletable(self):
        """
        An application can be deleted only if it is a draft and it hasn't been lodged yet
        :return:
        """
        return self.processing_status == 'draft' and not self.conservation_plan_number
    
    @property
    def is_flora_application(self):
        if self.application_type.name==GroupType.GROUP_TYPE_FLORA:
            return True
        return False

    @property
    def is_fauna_application(self):
        if self.application_type.name==GroupType.GROUP_TYPE_FAUNA:
            return True
        return False

    @property
    def is_community_application(self):
        if self.application_type.name==GroupType.GROUP_TYPE_COMMUNITY:
            return True
        return False


class ConservationPlanSpecies(models.Model):
    """
    -Species added for a particular conservation plan
    -A Species can be added to multiple plans and vice versa

    """
    conservation_plan = models.ForeignKey(ConservationPlan, on_delete=models.CASCADE, null=True, blank=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, null=True, blank=True)
    # dates the species was added/removed from this table
    effective_from = models.DateTimeField(null=True, blank=True)
    effective_to = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.species)  # TODO: is the most appropriate?


class ConservationPlanCommunity(models.Model):
    """
    -Species added for a particular conservation plan
    -A Species can be added to multiple plans and vice versa

    """
    conservation_plan = models.ForeignKey(ConservationPlan, on_delete=models.CASCADE, null=True, blank=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True)
    # dates the species was added/removed from this table
    effective_from = models.DateTimeField(null=True, blank=True)
    effective_to = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.species)  # TODO: is the most appropriate?
    