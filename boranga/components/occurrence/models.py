import logging
import datetime
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
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
from multiselectfield import MultiSelectField
from django.db import models,transaction
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from boranga.settings import (
    GROUP_NAME_ASSESSOR,
    GROUP_NAME_APPROVER,
    GROUP_NAME_EDITOR,
)
from boranga.components.main.utils import get_department_user
from boranga.components.main.related_item import RelatedItem
from boranga.components.species_and_communities.models import (
    DocumentCategory,
    DocumentSubCategory,
    GroupType,
    Species,
    Community,
)
from boranga.components.conservation_status.models import ConservationStatus
from boranga.ordered_model import OrderedModel

logger = logging.getLogger(__name__)


class OccurrenceReport(models.Model):
    """
    Occurrence Report for any particular species or community

    Used by:
    - Occurrence
    """
    CUSTOMER_STATUS_DRAFT = 'draft'
    CUSTOMER_STATUS_WITH_ASSESSOR = 'with_assessor'
    CUSTOMER_STATUS_WITH_APPROVER = 'with_approver'
    CUSTOMER_STATUS_AMENDMENT_REQUIRED = 'amendment_required'
    CUSTOMER_STATUS_APPROVED = 'approved'
    CUSTOMER_STATUS_DECLINED = 'declined'
    CUSTOMER_STATUS_DISCARDED = 'discarded'
    CUSTOMER_STATUS_CLOSED = 'closed'
    CUSTOMER_STATUS_PARTIALLY_APPROVED = 'partially_approved'
    CUSTOMER_STATUS_PARTIALLY_DECLINED = 'partially_declined'
    CUSTOMER_STATUS_CHOICES = ((CUSTOMER_STATUS_DRAFT, 'Draft'),
                               (CUSTOMER_STATUS_WITH_ASSESSOR, 'Under Review'),
                               (CUSTOMER_STATUS_WITH_APPROVER, 'Under Review'),
                               (CUSTOMER_STATUS_AMENDMENT_REQUIRED, 'Amendment Required'),
                               (CUSTOMER_STATUS_APPROVED, 'Approved'),
                               (CUSTOMER_STATUS_DECLINED, 'Declined'),
                               (CUSTOMER_STATUS_DISCARDED, 'Discarded'),
                               (CUSTOMER_STATUS_CLOSED, 'DeListed'),
                               (CUSTOMER_STATUS_PARTIALLY_APPROVED, 'Partially Approved'),
                               (CUSTOMER_STATUS_PARTIALLY_DECLINED, 'Partially Declined'),
                               )

    # List of statuses from above that allow a customer to edit an application.
    CUSTOMER_EDITABLE_STATE = ['draft',
                                'amendment_required',
                            ]

    # List of statuses from above that allow a customer to view an application (read-only)
    CUSTOMER_VIEWABLE_STATE = ['with_assessor','with_approver','under_review', 'approved', 'declined','closed','partially_approved', 'partially_declined']

    PROCESSING_STATUS_TEMP = 'temp'
    PROCESSING_STATUS_DRAFT = 'draft'
    PROCESSING_STATUS_WITH_ASSESSOR = 'with_assessor'
    PROCESSING_STATUS_WITH_REFERRAL = 'with_referral'
    PROCESSING_STATUS_WITH_APPROVER = 'with_approver'
    PROCESSING_STATUS_AWAITING_APPLICANT_RESPONSE = 'awaiting_applicant_respone'
    PROCESSING_STATUS_AWAITING_ASSESSOR_RESPONSE = 'awaiting_assessor_response'
    PROCESSING_STATUS_AWAITING_RESPONSES = 'awaiting_responses'
    PROCESSING_STATUS_APPROVED = 'approved'
    PROCESSING_STATUS_DECLINED = 'declined'
    PROCESSING_STATUS_DISCARDED = 'discarded'
    PROCESSING_STATUS_CLOSED = 'closed'
    PROCESSING_STATUS_PARTIALLY_APPROVED = 'partially_approved'
    PROCESSING_STATUS_PARTIALLY_DECLINED = 'partially_declined'
    PROCESSING_STATUS_CHOICES = ((PROCESSING_STATUS_DRAFT, 'Draft'),
                                 (PROCESSING_STATUS_WITH_ASSESSOR, 'With Assessor'),
                                 (PROCESSING_STATUS_WITH_REFERRAL, 'With Referral'),
                                 (PROCESSING_STATUS_WITH_APPROVER, 'With Approver'),
                                 (PROCESSING_STATUS_AWAITING_APPLICANT_RESPONSE, 'Awaiting Applicant Response'),
                                 (PROCESSING_STATUS_AWAITING_ASSESSOR_RESPONSE, 'Awaiting Assessor Response'),
                                 (PROCESSING_STATUS_AWAITING_RESPONSES, 'Awaiting Responses'),
                                 (PROCESSING_STATUS_APPROVED, 'Approved'),
                                 (PROCESSING_STATUS_DECLINED, 'Declined'),
                                 (PROCESSING_STATUS_DISCARDED, 'Discarded'),
                                 (PROCESSING_STATUS_CLOSED, 'DeListed'),
                                 (PROCESSING_STATUS_PARTIALLY_APPROVED, 'Partially Approved'),
                                 (PROCESSING_STATUS_PARTIALLY_DECLINED, 'Partially Declined'),
                                )
    REVIEW_STATUS_CHOICES = (
        ('not_reviewed', 'Not Reviewed'), ('awaiting_amendments', 'Awaiting Amendments'), ('amended', 'Amended'),
        ('accepted', 'Accepted'))
    customer_status = models.CharField('Customer Status', max_length=40, choices=CUSTOMER_STATUS_CHOICES,
                                       default=CUSTOMER_STATUS_CHOICES[0][0])

    APPLICATION_TYPE_CHOICES = (
        ('new_proposal', 'New Application'),
        ('amendment', 'Amendment'),
        ('renewal', 'Renewal'),
        ('external', 'External'),
    )

    RELATED_ITEM_CHOICES = [('species', 'Species'),('community', 'Community'),('agendaitem', 'Meeting Agenda Item')]

    # group_type of report
    group_type = models.ForeignKey(GroupType, on_delete=models.SET_NULL, blank=True, null=True)
    #
    proposal_type = models.CharField('Application Status Type', max_length=40, choices=APPLICATION_TYPE_CHOICES,
                                        default=APPLICATION_TYPE_CHOICES[0][0])

    #species related occurrence
    species = models.ForeignKey(Species, on_delete=models.CASCADE , related_name="occurrence_report", null=True, blank=True)

    #communties related occurrence
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="occurrence_report", null=True, blank=True)

    occurrence_report_number = models.CharField(max_length=9, blank=True, default='')

    reported_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    effective_from = models.DateTimeField(null=True, blank=True)
    effective_to = models.DateTimeField(null=True, blank=True)
    submitter = models.IntegerField(null=True)  # EmailUserRO
    lodgement_date = models.DateTimeField(blank=True, null=True) # TODO confirm if proposed date is the same or different

    assigned_officer = models.IntegerField(null=True) #EmailUserRO
    assigned_approver = models.IntegerField(null=True) #EmailUserRO
    approved_by = models.IntegerField(null=True) #EmailUserRO
    # internal user who edits the approved conservation status(only specific fields)
    #modified_by = models.IntegerField(null=True) #EmailUserRO 
    processing_status = models.CharField('Processing Status', max_length=30, choices=PROCESSING_STATUS_CHOICES,
                                         default=PROCESSING_STATUS_CHOICES[0][0])
    prev_processing_status = models.CharField(max_length=30, blank=True, null=True)
    review_status = models.CharField('Review Status', max_length=30, choices=REVIEW_STATUS_CHOICES,
                                     default=REVIEW_STATUS_CHOICES[0][0])
    proposed_decline_status = models.BooleanField(default=False)
    deficiency_data = models.TextField(null=True, blank=True) # deficiency comment
    assessor_data = models.TextField(null=True, blank=True)  # assessor comment
    approver_comment = models.TextField(blank=True)
    internal_application = models.BooleanField(default=False)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.occurrence_report_number)  # TODO: is the most appropriate?

    def save(self, *args, **kwargs):
        super(OccurrenceReport, self).save(*args,**kwargs)
        if self.occurrence_report_number == '':
            new_occurrence_report_id = 'OCR{}'.format(str(self.pk))
            self.occurrence_report_number = new_occurrence_report_id
            self.save()
    
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
    def can_user_edit(self):
        """
        :return: True if the application is in one of the editable status.
        """
        return self.customer_status in self.CUSTOMER_EDITABLE_STATE

    @property
    def can_user_view(self):
        """
        :return: True if the application is in one of the approved status.
        """
        return self.customer_status in self.CUSTOMER_VIEWABLE_STATE

    @property
    def is_discardable(self):
        """
        An application can be discarded by a customer if:
        1 - It is a draft
        2- or if the application has been pushed back to the user
        """
        return self.customer_status == 'draft' or self.processing_status == 'awaiting_applicant_response'
    
    @property
    def is_flora_application(self):
        if self.group_type.name==GroupType.GROUP_TYPE_FLORA:
            return True
        return False

    @property
    def is_fauna_application(self):
        if self.group_type.name==GroupType.GROUP_TYPE_FAUNA:
            return True
        return False

    @property
    def is_community_application(self):
        if self.group_type.name==GroupType.GROUP_TYPE_COMMUNITY:
            return True
        return False


class LandForm(models.Model):
    """
    # Admin List

    Used by:
    - HabitatComposition

    """
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)

    class Meta:
        app_label = 'boranga'
        verbose_name = "Land Form"
        verbose_name_plural = "Land Forms"
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class RockType(models.Model):
    """
    # Admin List

    Used by:
    - HabitatComposition

    """
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)

    class Meta:
        app_label = 'boranga'
        verbose_name = "Rock Type"
        verbose_name_plural = "Rock Types"
        ordering = ['name']

    def __str__(self):
        return str(self.name)

class SoilType(models.Model):
    """
    # Admin List

    Used by:
    - HabitatComposition

    """
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)

    class Meta:
        app_label = 'boranga'
        verbose_name = "Soil Type"
        verbose_name_plural = "Soil Types"
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class SoilColour(models.Model):
    """
    # Admin List

    Used by:
    - HabitatComposition

    """
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)

    class Meta:
        app_label = 'boranga'
        verbose_name = "Soil Colour"
        verbose_name_plural = "Soil Colours"
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Drainage(models.Model):
    """
    # Admin List

    Used by:
    - HabitatComposition

    """
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)

    class Meta:
        app_label = 'boranga'
        verbose_name = "Drainage"
        verbose_name_plural = "Drainages"
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class SoilCondition(models.Model):
    """
    # Admin List

    Used by:
    - HabitatComposition

    """
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)

    class Meta:
        app_label = 'boranga'
        verbose_name = "Soil Condition"
        verbose_name_plural = "Soil Conditions"
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class HabitatComposition(models.Model):
    """
    Habitat data  for occurrence report

    Used for:
    - Occurrence Report
    Is:
    - Table
    """
    occurrence_report = models.ForeignKey(OccurrenceReport, on_delete=models.CASCADE, unique=True, null=True, related_name="habitat_composition")
    
    land_form = MultiSelectField(max_length=250, blank=True, choices=[(land_form_instance.id, land_form_instance.name) for land_form_instance in LandForm.objects.all()], null=True)
    rock_type = models.ForeignKey(RockType, on_delete=models.SET_NULL, null=True, blank=True)
    loose_rock_percent = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)])
    soil_type = models.ForeignKey(SoilType, on_delete=models.SET_NULL, null=True, blank=True)
    soil_colour = models.ForeignKey(SoilColour, on_delete=models.SET_NULL, null=True, blank=True)
    soil_condition = models.ForeignKey(SoilCondition, on_delete=models.SET_NULL, null=True, blank=True)
    drainage = models.ForeignKey(Drainage, on_delete=models.SET_NULL, null=True, blank=True)
    water_quality = models.CharField(max_length=500, null=True, blank=True)
    habitat_notes = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.occurrence_report)  # TODO: is the most appropriate?\


class HabitatCondition(models.Model):
    """
    Habitat Condition data for occurrence report

    Used for:
    - Occurrence Report
    Is:
    - Table
    """
    occurrence_report = models.ForeignKey(OccurrenceReport, on_delete=models.CASCADE, unique=True, null=True, related_name="habitat_condition")
    
    pristine = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)])
    excellent = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)])
    very_good = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)])
    good = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)])
    dehydrated = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)])
    completely_dehydrated = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.occurrence_report)


class Intensity(models.Model):
    """
    # Admin List

    Used by:
    - FireHistory

    """
    name = models.CharField(max_length=250, blank=False, null=False, unique=True)

    class Meta:
        app_label = 'boranga'
        verbose_name = "Intensity"
        verbose_name_plural = "Intensities"
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class FireHistory(models.Model):
    """
    Fire History data for occurrence report

    Used for:
    - Occurrence Report
    Is:
    - Table
    """
    occurrence_report = models.ForeignKey(OccurrenceReport, on_delete=models.CASCADE, unique=True, null=True, related_name="fire_history")
    last_fire_estimate = models.DateField(null=True, blank=True)
    intensity = models.ForeignKey(RockType, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.occurrence_report)
