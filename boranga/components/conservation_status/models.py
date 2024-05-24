import json
import logging
from datetime import timedelta

import reversion
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models, transaction
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from ledger_api_client.managed_models import SystemGroup

from boranga import exceptions
from boranga.components.conservation_status.email import (
    send_approver_approve_email_notification,
    send_approver_decline_email_notification,
    send_assessor_ready_for_agenda_email_notification,
    send_conservation_status_amendment_email_notification,
    send_conservation_status_approval_email_notification,
    send_conservation_status_decline_email_notification,
    send_conservation_status_referral_complete_email_notification,
    send_conservation_status_referral_email_notification,
    send_conservation_status_referral_recall_email_notification,
    send_proposal_approver_sendback_email_notification,
)
from boranga.components.main.models import (
    CommunicationsLogEntry,
    Document,
    RevisionedMixin,
    UserAction,
)
from boranga.components.main.related_item import RelatedItem
from boranga.components.main.utils import get_department_user
from boranga.components.species_and_communities.models import (
    Community,
    DocumentCategory,
    DocumentSubCategory,
    GroupType,
    Species,
)
from boranga.ledger_api_utils import retrieve_email_user
from boranga.settings import (
    GROUP_NAME_CONSERVATION_STATUS_APPROVER,
    GROUP_NAME_CONSERVATION_STATUS_ASSESSOR,
)

logger = logging.getLogger(__name__)

private_storage = FileSystemStorage(
    location=settings.BASE_DIR + "/private-media/", base_url="/private-media/"
)


def update_species_conservation_status_comms_log_filename(instance, filename):
    return (
        f"{settings.MEDIA_APP_DIR}/conservation_status/{instance.log_entry.conservation_status.id}"
        f"/communications/{filename}"
    )


def update_conservation_status_comms_log_filename(instance, filename):
    return (
        f"{settings.MEDIA_APP_DIR}/conservation_status/{instance.log_entry.conservation_status.id}"
        f"/communications/{filename}"
    )


def update_referral_doc_filename(instance, filename):
    return "{}/conservation_status/{}/referral/{}".format(
        settings.MEDIA_APP_DIR, instance.referral.proposal.id, filename
    )


def update_conservation_status_amendment_request_doc_filename(instance, filename):
    return (
        f"conservation_status/{instance.conservation_status_amendment_request.conservation_status.id}"
        f"/amendment_request_documents/{filename}"
    )


def update_conservation_status_doc_filename(instance, filename):
    return f"{settings.MEDIA_APP_DIR}/conservation_status/{instance.conservation_status.id}/documents/{filename}"


class AbstractConservationList(models.Model):
    code = models.CharField(max_length=64)
    label = models.CharField(max_length=512)
    applies_to_species = models.BooleanField(default=False)
    applies_to_communities = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = "boranga"
        ordering = ["code"]

    @classmethod
    def get_lists_dict(
        cls: models.base.ModelBase, group_type: str | int | None
    ) -> list:
        try:
            if group_type and isinstance(group_type, int):
                group_type = GroupType.objects.get(id=group_type)
            elif group_type and isinstance(group_type, str):
                group_type = GroupType.objects.get(name=group_type)
        except GroupType.DoesNotExist:
            logger.warning(f"GroupType {group_type} does not exist")
            return []

        lists = cls.objects.values("id", "code")
        if group_type and group_type.name == GroupType.GROUP_TYPE_COMMUNITY:
            lists = lists.filter(applies_to_communities=True)
        elif group_type and group_type.name in [
            GroupType.GROUP_TYPE_FLORA,
            GroupType.GROUP_TYPE_FAUNA,
        ]:
            lists = lists.filter(applies_to_species=True)
        return list(lists)

    def __str__(self):
        return f"{self.code} - {self.label}"


class AbstractConservationCategory(models.Model):
    code = models.CharField(max_length=64)
    label = models.CharField(max_length=512)

    class Meta:
        abstract = True
        app_label = "boranga"
        ordering = ["code"]

    def __str__(self):
        return str(self.code)


class WAPriorityList(AbstractConservationList):

    class Meta:
        ordering = ["code"]
        app_label = "boranga"
        verbose_name = "WA Priority List"


class WAPriorityCategory(AbstractConservationCategory):
    wa_priority_lists = models.ManyToManyField(
        WAPriorityList, related_name="wa_priority_categories"
    )

    class Meta:
        ordering = ["code"]
        app_label = "boranga"
        verbose_name = "WA Priority Category"
        verbose_name_plural = "WA Priority Categories"

    @classmethod
    def get_categories_dict(
        cls: models.base.ModelBase, group_type: str | int | None
    ) -> list:
        try:
            if group_type and isinstance(group_type, int):
                group_type = GroupType.objects.get(id=group_type)
            elif group_type and isinstance(group_type, str):
                group_type = GroupType.objects.get(name=group_type)
        except GroupType.DoesNotExist:
            logger.warning(f"GroupType {group_type} does not exist")
            return []
        wa_priority_categories = []
        wa_priority_categories_qs = WAPriorityCategory.objects.only("id", "code")
        if group_type and group_type.name == GroupType.GROUP_TYPE_COMMUNITY:
            wa_priority_categories_qs = wa_priority_categories_qs.filter(
                wa_priority_lists__applies_to_communities=True
            )
        elif group_type and group_type.name in [
            GroupType.GROUP_TYPE_FLORA,
            GroupType.GROUP_TYPE_FAUNA,
        ]:
            wa_priority_categories_qs = wa_priority_categories_qs.filter(
                wa_priority_lists__applies_to_species=True
            )
        for wa_priority_category in wa_priority_categories_qs.distinct():
            list_ids = list(
                WAPriorityList.objects.filter(
                    wa_priority_categories=wa_priority_category.id
                ).values_list("id", flat=True)
            )
            wa_priority_categories.append(
                {
                    "id": wa_priority_category.id,
                    "code": wa_priority_category.code,
                    "list_ids": list_ids,
                }
            )
        return wa_priority_categories


class WALegislativeList(AbstractConservationList):

    class Meta:
        ordering = ["code"]
        app_label = "boranga"
        verbose_name = "WA Legislative List"


class WALegislativeCategory(AbstractConservationCategory):
    wa_legislative_lists = models.ManyToManyField(
        WALegislativeList, related_name="wa_legislative_categories"
    )

    class Meta:
        ordering = ["code"]
        app_label = "boranga"
        verbose_name = "WA Legislative Category"
        verbose_name_plural = "WA Legislative Categories"

    @classmethod
    def get_categories_dict(
        cls: models.base.ModelBase, group_type: str | int | None
    ) -> list:
        try:
            if group_type and isinstance(group_type, int):
                group_type = GroupType.objects.get(id=group_type)
            elif group_type and isinstance(group_type, str):
                group_type = GroupType.objects.get(name=group_type)
        except GroupType.DoesNotExist:
            logger.warning(f"GroupType {group_type} does not exist")
            return []
        wa_legislative_categories = []
        wa_legislative_categories_qs = WALegislativeCategory.objects.only("id", "code")
        if group_type and group_type.name == GroupType.GROUP_TYPE_COMMUNITY:
            wa_legislative_categories_qs = wa_legislative_categories_qs.filter(
                wa_legislative_lists__applies_to_communities=True
            )
        elif group_type and group_type.name in [
            GroupType.GROUP_TYPE_FLORA,
            GroupType.GROUP_TYPE_FAUNA,
        ]:
            wa_legislative_categories_qs = wa_legislative_categories_qs.filter(
                wa_legislative_lists__applies_to_species=True
            )
        for wa_legislative_category in wa_legislative_categories_qs.distinct():
            list_ids = list(
                WALegislativeList.objects.filter(
                    wa_legislative_categories=wa_legislative_category.id
                ).values_list("id", flat=True)
            )
            wa_legislative_categories.append(
                {
                    "id": wa_legislative_category.id,
                    "code": wa_legislative_category.code,
                    "list_ids": list_ids,
                }
            )
        return wa_legislative_categories


class CommonwealthConservationList(AbstractConservationList):

    class Meta:
        ordering = ["code"]
        app_label = "boranga"
        verbose_name = "Commonwealth Conservation List"


class ConservationChangeCode(models.Model):
    """
    When the conservation status of a species/community is changed, it can be for a number of reasons.
    These reasons are represented by change codes.
    """

    code = models.CharField(max_length=32)
    label = models.CharField(max_length=512)

    class Meta:
        app_label = "boranga"

    def __str__(self):
        return str(self.code)

    @classmethod
    def get_delisted_change_code(cls):
        return cls.objects.get(code=settings.CONSERVATION_CHANGE_CODE_DELIST)


class IUCNVersion(models.Model):
    """
    IUCN Version while approving the List
    """

    code = models.CharField(max_length=32, default="None")
    label = models.CharField(max_length=512, default="None")

    class Meta:
        app_label = "boranga"

    def __str__(self):
        return str(self.code)


class ConservationStatus(RevisionedMixin):
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
    """

    CUSTOMER_STATUS_DRAFT = "draft"
    CUSTOMER_STATUS_WITH_ASSESSOR = "with_assessor"
    CUSTOMER_STATUS_READY_FOR_AGENDA = "ready_for_agenda"
    CUSTOMER_STATUS_AMENDMENT_REQUIRED = "amendment_required"
    CUSTOMER_STATUS_APPROVED = "approved"
    CUSTOMER_STATUS_DECLINED = "declined"
    CUSTOMER_STATUS_DISCARDED = "discarded"
    CUSTOMER_STATUS_CLOSED = "closed"
    CUSTOMER_STATUS_PARTIALLY_APPROVED = "partially_approved"
    CUSTOMER_STATUS_PARTIALLY_DECLINED = "partially_declined"
    CUSTOMER_STATUS_CHOICES = (
        (CUSTOMER_STATUS_DRAFT, "Draft"),
        (CUSTOMER_STATUS_WITH_ASSESSOR, "Under Review"),
        (CUSTOMER_STATUS_READY_FOR_AGENDA, "In Meeting"),
        (CUSTOMER_STATUS_AMENDMENT_REQUIRED, "Amendment Required"),
        (CUSTOMER_STATUS_APPROVED, "Approved"),
        (CUSTOMER_STATUS_DECLINED, "Declined"),
        (CUSTOMER_STATUS_DISCARDED, "Discarded"),
        (CUSTOMER_STATUS_CLOSED, "DeListed"),
        (CUSTOMER_STATUS_PARTIALLY_APPROVED, "Partially Approved"),
        (CUSTOMER_STATUS_PARTIALLY_DECLINED, "Partially Declined"),
    )

    # List of statuses from above that allow a customer to edit an application.
    CUSTOMER_EDITABLE_STATE = [
        "draft",
        "amendment_required",
    ]

    # List of statuses from above that allow a customer to view an application (read-only)
    CUSTOMER_VIEWABLE_STATE = [
        "with_assessor",
        "ready_for_agenda",
        "under_review",
        "approved",
        "declined",
        "closed",
        "partially_approved",
        "partially_declined",
    ]

    PROCESSING_STATUS_TEMP = "temp"
    PROCESSING_STATUS_DRAFT = "draft"
    PROCESSING_STATUS_WITH_ASSESSOR = "with_assessor"
    PROCESSING_STATUS_WITH_REFERRAL = "with_referral"
    PROCESSING_STATUS_WITH_APPROVER = "with_approver"
    PROCESSING_STATUS_READY_FOR_AGENDA = "ready_for_agenda"
    PROCESSING_STATUS_AWAITING_APPLICANT_RESPONSE = "awaiting_applicant_respone"
    PROCESSING_STATUS_AWAITING_ASSESSOR_RESPONSE = "awaiting_assessor_response"
    PROCESSING_STATUS_AWAITING_RESPONSES = "awaiting_responses"
    PROCESSING_STATUS_APPROVED = "approved"
    PROCESSING_STATUS_DECLINED = "declined"
    PROCESSING_STATUS_DISCARDED = "discarded"
    PROCESSING_STATUS_CLOSED = "closed"
    PROCESSING_STATUS_PARTIALLY_APPROVED = "partially_approved"
    PROCESSING_STATUS_PARTIALLY_DECLINED = "partially_declined"
    PROCESSING_STATUS_CHOICES = (
        (PROCESSING_STATUS_DRAFT, "Draft"),
        (PROCESSING_STATUS_WITH_ASSESSOR, "With Assessor"),
        (PROCESSING_STATUS_WITH_REFERRAL, "With Referral"),
        (PROCESSING_STATUS_WITH_APPROVER, "With Approver"),
        (PROCESSING_STATUS_READY_FOR_AGENDA, "Ready For Agenda"),
        (PROCESSING_STATUS_AWAITING_APPLICANT_RESPONSE, "Awaiting Applicant Response"),
        (PROCESSING_STATUS_AWAITING_ASSESSOR_RESPONSE, "Awaiting Assessor Response"),
        (PROCESSING_STATUS_AWAITING_RESPONSES, "Awaiting Responses"),
        (PROCESSING_STATUS_APPROVED, "Approved"),
        (PROCESSING_STATUS_DECLINED, "Declined"),
        (PROCESSING_STATUS_DISCARDED, "Discarded"),
        (PROCESSING_STATUS_CLOSED, "DeListed"),
        (PROCESSING_STATUS_PARTIALLY_APPROVED, "Partially Approved"),
        (PROCESSING_STATUS_PARTIALLY_DECLINED, "Partially Declined"),
    )
    REVIEW_STATUS_CHOICES = (
        ("not_reviewed", "Not Reviewed"),
        ("awaiting_amendments", "Awaiting Amendments"),
        ("amended", "Amended"),
        ("accepted", "Accepted"),
    )
    customer_status = models.CharField(
        "Customer Status",
        max_length=40,
        choices=CUSTOMER_STATUS_CHOICES,
        default=CUSTOMER_STATUS_CHOICES[0][0],
    )

    RECURRENCE_PATTERNS = [(1, "Month"), (2, "Year")]
    change_code = models.ForeignKey(
        ConservationChangeCode, on_delete=models.SET_NULL, blank=True, null=True
    )
    change_date = models.DateField(null=True, blank=True)

    APPLICATION_TYPE_CHOICES = (
        ("new_proposal", "New Application"),
        ("amendment", "Amendment"),
        ("renewal", "Renewal"),
        ("external", "External"),
    )

    RELATED_ITEM_CHOICES = [
        ("species", "Species"),
        ("community", "Community"),
        ("agendaitem", "Meeting Agenda Item"),
    ]

    # group_type of application
    application_type = models.ForeignKey(
        GroupType, on_delete=models.SET_NULL, blank=True, null=True
    )
    #
    proposal_type = models.CharField(
        "Application Status Type",
        max_length=40,
        choices=APPLICATION_TYPE_CHOICES,
        default=APPLICATION_TYPE_CHOICES[0][0],
    )

    # species related conservation status
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="conservation_status",
        null=True,
        blank=True,
    )

    # communties related conservation status
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="conservation_status",
        null=True,
        blank=True,
    )

    conservation_status_number = models.CharField(max_length=9, blank=True, default="")

    # Conservation Lists and Categories
    wa_priority_list = models.ForeignKey(
        WAPriorityList,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="curr_wa_priority_list",
    )
    wa_priority_category = models.ForeignKey(
        WAPriorityCategory,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="curr_wa_priority_category",
    )
    wa_legislative_list = models.ForeignKey(
        WALegislativeList,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="curr_wa_legislative_list",
    )
    wa_legislative_category = models.ForeignKey(
        WALegislativeCategory,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="curr_wa_legislative_category",
    )
    commonwealth_conservation_list = models.ForeignKey(
        CommonwealthConservationList,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="curr_commonwealth_conservation_list",
    )
    international_conservation = models.CharField(max_length=100, blank=True, null=True)
    conservation_criteria = models.CharField(max_length=100, blank=True, null=True)

    # Conservation Lists and Categories (from a meeting)
    recommended_wa_priority_list = models.ForeignKey(
        WAPriorityList,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    recommended_wa_priority_category = models.ForeignKey(
        WAPriorityCategory,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    recommended_wa_legislative_list = models.ForeignKey(
        WALegislativeList,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    recommended_wa_legislative_category = models.ForeignKey(
        WALegislativeCategory,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    recommended_commonwealth_conservation_list = models.ForeignKey(
        CommonwealthConservationList,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    recommended_international_conservation = models.CharField(
        max_length=100, blank=True, null=True
    )
    recommended_conservation_criteria = models.CharField(
        max_length=100, blank=True, null=True
    )

    APPROVAL_LEVEL_INTERMEDIATE = "intermediate"
    APPROVAL_LEVEL_MINISTER = "minister"
    APPROVAL_LEVEL_CHOICES = (
        (APPROVAL_LEVEL_INTERMEDIATE, "Intermediate"),
        (APPROVAL_LEVEL_MINISTER, "Ministerial"),
    )

    approval_level = models.CharField(
        max_length=20,
        choices=APPROVAL_LEVEL_CHOICES,
        null=True,
    )

    iucn_version = models.ForeignKey(
        IUCNVersion,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="iucn_version",
    )
    comment = models.CharField(max_length=512, blank=True, null=True)
    review_due_date = models.DateField(null=True, blank=True)
    review_date = models.DateField(null=True, blank=True)
    reviewed_by = models.IntegerField(null=True)  # EmailUserRO
    recurrence_pattern = models.SmallIntegerField(
        choices=RECURRENCE_PATTERNS, default=1
    )
    recurrence_schedule = models.IntegerField(null=True, blank=True)
    proposed_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    effective_from = models.DateField(null=True, blank=True)
    effective_to = models.DateField(null=True, blank=True)
    submitter = models.IntegerField(null=True)  # EmailUserRO
    lodgement_date = models.DateTimeField(
        blank=True, null=True
    )  # TODO confirm if proposed date is the same or different

    assigned_officer = models.IntegerField(null=True)  # EmailUserRO
    assigned_approver = models.IntegerField(null=True)  # EmailUserRO
    approved_by = models.IntegerField(null=True)  # EmailUserRO
    processing_status = models.CharField(
        "Processing Status",
        max_length=30,
        choices=PROCESSING_STATUS_CHOICES,
        default=PROCESSING_STATUS_CHOICES[0][0],
    )
    prev_processing_status = models.CharField(max_length=30, blank=True, null=True)
    review_status = models.CharField(
        "Review Status",
        max_length=30,
        choices=REVIEW_STATUS_CHOICES,
        default=REVIEW_STATUS_CHOICES[0][0],
    )
    proposed_decline_status = models.BooleanField(default=False)
    deficiency_data = models.TextField(null=True, blank=True)  # deficiency comment
    assessor_data = models.TextField(null=True, blank=True)  # assessor comment
    approver_comment = models.TextField(blank=True)
    internal_application = models.BooleanField(default=False)

    # Date first listed
    listing_date = models.DateField(null=True, blank=True)

    class Meta:
        app_label = "boranga"

    def __str__(self):
        return str(self.conservation_status_number)

    def save(self, *args, **kwargs):
        if self.conservation_status_number == "":
            force_insert = kwargs.pop("force_insert", False)
            super().save(no_revision=True, force_insert=force_insert)
            new_conservation_status_id = f"CS{str(self.pk)}"
            self.conservation_status_number = new_conservation_status_id
            self.save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    @property
    def reference(self):
        return f"{self.conservation_status_number}"

    @property
    def group_type(self):
        if self.species:
            return self.species.group_type.get_name_display()
        elif self.community:
            return self.community.group_type.get_name_display()
        else:
            return (
                self.application_type.get_name_display()
            )  # when the form is incomplete

    @property
    def applicant(self):
        if self.submitter:
            email_user = retrieve_email_user(self.submitter)
            return f"{email_user.first_name} {email_user.last_name}"

    @property
    def applicant_email(self):
        if self.submitter:
            return self.email_user.email

    @property
    def applicant_details(self):
        if self.submitter:
            email_user = retrieve_email_user(self.submitter)
            return f"{email_user.first_name} {email_user.last_name}"

    @property
    def applicant_address(self):
        if self.submitter:
            email_user = retrieve_email_user(self.submitter)
            return email_user.residential_address

    @property
    def applicant_id(self):
        if self.submitter:
            return self.email_user.id

    @property
    def applicant_type(self):
        if self.submitter:
            # return self.APPLICANT_TYPE_SUBMITTER
            return "SUB"

    @property
    def applicant_field(self):
        return "submitter"

    def log_user_action(self, action, request):
        return ConservationStatusUserAction.log_action(self, action, request.user.id)

    @property
    def is_assigned(self):
        return self.assigned_officer is not None

    @property
    def can_officer_process(self):
        officer_view_state = [
            ConservationStatus.PROCESSING_STATUS_DRAFT,
            ConservationStatus.PROCESSING_STATUS_APPROVED,
            ConservationStatus.PROCESSING_STATUS_DECLINED,
            ConservationStatus.PROCESSING_STATUS_TEMP,
            ConservationStatus.PROCESSING_STATUS_DISCARDED,
            ConservationStatus.PROCESSING_STATUS_CLOSED,
        ]
        return self.processing_status not in officer_view_state

    @property
    def can_approver_process(self):
        approver_process_state = [
            ConservationStatus.PROCESSING_STATUS_READY_FOR_AGENDA,
            ConservationStatus.PROCESSING_STATUS_WITH_APPROVER,
        ]
        return self.processing_status in approver_process_state

    @property
    def can_officer_edit(self):
        officer_edit_state = [ConservationStatus.PROCESSING_STATUS_APPROVED]
        return self.processing_status in officer_edit_state

    @property
    def can_user_edit(self):
        return self.customer_status in self.CUSTOMER_EDITABLE_STATE

    @property
    def can_user_view(self):
        return self.customer_status in self.CUSTOMER_VIEWABLE_STATE

    @property
    def is_discardable(self):
        return self.customer_status == ConservationStatus.CUSTOMER_STATUS_DRAFT

    @property
    def is_deletable(self):
        return (
            self.customer_status == ConservationStatus.CUSTOMER_STATUS_DRAFT
            and not self.conservation_status_number
        )

    @property
    def latest_referrals(self):
        return self.referrals.all()[: settings.RECENT_REFERRAL_COUNT]

    @property
    def is_flora_application(self):
        return self.application_type.name == GroupType.GROUP_TYPE_FLORA

    @property
    def is_fauna_application(self):
        return self.application_type.name == GroupType.GROUP_TYPE_FAUNA

    @property
    def is_community_application(self):
        return self.application_type.name == GroupType.GROUP_TYPE_COMMUNITY

    @property
    def allowed_assessors(self):
        group = None
        if self.processing_status in [
            ConservationStatus.PROCESSING_STATUS_READY_FOR_AGENDA,
            ConservationStatus.PROCESSING_STATUS_WITH_APPROVER,
            ConservationStatus.PROCESSING_STATUS_APPROVED,
        ]:
            group = self.get_approver_group()
        elif self.processing_status in [
            ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR,
            ConservationStatus.PROCESSING_STATUS_WITH_REFERRAL,
        ]:
            group = self.get_assessor_group()
        users = (
            list(
                map(
                    lambda id: retrieve_email_user(id),
                    group.get_system_group_member_ids(),
                )
            )
            if group
            else []
        )
        return users

    def get_assessor_group(self):
        return SystemGroup.objects.get(name=GROUP_NAME_CONSERVATION_STATUS_ASSESSOR)

    def get_approver_group(self):
        return SystemGroup.objects.get(name=GROUP_NAME_CONSERVATION_STATUS_APPROVER)

    @property
    def assessor_recipients(self):
        recipients = []
        group_ids = self.get_assessor_group().get_system_group_member_ids()
        for id in group_ids:
            logger.info(id)
            recipients.append(EmailUser.objects.get(id=id).email)
        return recipients

    @property
    def approver_recipients(self):
        recipients = []
        group_ids = self.get_approver_group().get_system_group_member_ids()
        for id in group_ids:
            logger.info(id)
            recipients.append(EmailUser.objects.get(id=id).email)
        return recipients

    @property
    def current_conservation_status(self):
        current_conservation_statuses = ConservationStatus.objects.filter(
            species=self.species,
            processing_status=ConservationStatus.PROCESSING_STATUS_APPROVED,
        )
        if current_conservation_statuses.count() > 1:
            logger.warning(
                f"Multiple approved conservation statuses for {self.species}"
            )

        return current_conservation_statuses.first()

    # Check if the user is member of assessor group for the CS Proposal
    def is_assessor(self, user):
        if user.is_superuser:
            return True

        return user.id in self.get_assessor_group().get_system_group_member_ids()

    # Check if the user is member of assessor group for the CS Proposal
    def is_approver(self, user):
        if user.is_superuser:
            return True

        return user.id in self.get_assessor_group().get_system_group_member_ids()

    def can_assess(self, user):
        if self.processing_status in [
            ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR,
            ConservationStatus.PROCESSING_STATUS_WITH_REFERRAL,
        ]:
            return user.id in self.get_assessor_group().get_system_group_member_ids()
        elif self.processing_status in [
            ConservationStatus.PROCESSING_STATUS_READY_FOR_AGENDA,
            ConservationStatus.PROCESSING_STATUS_APPROVED,
        ]:
            return user.id in self.get_approver_group().get_system_group_member_ids()
        else:
            return False

    def assessor_comments_view(self, user):
        if self.processing_status in [
            ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR,
            ConservationStatus.PROCESSING_STATUS_WITH_REFERRAL,
            ConservationStatus.PROCESSING_STATUS_READY_FOR_AGENDA,
            ConservationStatus.PROCESSING_STATUS_WITH_APPROVER,
        ]:
            try:
                referral = ConservationStatusReferral.objects.get(
                    conservation_status=self, referral=user.id
                )
            except ConservationStatusReferral.DoesNotExist:
                referral = None

            if referral:
                return True

            elif user.id in self.get_assessor_group().get_system_group_member_ids():
                return True

            elif user.id in self.get_approver_group().get_system_group_member_ids():
                return True
            else:
                return False

    @property
    def status_without_assessor(self):
        status_without_assessor = [
            ConservationStatus.PROCESSING_STATUS_WITH_APPROVER,
            ConservationStatus.PROCESSING_STATUS_APPROVED,
            ConservationStatus.PROCESSING_STATUS_CLOSED,
            ConservationStatus.PROCESSING_STATUS_DECLINED,
            ConservationStatus.PROCESSING_STATUS_DRAFT,
            ConservationStatus.PROCESSING_STATUS_WITH_REFERRAL,
        ]

        return self.processing_status in status_without_assessor

    def has_assessor_mode(self, user):
        status_without_assessor = [
            ConservationStatus.PROCESSING_STATUS_WITH_APPROVER,
            ConservationStatus.PROCESSING_STATUS_APPROVED,
            ConservationStatus.PROCESSING_STATUS_CLOSED,
            ConservationStatus.PROCESSING_STATUS_DECLINED,
            ConservationStatus.PROCESSING_STATUS_DRAFT,
        ]
        if self.processing_status in status_without_assessor:
            # For Editing the 'Approved' conservation status for authorised group
            if self.processing_status == ConservationStatus.PROCESSING_STATUS_APPROVED:
                return (
                    user.id in self.get_approver_group().get_system_group_member_ids()
                )
            else:
                return False

        else:
            if self.assigned_officer:
                if self.assigned_officer == user.id:
                    return (
                        user.id
                        in self.get_assessor_group().get_system_group_member_ids()
                    )
                else:
                    return False
            else:
                return (
                    user.id in self.get_assessor_group().get_system_group_member_ids()
                )

    @property
    def can_view_recommended(self):
        # TODO: If we stick with the decision to never show the recommended fields
        # then remove the from the cosebase entirely.
        return False
        # return self.processing_status in ["ready_for_agenda", "approved", "closed"]

    def can_edit_recommended(self, user):
        recommended_edit_status = [
            ConservationStatus.PROCESSING_STATUS_READY_FOR_AGENDA
        ]
        if self.processing_status in recommended_edit_status:
            if self.assigned_officer:
                if self.assigned_officer == user.id:
                    return (
                        user.id
                        in self.get_assessor_group().get_system_group_member_ids()
                    )
                else:
                    return False
            else:
                return (
                    user.id in self.get_assessor_group().get_system_group_member_ids()
                )
        else:
            return False

    @transaction.atomic
    def assign_officer(self, request, officer):
        if not self.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        if not self.can_assess(officer):
            raise ValidationError(
                f"Officer with id {officer} is not authorised to be assigned to this conservation status"
            )

        if self.processing_status in [
            ConservationStatus.PROCESSING_STATUS_READY_FOR_AGENDA,
            ConservationStatus.PROCESSING_STATUS_WITH_APPROVER,
        ]:
            if officer == self.assigned_approver:
                return

            self.assigned_approver = officer.id
            self.save()

            # Create a log entry for the conservation status
            self.log_user_action(
                ConservationStatusUserAction.ACTION_ASSIGN_TO_APPROVER.format(
                    self.conservation_status_number,
                    f"{officer.get_full_name()}({officer.email})",
                ),
                request,
            )

            # TODO: Create a log entry for the user

        if self.processing_status in [
            ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR,
            ConservationStatus.PROCESSING_STATUS_WITH_REFERRAL,
        ]:
            if officer == self.assigned_officer:
                return

            self.assigned_officer = officer.id
            self.save()

            # Create a log entry for the conservation status
            self.log_user_action(
                ConservationStatusUserAction.ACTION_ASSIGN_TO_ASSESSOR.format(
                    self.conservation_status_number,
                    f"{officer.get_full_name()}({officer.email})",
                ),
                request,
            )

            # TODO: Create a log entry for the user

    @transaction.atomic
    def unassign(self, request):
        if not self.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        if (
            self.processing_status
            == ConservationStatus.PROCESSING_STATUS_READY_FOR_AGENDA
        ):
            if self.assigned_approver:
                self.assigned_approver = None
                self.save()

                # Create a log entry for the proposal
                self.log_user_action(
                    ConservationStatusUserAction.ACTION_UNASSIGN_APPROVER.format(
                        self.conservation_status_number
                    ),
                    request,
                )

                # TODO: Create a log entry for the user
        else:
            if self.assigned_officer:
                self.assigned_officer = None
                self.save()

                # Create a log entry for the proposal
                self.log_user_action(
                    ConservationStatusUserAction.ACTION_UNASSIGN_ASSESSOR.format(
                        self.conservation_status_number
                    ),
                    request,
                )

                # TODO: Create a log entry for the user

    @transaction.atomic
    def send_referral(self, request, referral_email, referral_text):
        referral_email = referral_email.lower()
        if self.processing_status not in [
            ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR,
            ConservationStatus.PROCESSING_STATUS_WITH_REFERRAL,
        ]:
            raise exceptions.ConservationStatusReferralCannotBeSent()

        self.processing_status = ConservationStatus.PROCESSING_STATUS_WITH_REFERRAL
        self.save()
        referral = None
        # Check if the user is in ledger
        try:
            user = EmailUser.objects.get(email__icontains=referral_email)
        except EmailUser.DoesNotExist:
            # Validate if it is a deparment user
            department_user = get_department_user(referral_email)
            if not department_user:
                raise ValidationError(
                    "The user you want to send the referral to is not a member of the department"
                )
            # TODO Check if the user is in ledger or create (must be done via api in segregated system)

        try:
            ConservationStatusReferral.objects.get(
                referral=user.id, conservation_status=self
            )
            raise ValidationError("A referral has already been sent to this user")
        except ConservationStatusReferral.DoesNotExist:
            referral = ConservationStatusReferral.objects.create(
                conservation_status=self,
                referral=user.id,
                sent_by=request.user.id,
                text=referral_text,
                assigned_officer=request.user.id,  # TODO should'nt use assigned officer as per das
            )

        # Create a log entry for the proposal
        self.log_user_action(
            ConservationStatusUserAction.ACTION_SEND_REFERRAL_TO.format(
                referral.id,
                self.conservation_status_number,
                f"{user.get_full_name()}({user.email})",
            ),
            request,
        )

        # TODO Create a log entry for the user

        # send email
        send_conservation_status_referral_email_notification(referral, request)

    @property
    def amendment_requests(self):
        qs = ConservationStatusAmendmentRequest.objects.filter(conservation_status=self)
        return qs

    def move_to_status(self, request, status, approver_comment):
        if not self.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        if status not in [
            ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR,
            ConservationStatus.PROCESSING_STATUS_WITH_APPROVER,
        ]:
            raise ValidationError("The provided status cannot be found.")

        if (
            self.processing_status == ConservationStatus.PROCESSING_STATUS_WITH_REFERRAL
            or self.can_user_edit
        ):
            raise ValidationError("You cannot change the current status at this time")

        if self.processing_status == status:
            return

        if self.processing_status == ConservationStatus.PROCESSING_STATUS_WITH_APPROVER:
            self.approver_comment = ""
            if approver_comment:
                self.approver_comment = approver_comment
                self.save()
                send_proposal_approver_sendback_email_notification(request, self)
        self.processing_status = status
        self.save()

        # Create a log entry for the conservation status
        if self.processing_status == self.PROCESSING_STATUS_WITH_ASSESSOR:
            self.log_user_action(
                ConservationStatusUserAction.ACTION_BACK_TO_PROCESSING.format(
                    self.conservation_status_number
                ),
                request,
            )

        # TODO: Create a log entry for the user

    def proposed_decline(self, request, details):
        with transaction.atomic():
            if not self.can_assess(request.user):
                raise exceptions.ProposalNotAuthorized()
            if (
                self.processing_status
                != ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR
            ):
                raise ValidationError(
                    "You cannot propose to decline if it is not with assessor"
                )

            reason = details.get("reason")
            ConservationStatusDeclinedDetails.objects.update_or_create(
                conservation_status=self,
                defaults={
                    "officer": request.user.id,
                    "reason": reason,
                    "cc_email": details.get("cc_email", None),
                },
            )
            self.proposed_decline_status = True
            approver_comment = ""

            self.move_to_status(
                request,
                ConservationStatus.PROCESSING_STATUS_WITH_APPROVER,
                approver_comment,
            )

            # Log proposal action
            self.log_user_action(
                ConservationStatusUserAction.ACTION_PROPOSED_DECLINE.format(
                    self.conservation_status_number
                ),
                request,
            )

            # TODO create a log entry for the user

            send_approver_decline_email_notification(reason, request, self)

    @transaction.atomic
    def final_decline(self, request, details):
        if not self.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        if self.processing_status not in ("with_assessor", "ready_for_agenda"):
            raise ValidationError(
                "You cannot decline the proposal if it is not with an assessor"
            )

        conservation_status_decline, created = (
            ConservationStatusDeclinedDetails.objects.update_or_create(
                conservation_status=self,
                defaults={
                    "officer": request.user.id,
                    "reason": details.get("reason"),
                    "cc_email": details.get("cc_email", None),
                },
            )
        )
        self.proposed_decline_status = True

        self.processing_status = ConservationStatus.PROCESSING_STATUS_DECLINED
        self.customer_status = ConservationStatus.CUSTOMER_STATUS_DECLINED

        self.save()

        # Log proposal action
        self.log_user_action(
            ConservationStatusUserAction.ACTION_DECLINE.format(
                self.conservation_status_number
            ),
            request,
        )

        # TODO create a log entry for the user

        send_conservation_status_decline_email_notification(
            self, request, conservation_status_decline
        )

    @transaction.atomic
    def proposed_approval(self, request, details):
        if not self.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        if self.processing_status != ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR:
            raise ValidationError(
                "You cannot propose for approval if it is not with assessor"
            )

        ConservationStatusIssuanceApprovalDetails.objects.update_or_create(
            conservation_status=self,
            defaults={
                "officer": request.user.id,
                "effective_from_date": details.get("effective_from_date"),
                "effective_to_date": details.get("effective_to_date"),
                "details": details.get("details"),
                "cc_email": details.get("cc_email", None),
            },
        )
        self.proposed_decline_status = False
        approver_comment = ""

        self.move_to_status(
            request,
            ConservationStatus.PROCESSING_STATUS_WITH_APPROVER,
            approver_comment,
        )
        self.assigned_officer = None
        self.save()

        # Log proposal action
        self.log_user_action(
            ConservationStatusUserAction.ACTION_PROPOSED_APPROVAL.format(
                self.conservation_status_number
            ),
            request,
        )

        # TODO create a log entry for the user

        send_approver_approve_email_notification(request, self)

    @transaction.atomic
    def final_approval(self, request, details):
        self.proposed_decline_status = False

        if not self.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        if self.processing_status not in [
            ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR,
            ConservationStatus.PROCESSING_STATUS_READY_FOR_AGENDA,
        ]:
            raise ValidationError(
                "This conservation status can not be approved if it is not with an assessor or ready for agenda"
            )

        # For conservation statuses that require ministerial approval
        # check if the meeting is scheduled or completed
        if self.approval_level == ConservationStatus.APPROVAL_LEVEL_MINISTER:
            from boranga.components.meetings.models import Meeting

            added_to_meeting_status = [
                Meeting.PROCESSING_STATUS_SCHEDULED,
                Meeting.PROCESSING_STATUS_COMPLETED,
            ]
            if not self.agendaitem_set.filter(
                meeting__processing_status__in=added_to_meeting_status
            ).exists():
                raise ValidationError(
                    "This conservation status can not be approved as there are no meetings "
                    "for the minister approval that are scheduled or completed"
                )

        # Add the approval document first to to get the reference id in below model
        proposal_approval_document = request.data["proposal_approval_document"]
        d = None
        if proposal_approval_document != "null":
            try:
                document = self.documents.get(name=str(proposal_approval_document))
            except ConservationStatusDocument.DoesNotExist:
                document = self.documents.get_or_create(
                    input_name="conservation_status_approval_doc",
                    name=str(proposal_approval_document),
                )[0]

            document.name = str(proposal_approval_document)
            document._file = proposal_approval_document
            document.save()

            d = ConservationStatusDocument.objects.get(id=document.id)

        effective_from = details.get("effective_from_date")
        effective_to = details.get("effective_to_date")
        ConservationStatusIssuanceApprovalDetails.objects.update_or_create(
            conservation_status=self,
            defaults={
                "officer": request.user.id,
                "effective_from_date": effective_from,
                "effective_to_date": effective_to,
                "details": details.get("details"),
                "cc_email": details.get("cc_email", None),
                "conservation_status_approval_document": d,
            },
        )

        self.processing_status = ConservationStatus.PROCESSING_STATUS_APPROVED
        self.customer_status = ConservationStatus.CUSTOMER_STATUS_APPROVED

        if effective_from:
            self.effective_from = effective_from

        if effective_to:
            self.effective_to = effective_to

        # Log proposal action
        self.log_user_action(
            ConservationStatusUserAction.ACTION_APPROVE_PROPOSAL_.format(
                self.conservation_status_number
            ),
            request,
        )

        # TODO create a log entry for the user

        # Delist / Close the previous approved version
        previous_approved_version = ConservationStatus.objects.filter(
            processing_status=ConservationStatus.PROCESSING_STATUS_APPROVED
        )

        if self.species:
            previous_approved_version = previous_approved_version.filter(
                species=self.species
            ).first()
        elif self.community:
            previous_approved_version = previous_approved_version.filter(
                community=self.community
            ).first()

        if previous_approved_version:
            # Check if the previous conservation status has a priority list
            if previous_approved_version.wa_priority_list and not self.wa_priority_list:
                self.wa_priority_list = previous_approved_version.wa_priority_list

                # Check if the previous conservation status has a priority category
                if (
                    previous_approved_version.wa_priority_category
                    and not self.wa_priority_category
                ):
                    self.wa_priority_category = (
                        previous_approved_version.wa_priority_category
                    )

            previous_approved_version.customer_status = (
                ConservationStatus.PROCESSING_STATUS_CLOSED
            )
            previous_approved_version.processing_status = (
                ConservationStatus.PROCESSING_STATUS_CLOSED
            )
            previous_approved_version.change_code = (
                ConservationChangeCode.get_delisted_change_code()
            )
            if self.effective_from:
                previous_approved_version.effective_to = (
                    self.effective_from - timedelta(days=1)
                )
            previous_approved_version.save()

            # Create a log entry for the conservation status
            self.log_user_action(
                ConservationStatusUserAction.ACTION_CLOSE_CONSERVATIONSTATUS.format(
                    previous_approved_version.conservation_status_number
                ),
                request,
            )

        # send Proposal approval email with attachment
        send_conservation_status_approval_email_notification(self, request)

        self.save()
        self.documents.all().update(can_delete=False)

    @transaction.atomic
    def proposed_ready_for_agenda(self, request):
        if not self.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        if self.processing_status != ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR:
            raise ValidationError(
                "You cannot propose for ready for agenda if it is not with assessor"
            )

        (self.processing_status,) = (
            ConservationStatus.PROCESSING_STATUS_READY_FOR_AGENDA
        )
        self.customer_status = ConservationStatus.PROCESSING_STATUS_READY_FOR_AGENDA
        self.save()

        # Log proposal action
        self.log_user_action(
            ConservationStatusUserAction.ACTION_PROPOSED_READY_FOR_AGENDA.format(
                self.conservation_status_number
            ),
            request,
        )

        # TODO create a log entry for the user

        send_assessor_ready_for_agenda_email_notification(request, self)

    def get_related_items(self, filter_type, **kwargs):
        return_list = []
        if filter_type == "all":
            related_field_names = ["species", "community", "agendaitem"]
        else:
            related_field_names = [
                filter_type,
            ]
        all_fields = self._meta.get_fields()
        for a_field in all_fields:
            if a_field.name in related_field_names:
                field_objects = []
                if a_field.is_relation:
                    if a_field.many_to_many:
                        pass
                    elif a_field.many_to_one:  # foreign key
                        field_objects = [
                            getattr(self, a_field.name),
                        ]
                    elif a_field.one_to_many:  # reverse foreign key
                        field_objects = a_field.related_model.objects.filter(
                            **{a_field.remote_field.name: self}
                        )
                    elif a_field.one_to_one:
                        if hasattr(self, a_field.name):
                            field_objects = [
                                getattr(self, a_field.name),
                            ]
                for field_object in field_objects:
                    if field_object:
                        related_item = field_object.as_related_item
                        return_list.append(related_item)

        return return_list

    @property
    def as_related_item(self):
        related_item = RelatedItem(
            identifier=self.related_item_identifier,
            model_name=self._meta.verbose_name,
            descriptor=self.related_item_descriptor,
            status=self.related_item_status,
            action_url=f'<a href=/internal/conservation_status/{self.id} target="_blank">View</a>',
        )
        return related_item

    @property
    def related_item_identifier(self):
        return self.conservation_status_number

    @property
    def related_item_descriptor(self):
        if self.conservation_list:
            return self.conservation_list.code

    @property
    def related_item_status(self):
        return self.get_processing_status_display


class ConservationStatusLogEntry(CommunicationsLogEntry):
    conservation_status = models.ForeignKey(
        ConservationStatus, related_name="comms_logs", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.reference} - {self.subject}"

    class Meta:
        app_label = "boranga"

    def save(self, **kwargs):
        # save the application reference if the reference not provided
        if not self.reference:
            self.reference = self.conservation_status.reference
        super().save(**kwargs)


class ConservationStatusLogDocument(Document):
    log_entry = models.ForeignKey(
        "ConservationStatusLogEntry", related_name="documents", on_delete=models.CASCADE
    )
    _file = models.FileField(
        upload_to=update_conservation_status_comms_log_filename,
        max_length=512,
        storage=private_storage,
    )

    class Meta:
        app_label = "boranga"


class ConservationStatusUserAction(UserAction):
    # ConservationStatus Proposal
    ACTION_EDIT_CONSERVATION_STATUS = "Edit Conservation Status {}"
    ACTION_LODGE_PROPOSAL = "Lodge proposal for conservation status {}"
    ACTION_SAVE_APPLICATION = "Save proposal {}"
    ACTION_EDIT_APPLICATION = "Edit proposal {}"
    ACTION_ASSIGN_TO_ASSESSOR = (
        "Assign conservation status proposal {} to {} as the assessor"
    )
    ACTION_UNASSIGN_ASSESSOR = "Unassign assessor from conservation status proposal {}"
    ACTION_ASSIGN_TO_APPROVER = (
        "Assign conservation status proposal {} to {} as the approver"
    )
    ACTION_UNASSIGN_APPROVER = "Unassign approver from conservation status proposal {}"
    ACTION_DECLINE = "Decline conservation status application {}"
    ACTION_APPROVE_PROPOSAL_ = "Approve conservation status  proposal {}"
    ACTION_CLOSE_CONSERVATIONSTATUS = "De list conservation status {}"
    ACTION_DISCARD_PROPOSAL = "Discard conservation status proposal {}"
    ACTION_APPROVAL_LEVEL_DOCUMENT = "Assign Approval level document {}"

    # Amendment
    ACTION_ID_REQUEST_AMENDMENTS = "Request amendments"

    # Assessors
    ACTION_SAVE_ASSESSMENT_ = "Save assessment {}"
    ACTION_CONCLUDE_ASSESSMENT_ = "Conclude assessment {}"
    ACTION_PROPOSED_READY_FOR_AGENDA = (
        "Conservation status proposal {} has been proposed for ready for agenda"
    )
    ACTION_PROPOSED_APPROVAL = (
        "Conservation status proposal {} has been proposed for approval"
    )
    ACTION_PROPOSED_DECLINE = (
        "Conservation status proposal {} has been proposed for decline"
    )

    # Referrals
    ACTION_SEND_REFERRAL_TO = (
        "Send referral {} for conservation status proposal {} to {}"
    )
    ACTION_RESEND_REFERRAL_TO = (
        "Resend referral {} for conservation status proposal {} to {}"
    )
    ACTION_REMIND_REFERRAL = (
        "Send reminder for referral {} for conservation status proposal {} to {}"
    )
    ACTION_BACK_TO_PROCESSING = "Back to processing for conservation status proposal {}"
    RECALL_REFERRAL = (
        "Referral {} for conservation status proposal {} has been recalled"
    )
    COMMENT_REFERRAL = (
        "Referral {} for conservation status proposal {} has been commented by {}"
    )
    CONCLUDE_REFERRAL = (
        "Referral {} for conservation status proposal {} has been concluded by {}"
    )

    class Meta:
        app_label = "boranga"
        ordering = ("-when",)

    @classmethod
    def log_action(cls, conservation_status, action, user):
        return cls.objects.create(
            conservation_status=conservation_status, who=user, what=str(action)
        )

    conservation_status = models.ForeignKey(
        ConservationStatus, related_name="action_logs", on_delete=models.CASCADE
    )


class ConservationStatusDocument(Document):
    document_number = models.CharField(max_length=9, blank=True, default="")
    conservation_status = models.ForeignKey(
        "ConservationStatus", related_name="documents", on_delete=models.CASCADE
    )
    _file = models.FileField(
        upload_to=update_conservation_status_doc_filename,
        max_length=512,
        storage=private_storage,
    )
    input_name = models.CharField(max_length=255, null=True, blank=True)
    can_delete = models.BooleanField(
        default=True
    )  # after initial submit prevent document from being deleted
    can_hide = models.BooleanField(
        default=False
    )  # after initial submit, document cannot be deleted but can be hidden
    hidden = models.BooleanField(
        default=False
    )  # after initial submit prevent document from being deleted
    # Priya alternatively used below visible field in boranga
    visible = models.BooleanField(
        default=True
    )  # to prevent deletion on file system, hidden and still be available in history
    document_category = models.ForeignKey(
        DocumentCategory, null=True, blank=True, on_delete=models.SET_NULL
    )
    document_sub_category = models.ForeignKey(
        DocumentSubCategory, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        app_label = "boranga"
        verbose_name = "Conservation Status Document"

    def save(self, *args, **kwargs):
        # Prefix "D" char to document_number.
        if self.document_number == "":
            force_insert = kwargs.pop("force_insert", False)
            super().save(no_revision=True, force_insert=force_insert)
            new_document_id = f"D{str(self.pk)}"
            self.document_number = new_document_id
            self.save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    @transaction.atomic
    def add_documents(self, request, *args, **kwargs):
        # save the files
        data = json.loads(request.data.get("data"))

        for idx in range(data["num_files"]):
            _file = request.data.get("file-" + str(idx))
            self._file = _file
            self.name = _file.name
            self.input_name = data["input_name"]
            self.can_delete = True
            self.save(no_revision=True)

        # end save documents
        self.save(*args, **kwargs)


class ConservationStatusDeclinedDetails(models.Model):
    conservation_status = models.OneToOneField(
        ConservationStatus, on_delete=models.CASCADE
    )
    officer = models.IntegerField()  # EmailUserRO
    reason = models.TextField(blank=True)
    cc_email = models.TextField(null=True)

    class Meta:
        app_label = "boranga"


class ConservationStatusIssuanceApprovalDetails(models.Model):
    conservation_status = models.OneToOneField(
        ConservationStatus, on_delete=models.CASCADE
    )
    officer = models.IntegerField()  # EmailUserRO
    effective_from_date = models.DateField(null=True, blank=True)
    effective_to_date = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True)
    cc_email = models.TextField(null=True)
    conservation_status_approval_document = models.ForeignKey(
        ConservationStatusDocument,
        blank=True,
        null=True,
        related_name="conservation_status_approval_document",
        on_delete=models.SET_NULL,
    )

    class Meta:
        app_label = "boranga"


class ConservationStatusReferralDocument(Document):
    referral = models.ForeignKey(
        "ConservationStatusReferral",
        related_name="referral_documents",
        on_delete=models.CASCADE,
    )
    _file = models.FileField(
        upload_to=update_referral_doc_filename, max_length=512, storage=private_storage
    )
    input_name = models.CharField(max_length=255, null=True, blank=True)
    can_delete = models.BooleanField(
        default=True
    )  # after initial submit prevent document from being deleted

    def delete(self):
        if self.can_delete:
            return self.can_delete
        logger.info(
            "Cannot delete existing document object after Application has been submitted "
            "(including document submitted before Application pushback to status Draft): {}".format(
                self.name
            )
        )

    class Meta:
        app_label = "boranga"


class ConservationStatusReferral(models.Model):
    SENT_CHOICES = ((1, "Sent From Assessor"), (2, "Sent From Referral"))
    PROCESSING_STATUS_WITH_REFERRAL = "with_referral"
    PROCESSING_STATUS_RECALLED = "recalled"
    PROCESSING_STATUS_COMPLETED = "completed"
    PROCESSING_STATUS_CHOICES = (
        (PROCESSING_STATUS_WITH_REFERRAL, "Awaiting"),
        (PROCESSING_STATUS_RECALLED, "Recalled"),
        (PROCESSING_STATUS_COMPLETED, "Completed"),
    )
    lodged_on = models.DateTimeField(auto_now_add=True)
    conservation_status = models.ForeignKey(
        ConservationStatus, related_name="referrals", on_delete=models.CASCADE
    )
    sent_by = models.IntegerField()  # EmailUserRO
    referral = models.IntegerField()  # EmailUserRO
    linked = models.BooleanField(default=False)
    sent_from = models.SmallIntegerField(
        choices=SENT_CHOICES, default=SENT_CHOICES[0][0]
    )
    processing_status = models.CharField(
        "Processing Status",
        max_length=30,
        choices=PROCESSING_STATUS_CHOICES,
        default=PROCESSING_STATUS_CHOICES[0][0],
    )
    text = models.TextField(blank=True)  # Assessor text when send_referral
    referral_text = models.TextField(
        blank=True
    )  # used in other projects for complete referral comment but not used in boranga
    referral_comment = models.TextField(blank=True, null=True)  # Referral Comment
    document = models.ForeignKey(
        ConservationStatusReferralDocument,
        blank=True,
        null=True,
        related_name="referral_document",
        on_delete=models.SET_NULL,
    )
    assigned_officer = models.IntegerField(null=True)  # EmailUserRO

    class Meta:
        app_label = "boranga"
        ordering = ("-lodged_on",)

    def __str__(self):
        return f"Application {self.conservation_status.id} - Referral {self.id}"

    # Methods
    @property
    def latest_referrals(self):
        return ConservationStatusReferral.objects.filter(
            sent_by=self.referral, conservation_status=self.conservation_status
        )[:2]

    @property
    def can_be_completed(self):
        # Referral cannot be completed until second level referral sent by referral has been completed/recalled
        return not ConservationStatusReferral.objects.filter(
            sent_by=self.referral,
            conservation_status=self.conservation_status,
            processing_status=ConservationStatusReferral.PROCESSING_STATUS_WITH_REFERRAL,
        ).exists()

    @property
    def referral_as_email_user(self):
        return retrieve_email_user(self.referral)

    @transaction.atomic
    def remind(self, request):
        if not self.conservation_status.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        # Create a log entry for the proposal
        self.conservation_status.log_user_action(
            ConservationStatusUserAction.ACTION_REMIND_REFERRAL.format(
                self.id,
                self.conservation_status.conservation_status_number,
                f"{self.referral_as_email_user.get_full_name()}",
            ),
            request,
        )

        # TODO Create a log entry for the user who performed the action

        # send email
        send_conservation_status_referral_email_notification(
            self,
            request,
            reminder=True,
        )

    @transaction.atomic
    def recall(self, request):
        if not self.conservation_status.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        self.processing_status = ConservationStatusReferral.PROCESSING_STATUS_RECALLED
        self.save()

        outstanding = self.conservation_status.referrals.filter(
            processing_status=ConservationStatusReferral.PROCESSING_STATUS_WITH_REFERRAL
        )
        if len(outstanding) == 0:
            self.conservation_status.processing_status = (
                ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR
            )
            self.conservation_status.save()

        send_conservation_status_referral_recall_email_notification(self, request)

        # Create a log entry for the conservation status
        self.conservation_status.log_user_action(
            ConservationStatusUserAction.RECALL_REFERRAL.format(
                self.id,
                self.conservation_status.conservation_status_number,
            ),
            request,
        )

        # TODO Create a log entry for the user who performed the action

    @transaction.atomic
    def resend(self, request):
        if not self.conservation_status.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        self.processing_status = (
            ConservationStatusReferral.PROCESSING_STATUS_WITH_REFERRAL
        )
        self.conservation_status.processing_status = (
            ConservationStatusReferral.PROCESSING_STATUS_WITH_REFERRAL
        )
        self.conservation_status.save()

        self.sent_from = 1
        self.save()

        # Create a log entry for the conservation status
        self.conservation_status.log_user_action(
            ConservationStatusUserAction.ACTION_RESEND_REFERRAL_TO.format(
                self.id,
                self.conservation_status.conservation_status_number,
                f"{self.referral_as_email_user.get_full_name()}({self.referral_as_email_user.email})",
            ),
            request,
        )

        # TODO Create a log entry for the user who performed the action

        # send email
        send_conservation_status_referral_email_notification(self, request)

    @transaction.atomic
    def send_referral(self, request, referral_email, referral_text):
        referral_email = referral_email.lower()
        if not (
            self.conservation_status.processing_status
            == ConservationStatus.PROCESSING_STATUS_WITH_REFERRAL
        ):
            raise exceptions.ConservationStatusReferralCannotBeSent()

        if request.user.id != self.referral:
            raise exceptions.ReferralNotAuthorized()
        if self.sent_from != 1:
            raise exceptions.ReferralCanNotSend()
        self.conservation_status.processing_status = (
            ConservationStatus.PROCESSING_STATUS_WITH_REFERRAL
        )
        self.conservation_status.save()
        referral = None

        # Check if the user is in ledger
        try:
            user = EmailUser.objects.get(email__icontains=referral_email)
        except EmailUser.DoesNotExist:
            # Validate if it is a deparment user
            department_user = get_department_user(referral_email)
            if not department_user:
                raise ValidationError(
                    "The user you want to send the referral to is not a member of the department"
                )

            # TODO Check if the user is in ledger or create (must be done via api in segregated system)

        qs = ConservationStatusReferral.objects.filter(
            sent_by=user.id, conservation_status=self.conservation_status
        )
        if qs:
            raise ValidationError("You cannot send referral to this user")
        try:
            ConservationStatusReferral.objects.get(
                referral=user.id,
                conservation_status=self.conservation_status,
            )
            raise ValidationError("A referral has already been sent to this user")
        except ConservationStatusReferral.DoesNotExist:
            # Create Referral
            referral = ConservationStatusReferral.objects.create(
                conservation_status=self.conservation_status,
                referral=user.id,
                sent_by=request.user.id,
                sent_from=2,
                text=referral_text,
            )

        # Create a log entry for the conservation status
        self.conservation_status.log_user_action(
            ConservationStatusUserAction.ACTION_SEND_REFERRAL_TO.format(
                referral.id,
                self.conservation_status.conservation_status_number,
                f"{user.get_full_name()}({user.email})",
            ),
            request,
        )

        # TODO Create a log entry for the user who performed the action

        # send email
        send_conservation_status_referral_email_notification(referral, request)

    @transaction.atomic
    def complete(self, request):
        if request.user.id != self.referral:
            raise exceptions.ReferralNotAuthorized()

        self.processing_status = ConservationStatusReferral.PROCESSING_STATUS_COMPLETED
        self.save()

        outstanding = self.conservation_status.referrals.filter(
            processing_status=ConservationStatusReferral.PROCESSING_STATUS_WITH_REFERRAL
        )
        if len(outstanding) == 0:
            self.conservation_status.processing_status = (
                ConservationStatus.PROCESSING_STATUS_WITH_ASSESSOR
            )
            self.conservation_status.save()

        # Create a log entry for the conservation status
        self.conservation_status.log_user_action(
            ConservationStatusUserAction.CONCLUDE_REFERRAL.format(
                self.id,
                self.conservation_status.conservation_status_number,
                f"{self.referral_as_email_user.get_full_name()}({self.referral_as_email_user.email})",
            ),
            request,
        )

        # TODO Create a log entry for the user who performed the action

        send_conservation_status_referral_complete_email_notification(self, request)

    def can_assess_referral(self, user):
        return (
            self.processing_status
            == ConservationStatusReferral.PROCESSING_STATUS_WITH_REFERRAL
        )

    @property
    def can_be_processed(self):
        return (
            self.processing_status
            == ConservationStatusReferral.PROCESSING_STATUS_WITH_REFERRAL
        )


class ConservationStatusProposalRequest(models.Model):
    conservation_status = models.ForeignKey(
        ConservationStatus, on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=200, blank=True)
    text = models.TextField(blank=True)
    officer = models.IntegerField(null=True)  # EmailUserRO

    class Meta:
        app_label = "boranga"


class ProposalAmendmentReason(models.Model):
    reason = models.CharField("Reason", max_length=125)

    class Meta:
        app_label = "boranga"
        verbose_name = "Proposal Amendment Reason"  # display name in Admin
        verbose_name_plural = "Proposal Amendment Reasons"

    def __str__(self):
        return self.reason


class ConservationStatusAmendmentRequest(ConservationStatusProposalRequest):
    STATUS_CHOICE_REQUESTED = "requested"
    STATUS_CHOICE_AMENDED = "amended"

    STATUS_CHOICES = (
        (STATUS_CHOICE_REQUESTED, "Requested"),
        (STATUS_CHOICE_AMENDED, "Amended"),
    )

    status = models.CharField(
        "Status", max_length=30, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    reason = models.ForeignKey(
        ProposalAmendmentReason, blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        app_label = "boranga"

    @transaction.atomic
    def generate_amendment(self, request):
        if not self.conservation_status.can_assess(request.user):
            raise exceptions.ProposalNotAuthorized()

        if self.status == ConservationStatusAmendmentRequest.STATUS_CHOICE_REQUESTED:
            conservation_status = self.conservation_status
            if (
                conservation_status.processing_status
                != ConservationStatus.PROCESSING_STATUS_DRAFT
            ):
                conservation_status.processing_status = (
                    ConservationStatus.PROCESSING_STATUS_DRAFT
                )
                conservation_status.customer_status = (
                    ConservationStatus.PROCESSING_STATUS_DRAFT
                )
                conservation_status.save()
                # TODO at the moment conservation_status is not having it's document model
                # conservation_status.documents.all().update(can_hide=True)

            # Create a log entry for the conservationstatus
            conservation_status.log_user_action(
                ConservationStatusUserAction.ACTION_ID_REQUEST_AMENDMENTS,
                request,
            )

            # Create a log entry for the user

            # send email
            send_conservation_status_amendment_email_notification(
                self, request, conservation_status
            )

        self.save()

    def add_documents(self, request):
        with transaction.atomic():
            # save the files
            data = json.loads(request.data.get("data"))
            if not data.get("update"):
                documents_qs = self.cs_amendment_request_documents.filter(
                    input_name="amendment_request_doc", visible=True
                )
                documents_qs.delete()
            for idx in range(data["num_files"]):
                _file = request.data.get("file-" + str(idx))
                document = self.cs_amendment_request_documents.create(
                    _file=_file, name=_file.name
                )
                document.input_name = data["input_name"]
                document.can_delete = True
                document.save()
            # end save documents
            self.save()

        return


class ConservationStatusAmendmentRequestDocument(Document):
    conservation_status_amendment_request = models.ForeignKey(
        "ConservationStatusAmendmentRequest",
        related_name="cs_amendment_request_documents",
        on_delete=models.CASCADE,
    )
    _file = models.FileField(
        upload_to=update_conservation_status_amendment_request_doc_filename,
        max_length=500,
        storage=private_storage,
    )
    input_name = models.CharField(max_length=255, null=True, blank=True)
    can_delete = models.BooleanField(
        default=True
    )  # after initial submit prevent document from being deleted
    visible = models.BooleanField(
        default=True
    )  # to prevent deletion on file system, hidden and still be available in history

    def delete(self):
        if self.can_delete:
            return super().delete()


# Species Document History
reversion.register(ConservationStatusDocument)

# Conservation Status History
reversion.register(ConservationStatus, follow=["species", "community"])
