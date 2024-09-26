import logging

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from ledger_api_client.ledger_models import EmailUserRO
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from rest_framework import serializers

from boranga.components.main.models import (
    ArchivableModel,
    CommunicationsLogEntry,
    HelpTextEntry,
)
from boranga.helpers import (
    get_display_field_for_model,
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

    class Meta:
        model = ContentType
        fields = "__all__"

    def get_model_verbose_name(self, obj):
        if not obj.model_class():
            return None
        return obj.model_class()._meta.verbose_name.title()

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
            choices = field.choices if hasattr(field, "choices") else None
            if field_type == "MultiSelectField":
                # Have to create an instance for the choices to be populated :-(
                # as for some reason they are populated in the __init__ method
                instance = obj.model_class()()
                multi_select_field = instance._meta.get_field(field.name)
                choices = multi_select_field.choices

            allow_null = field.null if hasattr(field, "null") else None
            max_length = field.max_length if hasattr(field, "max_length") else None
            xlsx_validation_type = get_openpyxl_data_validation_type_for_django_field(
                field
            )
            lookup_field_options = None

            if isinstance(field, GenericForeignKey):
                continue

            if isinstance(field, (models.ForeignKey, models.ManyToManyField)):
                related_model = field.related_model
                fields = related_model._meta.get_fields()
                lookup_field_options = [
                    field.verbose_name.lower()
                    for field in related_model._meta.get_fields()
                    if not field.related_model
                    and (hasattr(field, "unique") and field.unique)
                    and not field.name.endswith("_number")
                ]

                related_model_qs = related_model.objects.all()

                if issubclass(related_model, ArchivableModel):
                    related_model_qs = related_model_qs.filter(archived=False)

                related_model_count = related_model_qs.count()

                if (
                    related_model_count == 0
                    or related_model_count
                    > settings.OCR_BULK_IMPORT_LOOKUP_TABLE_RECORD_LIMIT
                ):
                    choices = None
                else:
                    display_field = get_display_field_for_model(related_model)
                    choices = list(related_model_qs.values_list("id", display_field))

            model_fields.append(
                {
                    "name": field.name,
                    "display_name": display_name,
                    "content_type": content_type,
                    "type": field_type,
                    "choices": choices,
                    "allow_null": allow_null,
                    "max_length": max_length,
                    "xlsx_validation_type": xlsx_validation_type,
                    "lookup_field_options": lookup_field_options,
                }
            )
        return model_fields
