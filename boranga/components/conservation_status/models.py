import datetime
from django.db import models
from boranga.components.main.models import (
    CommunicationsLogEntry, 
    UserAction,
    Document
)
from boranga.components.species_and_communities.models import(
    Species,
    Community,
)
import json
from django.db import models,transaction
from django.conf import settings
from django.core.files.storage import FileSystemStorage

private_storage = FileSystemStorage(location=settings.BASE_DIR+"/private-media/", base_url='/private-media/')


def update_species_conservation_status_comms_log_filename(instance, filename):
    return '{}/conservation_status/{}/communications/{}'.format(settings.MEDIA_APP_DIR, instance.log_entry.conservation_status.id,filename)

def update_conservation_status_comms_log_filename(instance, filename):
    return '{}/conservation_status/{}/communications/{}'.format(settings.MEDIA_APP_DIR, instance.log_entry.conservation_status.id,filename)


class ConservationList(models.Model):
    """

    NB: Can have multiple lists per species
    WAPEC       WA Priority Ecological Community List
    DBCA_RLE    Pre-BCA DBCA precursor to IUCN RLE
    WAPS        WA Priority Species List
    SPFN        Wildlife Conservation (Specially Protected Fauna) Notice, Schedules
    IUCN_RLE    IUCN Red List of Ecosystems
    IUCN2012    IUCN Red List Categories and Criteria v3.1(2001) 2nd edition (2012)
    IUCN2001    IUCN Red List Categories and Criteria v3.1(2001)
    EPBC        Environment Protection and Biodiversity Conservation Act 1999
    IUCN1994    IUCN Red List Categories v2.3 (1994)
    WAWCA       Wildlife Conservation Act 1950, Gazettal notice listing

    Has a:
    - N/A
    Used by:
    - SpeciesConservationStatus
    - CommunityConservationStatus
    - ConservationCategory
    - ConservationCriteria
    Is:
    - TBD
    """
    APPROVAL_LEVEL_CHOICES = (
        ('intermediate', 'Intermediate'),
        ('minister', 'Minister'),
    )

    code = models.CharField(max_length=64,
                            default="None")
    label = models.CharField(max_length=512,
                            default="None")
    applies_to_wa = models.BooleanField(default=False)
    applies_to_commonwealth = models.BooleanField(default=False)
    applies_to_international = models.BooleanField(default=False)
    applies_to_species = models.BooleanField(default=False)
    applies_to_communities = models.BooleanField(default=False)
    approval_level = models.CharField('Approval level', max_length=20, choices=APPROVAL_LEVEL_CHOICES,
                                        default=APPROVAL_LEVEL_CHOICES[0][0])

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.code)


class ConservationCategory(models.Model):
    """
    Dependent on Conservation List (FK)
    eg.:
    CR  Critically endangered fauna (S1)
    P1  Priority 1
    PD  Presumed Totally Destroyed
    P1  Priority 1
    EN  Endangered fauna (S2)
    P2  Priority 2
    

    Has a:
    - ConservationList
    Used by:
    - SpeciesConservationStatus
    - CommunityConservationStatus
    Is:
    - TBD
    """
    conservation_list = models.ForeignKey(ConservationList, on_delete=models.CASCADE, related_name="conservation_categories", null=True)
    code = models.CharField(max_length=64,
                            default="None")
    label = models.CharField(max_length=512,
                            default="None")

    class Meta:
        app_label = 'boranga'
        verbose_name = "Conservation Category"
        verbose_name_plural = "Conservation Categories"

    def __str__(self):
        return str(self.code)


class ConservationCriteria(models.Model):
    """
    Dependent on Conservation List (FK)

    Justification for listing as threatened (IUCN-how everything is defined)
    eg:
    A
    Ai
    Aii
    B
    Bi
    Bii
    NB: may have multiple of these per species
    Has a:
    - N/A
    Used by:
    - SpeciesConservationStatus
    - CommunityConservationStatus
    Is:
    - TBD
    """
    conservation_list = models.ForeignKey(ConservationList, on_delete=models.CASCADE, related_name="conservation_criterias", null=True)
    code = models.CharField(max_length=64)
    label = models.CharField(max_length=512,
                            default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.code)


class ConservationChangeCode(models.Model):
    """
    When the conservation status of a species/community is changed, it can be for a number of reasons. 
    These reasons are represented by change codes.
    """
    code = models.CharField(max_length=32,
                            default="None")
    label = models.CharField(max_length=512,
                            default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.code)


class ConservationStatus(models.Model):
    """
    Several lists with different attributes

    NB: Different lists has different different entries
    mainly interest in wa but must accomodte comm as well
    Has a:
    - ConservationChangeCode
    - ConservationList
    - ConservationCategory
    - ConservationCriteria
    Used by:
    - SpeciesConservationStatus
    - CommunityConservationStatus
    Is:
    - Abstract class
    """
    CUSTOMER_STATUS_DRAFT = 'draft'
    CUSTOMER_STATUS_WITH_ASSESSOR = 'with_assessor'
    CUSTOMER_STATUS_AMENDMENT_REQUIRED = 'amendment_required'
    CUSTOMER_STATUS_APPROVED = 'approved'
    CUSTOMER_STATUS_DECLINED = 'declined'
    CUSTOMER_STATUS_DISCARDED = 'discarded'
    CUSTOMER_STATUS_PARTIALLY_APPROVED = 'partially_approved'
    CUSTOMER_STATUS_PARTIALLY_DECLINED = 'partially_declined'
    CUSTOMER_STATUS_CHOICES = ((CUSTOMER_STATUS_DRAFT, 'Draft'),
                               (CUSTOMER_STATUS_WITH_ASSESSOR, 'Under Review'),
                               (CUSTOMER_STATUS_AMENDMENT_REQUIRED, 'Amendment Required'),
                               (CUSTOMER_STATUS_APPROVED, 'Approved'),
                               (CUSTOMER_STATUS_DECLINED, 'Declined'),
                               (CUSTOMER_STATUS_DISCARDED, 'Discarded'),
                               (CUSTOMER_STATUS_PARTIALLY_APPROVED, 'Partially Approved'),
                               (CUSTOMER_STATUS_PARTIALLY_DECLINED, 'Partially Declined'),
                               )

    # List of statuses from above that allow a customer to edit an application.
    CUSTOMER_EDITABLE_STATE = ['draft',
                                'amendment_required',
                            ]

    # List of statuses from above that allow a customer to view an application (read-only)
    CUSTOMER_VIEWABLE_STATE = ['with_assessor', 'under_review', 'approved', 'declined','partially_approved', 'partially_declined']

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
                                 (PROCESSING_STATUS_PARTIALLY_APPROVED, 'Partially Approved'),
                                 (PROCESSING_STATUS_PARTIALLY_DECLINED, 'Partially Declined'),
                                )
    REVIEW_STATUS_CHOICES = (
        ('not_reviewed', 'Not Reviewed'), ('awaiting_amendments', 'Awaiting Amendments'), ('amended', 'Amended'),
        ('accepted', 'Accepted'))
    customer_status = models.CharField('Customer Status', max_length=40, choices=CUSTOMER_STATUS_CHOICES,
                                       default=CUSTOMER_STATUS_CHOICES[0][0])

    RECURRENCE_PATTERNS = [(1, 'Month'), (2, 'Year')]
    change_code = models.ForeignKey(ConservationChangeCode, 
                                    on_delete=models.SET_NULL , blank=True, null=True)

    #species related conservation status
    species = models.ForeignKey(Species, on_delete=models.CASCADE , related_name="conservation_status", null=True, blank=True)

    #communties related conservation status
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="conservation_status", null=True, blank=True)

    conservation_status_number = models.CharField(max_length=9, blank=True, default='')

    # current listing details
    current_conservation_list = models.ForeignKey(ConservationList,
                                             on_delete=models.CASCADE, blank=True, null=True, related_name="curr_conservation_list")
    current_conservation_category = models.ForeignKey(ConservationCategory, 
                                              on_delete=models.SET_NULL, blank=True, null=True, related_name="curr_conservation_category")
    current_conservation_criteria = models.ManyToManyField(ConservationCriteria, blank=True, null=True, related_name="curr_conservation_criteria")
    # proposed listing details
    proposed_conservation_list = models.ForeignKey(ConservationList,
                                             on_delete=models.CASCADE, blank=True, null=True, related_name="prop_conservation_list")
    proposed_conservation_category = models.ForeignKey(ConservationCategory, 
                                              on_delete=models.SET_NULL, blank=True, null=True, related_name="prop_conservation_category")
    proposed_conservation_criteria = models.ManyToManyField(ConservationCriteria, blank=True, null=True, related_name="prop_conservation_criteria")
    comment = models.CharField(max_length=512, blank=True, null=True)
    review_date = models.DateField(null=True,blank=True)
    recurrence_pattern = models.SmallIntegerField(choices=RECURRENCE_PATTERNS,default=1)
    recurrence_schedule = models.IntegerField(null=True,blank=True)
    proposed_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    effective_from = models.DateTimeField(null=True, blank=True)
    effective_to = models.DateTimeField(null=True, blank=True)
    submitter = models.IntegerField(null=True)  # EmailUserRO
    lodgement_date = models.DateTimeField(blank=True, null=True) # TODO confirm if proposed date is the same or different

    assigned_officer = models.IntegerField(null=True) #EmailUserRO
    assigned_approver = models.IntegerField(null=True) #EmailUserRO
    approved_by = models.IntegerField(null=True) #EmailUserRO
    processing_status = models.CharField('Processing Status', max_length=30, choices=PROCESSING_STATUS_CHOICES,
                                         default=PROCESSING_STATUS_CHOICES[0][0])
    prev_processing_status = models.CharField(max_length=30, blank=True, null=True)
    review_status = models.CharField('Review Status', max_length=30, choices=REVIEW_STATUS_CHOICES,
                                     default=REVIEW_STATUS_CHOICES[0][0])

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.conservation_status_number)  # TODO: is the most appropriate?

    def save(self, *args, **kwargs):
        super(ConservationStatus, self).save(*args,**kwargs)
        if self.conservation_status_number == '':
            new_conservation_status_id = 'CS{}'.format(str(self.pk))
            self.conservation_status_number = new_conservation_status_id
            self.save()

    @property
    def reference(self):
        return '{}-{}'.format(self.conservation_status_number,self.conservation_status_number) #TODO : the second parameter is lodgement.sequence no. don't know yet what for species it should be

    @property
    def group_type(self):
        if self.species:
            return self.species.group_type.get_name_display()
        elif self.community:
            return self.community.group_type.get_name_display()

    def log_user_action(self, action, request):
        return ConservationStatusUserAction.log_action(self, action, request.user)

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


class ConservationStatusLogEntry(CommunicationsLogEntry):
    conservation_status = models.ForeignKey(ConservationStatus, related_name='comms_logs', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.reference, self.subject)

    class Meta:
        app_label = 'boranga'

    def save(self, **kwargs):
        # save the application reference if the reference not provided
        if not self.reference:
            self.reference = self.conservation_status.reference
        super(ConservationStatusLogEntry, self).save(**kwargs)


class ConservationStatusLogDocument(Document):
    log_entry = models.ForeignKey('ConservationStatusLogEntry',related_name='documents', on_delete=models.CASCADE)
    _file = models.FileField(upload_to=update_conservation_status_comms_log_filename, max_length=512, storage=private_storage)

    class Meta:
        app_label = 'boranga'


class ConservationStatusUserAction(UserAction):
    #ConservationStatus Proposal
    ACTION_EDIT_CONSERVATION_STATUS= "Edit Conservation Status {}"
    ACTION_LODGE_PROPOSAL = "Lodge proposal for conservation status {}"
    ACTION_ASSIGN_TO_ASSESSOR = "Assign proposal {} to {} as the assessor"
    ACTION_UNASSIGN_ASSESSOR = "Unassign assessor from proposal {}"
    ACTION_ASSIGN_TO_APPROVER = "Assign proposal {} to {} as the approver"
    ACTION_UNASSIGN_APPROVER = "Unassign approver from proposal {}"
    ACTION_DISCARD_PROPOSAL = "Discard proposal {}"
    ACTION_APPROVAL_LEVEL_DOCUMENT = "Assign Approval level document {}"
    
    # Assessors
    ACTION_SAVE_ASSESSMENT_ = "Save assessment {}"
    ACTION_CONCLUDE_ASSESSMENT_ = "Conclude assessment {}"
    ACTION_PROPOSED_APPROVAL = "Proposal {} has been proposed for approval"
    ACTION_PROPOSED_DECLINE = "Proposal {} has been proposed for decline"


    class Meta:
        app_label = 'boranga'
        ordering = ('-when',)

    @classmethod
    def log_action(cls, conservation_status, action, user):
        return cls.objects.create(
            conservation_status=conservation_status,
            who=user,
            what=str(action)
        )

    conservation_status= models.ForeignKey(ConservationStatus, related_name='action_logs', on_delete=models.CASCADE)



# class SpeciesConservationStatus(ConservationStatus):
#     """
#     Species Conservation Status
#     """
#     species = models.ForeignKey(Species, on_delete=models.CASCADE , related_name="conservation_status")
#     conservation_status_number = models.CharField(max_length=9, blank=True, default='')

#     class Meta:
#         app_label = 'boranga'

#     def __str__(self):
#         return(self.conservation_status_number)

#     def save(self, *args, **kwargs):
#         super(SpeciesConservationStatus, self).save(*args,**kwargs)
#         if self.conservation_status_number == '':
#             new_conservation_status_id = 'CS{}'.format(str(self.pk))
#             self.conservation_status_number = new_conservation_status_id
#             self.save()

#     @property
#     def reference(self):
#         return '{}-{}'.format(self.conservation_status_number,self.conservation_status_number) #TODO : the second parameter is lodgement.sequence no. don't know yet what for species it should be

#     def log_user_action(self, action, request):
#         return SpeciesConservationStatusUserAction.log_action(self, action, request.user)


# class CommunityConservationStatus(ConservationStatus):
#     """
#     Community Conservation Status
#     """
#     community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="conservation_status")
#     conservation_status_number = models.CharField(max_length=9, blank=True, default='')

#     class Meta:
#         app_label = 'boranga'

#     def __str__(self):
#         return(self.conservation_status_number)

#     def save(self, *args, **kwargs):
#         super(CommunityConservationStatus, self).save(*args,**kwargs)
#         if self.conservation_status_number == '':
#             new_conservation_status_id = 'CS{}'.format(str(self.pk))
#             self.conservation_status_number = new_conservation_status_id
#             self.save()
