from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from ledger_api_client.ledger_models import EmailUserRO as EmailUser

from boranga.components.main.models import CommunicationsLogEntry, Document, UserAction

private_storage = FileSystemStorage(
    location=settings.BASE_DIR + "/private-media/", base_url="/private-media/"
)


class UserCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "boranga"
        verbose_name_plural = "User Categories"

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    email_user = models.IntegerField()
    organisation = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    user_category = models.ForeignKey(UserCategory, on_delete=models.PROTECT)

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
