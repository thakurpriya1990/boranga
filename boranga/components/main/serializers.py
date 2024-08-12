from ledger_api_client.ledger_models import EmailUserRO
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from rest_framework import serializers

from boranga.components.main.models import (
    CommunicationsLogEntry,
    GlobalSettings,
    HelpTextEntry,
)
from boranga.helpers import is_django_admin


class CommunicationLogEntrySerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=EmailUser.objects.all(), required=False
    )
    documents = serializers.SerializerMethodField()

    class Meta:
        model = CommunicationsLogEntry
        fields = (
            "id",
            "customer",
            "to",
            "fromm",
            "cc",
            "type",
            "reference",
            "subject" "text",
            "created",
            "staff",
            "proposal" "documents",
        )

    def get_documents(self, obj):
        return [[d.name, d._file.url] for d in obj.documents.all()]


class GlobalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSettings
        fields = ("key", "value")


class EmailUserROSerializerForReferral(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    telephone = serializers.CharField(source="phone_number")
    mobile_phone = serializers.CharField(source="mobile_number")

    class Meta:
        model = EmailUserRO
        fields = (
            "id",
            "name",
            "title",
            "email",
            "telephone",
            "mobile_phone",
        )

    def get_name(self, user):
        return user.get_full_name()


class EmailUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = EmailUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "title",
            "organisation",
            "fullname",
        )

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class LimitedEmailUserSerializer(EmailUserSerializer):
    class Meta:
        model = EmailUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "title",
            "organisation",
            "fullname",
        ]


class HelpTextEntrySerializer(serializers.ModelSerializer):
    user_can_administer = serializers.SerializerMethodField()

    class Meta:
        model = HelpTextEntry
        fields = [
            "id",
            "section_id",
            "text",
            "icon_with_popover",
            "user_can_administer",
        ]

    def get_user_can_administer(self, obj):
        return is_django_admin(self.context["request"])
