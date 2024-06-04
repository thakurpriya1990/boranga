from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from ledger_api_client.managed_models import SystemGroup, SystemGroupPermission

from boranga.components.main.models import CommunicationsLogEntry, Document, UserAction

private_storage = FileSystemStorage(
    location=settings.BASE_DIR + "/private-media/", base_url="/private-media/"
)


class SubmitterCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "boranga"
        verbose_name_plural = "Submitter Categories"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def get_filter_list(cls):
        return list(cls.objects.all().values("id", "name"))


class SubmitterInformation(models.Model):
    email_user = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    contact_details = models.TextField(blank=True, null=True)
    organisation = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    submitter_category = models.ForeignKey(
        SubmitterCategory, on_delete=models.PROTECT, blank=True, null=True
    )

    class Meta:
        app_label = "boranga"


class ExternalContributorBlacklist(models.Model):
    email = models.EmailField(unique=True)
    reason = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "boranga"
        verbose_name_plural = "External Contributor Blacklist"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Remove the user from the external contributors group
        external_contributor_group = SystemGroup.objects.get(
            name=settings.GROUP_NAME_EXTERNAL_CONTRIBUTOR
        )
        try:
            user = EmailUser.objects.get(email=self.email)
        except EmailUser.DoesNotExist:
            return

        SystemGroupPermission.objects.filter(
            system_group=external_contributor_group, emailuser=user
        ).delete()
        # Have to save the group to flush the member cache
        external_contributor_group.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            user = EmailUser.objects.get(email=self.email)
        except EmailUser.DoesNotExist:
            return

        # If user is already in the external contributors group, don't add them again
        external_contributor_group = SystemGroup.objects.get(
            name=settings.GROUP_NAME_EXTERNAL_CONTRIBUTOR
        )
        if SystemGroupPermission.objects.filter(
            system_group=external_contributor_group, emailuser=user
        ).exists():
            return

        # Add user back into the external contributors group
        SystemGroupPermission.objects.create(
            system_group=external_contributor_group, emailuser=user
        )

        # Have to save the group to flush the member cache
        external_contributor_group.save()

        super().delete(*args, **kwargs)


class EmailUserLogEntry(CommunicationsLogEntry):
    email_user = models.IntegerField()

    def __str__(self):
        return f"Email User ID: {self.email_user} - {self.subject}"

    class Meta:
        app_label = "boranga"


def email_user_comms_log_document_upload_location(instance, filename):
    return "{}/email_user/{}/communications/{}".format(
        settings.MEDIA_APP_DIR, instance.log_entry.email_user, filename
    )


class EmailUserLogDocument(Document):
    log_entry = models.ForeignKey(
        EmailUserLogEntry, related_name="documents", on_delete=models.CASCADE
    )
    _file = models.FileField(
        upload_to=email_user_comms_log_document_upload_location,
        max_length=512,
        storage=private_storage,
    )

    class Meta:
        app_label = "boranga"


class EmailUserAction(UserAction):
    email_user = models.IntegerField()

    @classmethod
    def log_action(cls, email_user, action, request_user):
        return cls.objects.create(
            email_user=email_user.id,
            who=request_user.id,
            what=str(action),
        )

    class Meta:
        app_label = "boranga"


def log_user_action(self, action, request):
    """As EmailUserRO is outside the boranga app,
    we need to monkey patch it to add the log_user_action method"""
    return EmailUserAction.log_action(self, action, request.user)


setattr(EmailUser, "log_user_action", log_user_action)
