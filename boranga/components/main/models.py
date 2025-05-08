import logging
import os
from abc import ABCMeta, abstractmethod

from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.db import models
from ordered_model.models import OrderedModel, OrderedModelManager
from reversion.models import Version

from boranga.helpers import check_file

private_storage = FileSystemStorage(
    location=settings.BASE_DIR + "/private-media/", base_url="/private-media/"
)
model_type = models.base.ModelBase

logger = logging.getLogger(__name__)


class AbstractModelMeta(ABCMeta, model_type):
    pass


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


class FileExtensionWhitelist(models.Model):

    name = models.CharField(
        max_length=16,
        help_text="The file extension without the dot, e.g. jpg, pdf, docx, etc",
    )
    model = models.CharField(max_length=255, default="all")

    compressed = models.BooleanField(
        help_text="Check this box for extensions such as zip, 7z, and tar",
    )

    class Meta:
        app_label = "boranga"
        unique_together = ("name", "model")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field("model").choices = (
            (
                "all",
                "all",
            ),
        ) + tuple(
            map(
                lambda m: (m, m),
                filter(
                    lambda m: Document
                    in apps.get_app_config("boranga").models[m].__bases__,
                    apps.get_app_config("boranga").models,
                ),
            )
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(settings.CACHE_KEY_FILE_EXTENSION_WHITELIST)


class DocumentQuerySet(models.QuerySet):
    def delete(self) -> None:
        self.update(active=False)


class ActiveManager(models.Manager):
    def active(self) -> models.QuerySet:
        return self.model.objects.filter(active=True)

    def get_queryset(self) -> models.QuerySet:
        return DocumentQuerySet(self.model, using=self._db)


class Document(RevisionedMixin, metaclass=AbstractModelMeta):
    name = models.CharField(
        max_length=255, blank=True, verbose_name="name", help_text=""
    )
    description = models.TextField(blank=True, verbose_name="description", help_text="")
    uploaded_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "boranga"
        abstract = True

    def __str__(self):
        return self.name or self.filename

    def delete(self, *args, **kwargs):
        # Users are allowed to remove documents from our file system
        # if they are related to a proposal that has not yet been submitted
        parent_instance = self.get_parent_instance()
        if not parent_instance:
            raise AttributeError(
                "Document does not have an associated parent instance. Cannot delete."
            )

        # If the parent instance doesn't have a lodgement_date field
        # or it has a lodgement_date field and it is not None
        # then we do not allow the file to be removed from the file system
        if self.parent_submitted:
            self.deactivate()
            return

        # If the parent instance has a lodgement_date field and it is None
        # then we allow the file to be removed from the file system as the
        # parent instance has not yet been submitted
        if (
            hasattr(parent_instance, "lodgement_date")
            and parent_instance.lodgement_date is None
            and self._file
        ):
            if os.path.exists(self._file.path):
                os.remove(self._file.path)
            else:
                logger.warning(
                    "File not found on file system: %s (%s). Setting _file to None",
                    self._file.path,
                    self._file.name,
                )
            self._file = None

        # Document records are never actually deleted, just marked as inactive
        self.deactivate()

    def deactivate(self):
        self.active = False
        self.save()

    @abstractmethod
    def get_parent_instance(self) -> models.Model:
        raise NotImplementedError(
            "Subclasses of Document must implement a get_parent_instance method"
        )

    @property
    def parent_submitted(self):
        parent_instance = self.get_parent_instance()
        if (
            hasattr(parent_instance, "lodgement_date")
            and parent_instance.lodgement_date
        ):
            return True
        return False

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

    def check_file(self, file):
        return check_file(file, self._meta.model_name)


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
    user = models.IntegerField(unique=True)  # EmailUserRO
    area_of_interest = models.ForeignKey(
        "GroupType", on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        app_label = "boranga"
        verbose_name_plural = "User System Settings"


class ArchivableManager(models.Manager):
    def active(self):
        return super().get_queryset().filter(archived=False)

    def archived(self):
        return super().get_queryset().filter(archived=True)


class ArchivableModel(models.Model):
    objects = ArchivableManager()

    archived = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def archive(self):
        if not self.archived:
            self.archived = True
            self.save()

    def unarchive(self):
        if self.archived:
            self.archived = False
            self.save()


class OrderedArchivableManager(OrderedModelManager, ArchivableManager):
    pass


class HelpTextEntry(ArchivableModel):
    section_id = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    icon_with_popover = models.BooleanField(
        default=False,
        help_text="Instead of showing the text in situ, show a popover with the text",
    )
    authenticated_users_only = models.BooleanField(default=True)
    internal_users_only = models.BooleanField(default=True)

    class Meta:
        app_label = "boranga"
        verbose_name_plural = "Help Text Entries"

    def __str__(self):
        return self.section_id


class AbstractOrderedListManager(OrderedModelManager):
    def active(self):
        return super().get_queryset().filter(archived=False)

    def archived(self):
        return super().get_queryset().filter(archived=True)


class AbstractOrderedList(OrderedModel, ArchivableModel):
    objects = AbstractOrderedListManager()

    item = models.CharField(max_length=100)

    class Meta(OrderedModel.Meta):
        abstract = True
        app_label = "boranga"

    def __str__(self):
        return str(self.item)

    def get_lists_dict(
        cls: models.base.ModelBase,
        active_only: bool = False,
    ) -> list:
        lists = cls.objects.all()

        if active_only:
            lists = cls.objects.active()

        lists = lists.values("id", "item").order_by("order")

        return list(lists)
