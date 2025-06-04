import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from ledger_api_client.ledger_models import EmailUserRO
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from rest_framework import serializers

from boranga.components.main.models import CommunicationsLogEntry, HelpTextEntry
from boranga.helpers import (
    get_choices_for_field,
    get_filter_field_options_for_field,
    get_lookup_field_options_for_field,
    get_openpyxl_data_validation_type_for_django_field,
    is_django_admin,
)

logger = logging.getLogger(__name__)


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


class ContentTypeSerializer(serializers.ModelSerializer):
    model_fields = serializers.SerializerMethodField()
    model_verbose_name = serializers.SerializerMethodField()
    model_abbreviation = serializers.SerializerMethodField()

    class Meta:
        model = ContentType
        fields = "__all__"

    def get_model_verbose_name(self, obj):
        if not obj.model_class():
            return None
        return obj.model_class()._meta.verbose_name.title()

    def get_model_abbreviation(self, obj):
        if not obj.model_class():
            return None
        return obj.model_class().BULK_IMPORT_ABBREVIATION

    def get_model_fields(self, obj):
        if not obj.model_class():
            return []

        content_type = ContentType.objects.get_for_model(obj.model_class()).id

        fields = obj.model_class()._meta.get_fields()
        exclude_fields = []
        if hasattr(obj.model_class(), "BULK_IMPORT_EXCLUDE_FIELDS"):
            exclude_fields = obj.model_class().BULK_IMPORT_EXCLUDE_FIELDS

        def filter_fields(field):
            return (
                field.name not in exclude_fields
                and field.name != "occurrence_report"
                and not field.auto_created
                and not (
                    field.is_relation
                    and type(field)
                    not in [
                        ForeignKey,
                        OneToOneField,
                        ManyToManyField,
                    ]
                )
            )

        fields = list(filter(filter_fields, fields))
        model_fields = []
        for field in fields:
            display_name = (
                field.verbose_name.title()
                if hasattr(field, "verbose_name")
                else field.name
            )
            field_type = str(type(field)).split(".")[-1].replace("'>", "")
            allow_null = field.null if hasattr(field, "null") else None
            max_length = field.max_length if hasattr(field, "max_length") else None
            xlsx_validation_type = get_openpyxl_data_validation_type_for_django_field(
                field
            )

            if isinstance(field, GenericForeignKey):
                continue

            choices = get_choices_for_field(obj.model_class(), field)
            lookup_field_options = get_lookup_field_options_for_field(field)
            filter_field_options = get_filter_field_options_for_field(field)
            model_fields.append(
                {
                    "name": field.name,
                    "display_name": display_name,
                    "content_type": content_type,
                    "type": field_type,
                    "allow_null": allow_null,
                    "max_length": max_length,
                    "xlsx_validation_type": xlsx_validation_type,
                    "choices": choices,
                    "lookup_field_options": lookup_field_options,
                    "filter_field_options": filter_field_options,
                }
            )
        return model_fields


class AbstractOrderedListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order = serializers.IntegerField()
    item = serializers.CharField()


class IntegerFieldEmptytoNullSerializerMixin:
    """
    A mixin to convert empty integer fields to None.
    This is useful for serializers where an empty integer field should be treated as null.
    """

    def to_internal_value(self, data):
        data = data.copy()
        for field_name, field in self.fields.items():
            if (
                isinstance(field, serializers.IntegerField)
                and data.get(field_name) == ""
            ):
                data[field_name] = None
        return super().to_internal_value(data)
