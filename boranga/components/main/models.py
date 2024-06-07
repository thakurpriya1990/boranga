import logging
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from reversion.models import Version

private_storage = FileSystemStorage(
    location=settings.BASE_DIR + "/private-media/", base_url="/private-media/"
)

logger = logging.getLogger(__name__)


class RevisionedMixin(models.Model):
    """
    A model tracked by reversion through the save method.
    """

    def save(self, **kwargs):
        from reversion import revisions

        if kwargs.pop("no_revision", False):
            if "version_user" in kwargs:
                kwargs.pop("version_user", None)
            if "version_comment" in kwargs:
                kwargs.pop("version_comment", "")
            super().save(**kwargs)
        # kwargs can be set as attributes via serializers sometimes
        elif hasattr(self, "no_revision") and self.no_revision:
            if "version_user" in kwargs:
                kwargs.pop("version_user", None)
            if "version_comment" in kwargs:
                kwargs.pop("version_comment", "")
            super().save(**kwargs)
            # set no_revision to False - if an instance is saved twice for some reason
            # this should NOT be carried over (unless set to True again)
            self.no_revision = False
        else:
            with revisions.create_revision():
                if "version_user" in kwargs:
                    revisions.set_user(kwargs.pop("version_user", None))
                elif hasattr(self, "version_user") and self.version_user is not None:
                    revisions.set_user(self.version_user)
                    self.version_user = None
                if "version_comment" in kwargs:
                    revisions.set_comment(kwargs.pop("version_comment", ""))
                super().save(**kwargs)

    @property
    def revision_created_date(self):
        return Version.objects.get_for_object(self).last().revision.date_created

    @property
    def revision_modified_date(self):
        return Version.objects.get_for_object(self).first().revision.date_created

    class Meta:
        abstract = True


class UserAction(models.Model):
    who = models.IntegerField()  # EmailUserRO
    when = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    what = models.TextField(blank=False)

    def __str__(self):
        return "{what} ({who} at {when})".format(
            what=self.what, who=self.who, when=self.when
        )

    class Meta:
        abstract = True
        app_label = "boranga"


class CommunicationsLogEntry(models.Model):
    TYPE_CHOICES = [
        ("email", "Email"),
        ("phone", "Phone Call"),
        ("mail", "Mail"),
        ("person", "In Person"),
        ("onhold", "On Hold"),
        ("onhold_remove", "Remove On Hold"),
        ("with_qaofficer", "With QA Officer"),
        ("with_qaofficer_completed", "QA Officer Completed"),
        ("referral_complete", "Referral Completed"),
    ]
    DEFAULT_TYPE = TYPE_CHOICES[0][0]

    to = models.TextField(blank=True, verbose_name="To")
    fromm = models.CharField(max_length=200, blank=True, verbose_name="From")
    cc = models.TextField(blank=True, verbose_name="cc")

    type = models.CharField(max_length=35, choices=TYPE_CHOICES, default=DEFAULT_TYPE)
    reference = models.CharField(max_length=100, blank=True)
    subject = models.CharField(
        max_length=200, blank=True, verbose_name="Subject / Description"
    )
    text = models.TextField(blank=True)

    customer = models.IntegerField(null=True)  # EmailUserRO
    staff = models.IntegerField()  # EmailUserRO

    created = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        app_label = "boranga"


class Document(RevisionedMixin):
    name = models.CharField(
        max_length=255, blank=True, verbose_name="name", help_text=""
    )
    description = models.TextField(blank=True, verbose_name="description", help_text="")
    uploaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "boranga"
        abstract = True

    @property
    def path(self):
        # return self.file.path
        # return self._file.path
        # comment above line to fix the error "The '_file' attribute has no file
        # associated with it." when adding comms log entry.
        if self._file:
            return self._file.path
        else:
            return ""

    @property
    def filename(self):
        return os.path.basename(self.path)

    def __str__(self):
        return self.name or self.filename


class GlobalSettings(models.Model):
    keys = (
        ("credit_facility_link", "Credit Facility Link"),
        ("deed_poll", "Deed poll"),
        ("deed_poll_filming", "Deed poll Filming"),
        ("deed_poll_event", "Deed poll Event"),
        ("online_training_document", "Online Training Document"),
        ("park_finder_link", "Park Finder Link"),
        ("fees_and_charges", "Fees and charges link"),
        ("event_fees_and_charges", "Event Fees and charges link"),
        ("commercial_filming_handbook", "Commercial Filming Handbook link"),
        ("park_stay_link", "Park Stay Link"),
        ("event_traffic_code_of_practice", "Event traffic code of practice"),
        ("trail_section_map", "Trail section map"),
        ("dwer_application_form", "DWER Application Form"),
    )
    key = models.CharField(
        max_length=255,
        choices=keys,
        blank=False,
        null=False,
    )
    value = models.CharField(max_length=255)

    class Meta:
        app_label = "boranga"
        verbose_name_plural = "Global Settings"


# @python_2_unicode_compatible
class SystemMaintenance(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def duration(self):
        """Duration of system maintenance (in mins)"""
        return (
            int((self.end_date - self.start_date).total_seconds() / 60.0)
            if self.end_date and self.start_date
            else ""
        )
        # return (datetime.now(tz=tz) - self.start_date).total_seconds()/60.

    duration.short_description = "Duration (mins)"

    class Meta:
        app_label = "boranga"
        verbose_name_plural = "System maintenance"

    def __str__(self):
        return (
            f"System Maintenance: {self.name} ({self.description}) "
            f"- starting {self.start_date}, ending {self.end_date}"
        )


class UserSystemSettings(models.Model):
    # user = models.OneToOneField(EmailUser, related_name='system_settings', on_delete=models.CASCADE)
    user = models.IntegerField(unique=True)  # EmailUserRO
    event_training_completed = models.BooleanField(default=False)
    event_training_date = models.DateField(blank=True, null=True)

    class Meta:
        app_label = "boranga"
        verbose_name_plural = "User System Settings"
