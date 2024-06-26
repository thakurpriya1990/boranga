import logging

from django.conf import settings
from django.db import models
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from ledger_api_client.managed_models import SystemGroup

from boranga.settings import (
    DJANGO_ADMIN_GROUP,
    GROUP_NAME_CONSERVATION_STATUS_APPROVER,
    GROUP_NAME_CONSERVATION_STATUS_ASSESSOR,
    GROUP_NAME_EXTERNAL_CONTRIBUTOR,
    GROUP_NAME_INTERNAL_CONTRIBUTOR,
    GROUP_NAME_OCCURRENCE_APPROVER,
    GROUP_NAME_OCCURRENCE_ASSESSOR,
    GROUP_NAME_READONLY_USER,
    GROUP_NAME_SPECIES_COMMUNITIES_APPROVER,
)

logger = logging.getLogger(__name__)


def superuser_ids_list():
    return list(
        EmailUser.objects.filter(is_superuser=True).values_list("id", flat=True)
    )


def belongs_to_by_user_id(user_id, group_name):
    if user_id in superuser_ids_list():
        return True

    system_group = SystemGroup.objects.filter(name=group_name).first()
    return system_group and user_id in system_group.get_system_group_member_ids()


def belongs_to(request, group_name, internal_only=False, external_only=False):
    if not request.user.is_authenticated:
        return False
    if request.user.is_superuser:
        return True
    if internal_only and not is_internal(request):
        return False
    if external_only and is_internal(request):
        return False

    return belongs_to_by_user_id(request.user.id, group_name)


def belongs_to_groups(request, group_names: list) -> bool:
    if not request.user.is_authenticated:
        return False
    if request.user.is_superuser:
        return True

    for group_name in group_names:
        if belongs_to_by_user_id(request.user.id, group_name):
            return True

    return False


def member_ids(group_name):
    # Centralised member_ids method that includes all superusers (not totally sure we want this yet)
    system_group = SystemGroup.objects.filter(name=group_name).first()
    if not system_group:
        logger.warning(f"SystemGroup {group_name} not found")
        return []

    return system_group.get_system_group_member_ids() + superuser_ids_list()


def is_django_admin(request):
    return belongs_to(request, DJANGO_ADMIN_GROUP, internal_only=True)


def is_readonly_user(request):
    return belongs_to(request, GROUP_NAME_READONLY_USER, internal_only=True)


def is_species_communities_approver(request):
    return belongs_to(
        request, GROUP_NAME_SPECIES_COMMUNITIES_APPROVER, internal_only=True
    )


def is_conservation_status_assessor(request):
    return belongs_to(
        request, GROUP_NAME_CONSERVATION_STATUS_ASSESSOR, internal_only=True
    )


def is_conservation_status_approver(request):
    return belongs_to(
        request, GROUP_NAME_CONSERVATION_STATUS_APPROVER, internal_only=True
    )


def is_internal_contributor(request):
    return belongs_to(request, GROUP_NAME_INTERNAL_CONTRIBUTOR, internal_only=True)


def is_occurrence_assessor(request):
    return belongs_to(request, GROUP_NAME_OCCURRENCE_ASSESSOR, internal_only=True)


def is_occurrence_approver(request):
    return belongs_to(request, GROUP_NAME_OCCURRENCE_APPROVER, internal_only=True)


def is_external_contributor(request):
    return belongs_to(request, GROUP_NAME_EXTERNAL_CONTRIBUTOR, external_only=True)


def is_contributor(request):
    return is_internal_contributor(request) or is_external_contributor(request)


def is_new_external_contributor(user_id):
    from boranga.components.conservation_status.models import ConservationStatus
    from boranga.components.occurrence.models import OccurrenceReport

    if not belongs_to_by_user_id(user_id, GROUP_NAME_EXTERNAL_CONTRIBUTOR):
        return False

    finalised_cs = ConservationStatus.objects.filter(
        submitter=user_id,
        processing_status__in=[
            ConservationStatus.PROCESSING_STATUS_APPROVED,
            ConservationStatus.PROCESSING_STATUS_DECLINED,
        ],
    ).exists()
    finalised_ocr = OccurrenceReport.objects.filter(
        submitter=user_id,
        processing_status__in=[
            OccurrenceReport.PROCESSING_STATUS_APPROVED,
            OccurrenceReport.PROCESSING_STATUS_DECLINED,
        ],
    ).exists()

    return not finalised_cs and not finalised_ocr


def is_conservation_status_referee(request, cs_proposal=None):
    if not request.user.is_authenticated:
        return False

    if request.user.is_superuser:
        return True

    from boranga.components.conservation_status.models import ConservationStatusReferral

    qs = ConservationStatusReferral.objects.filter(referral=request.user.id)
    if cs_proposal:
        qs = qs.filter(conservation_status=cs_proposal)

    return qs.exists()


def in_dbca_domain(request):
    user = request.user
    domain = user.email.split("@")[1]
    if domain in settings.DEPT_DOMAINS:
        if not user.is_staff:
            # hack to reset department user to is_staff==True, if the user logged in externally
            # (external departmentUser login defaults to is_staff=False)
            user.is_staff = True
            user.save()
        return True
    return False


def email_in_dept_domains(email):
    return email.split("@")[1] in settings.DEPT_DOMAINS


def is_in_organisation_contacts(request, organisation):
    return request.user.email in organisation.contacts.all().values_list(
        "email", flat=True
    )


def is_departmentUser(request):
    return request.user.is_authenticated and in_dbca_domain(request)


def is_customer(request):
    return request.user.is_authenticated and not request.user.is_staff


def is_internal(request):
    return is_departmentUser(request) and belongs_to_groups(
        request, settings.INTERNAL_GROUPS
    )


def get_all_officers():
    return EmailUser.objects.filter(groups__name=settings.ADMIN_GROUP)


def get_instance_identifier(instance):
    """Checks the instance for the attributes specified in settings"""
    for field in settings.ACTION_LOGGING_IDENTIFIER_FIELDS:
        if hasattr(instance, field):
            return getattr(instance, field)
    raise AttributeError(
        f"Model instance has no valid identifier to use for logging. Tried: {settings.ACTION_LOGGING_IDENTIFIER_FIELDS}"
    )


def clone_model(
    source_model_class: models.base.ModelBase,
    target_model_class: models.base.ModelBase,
    source_model: models.Model,
    save: bool = False,
) -> models.Model:
    """
    Copies field values from source_model to a new instance of target_model_class.

    Will complain if:
        - source_model is not an instance of source_model_class.
        - the new instance of target_model_class does not contain a field that is in source_model.

    Returns None if source_model is None so caller must check for existence of return value.

    Pass save=True to save the new instance to the database automatically after copying the field values.
    """
    logger.debug(f"Save: {save}")
    if source_model is None:
        return None

    if not isinstance(source_model, source_model_class):
        raise ValueError(
            f"source_model is not an instance of {source_model_class.__name__}"
        )

    target_model = target_model_class()

    try:
        for field in source_model._meta.fields:
            if field.primary_key:
                continue

            setattr(target_model, field.name, getattr(source_model, field.name))
    except AttributeError as e:
        logger.error(
            f"Error copying field values from {source_model} to {target_model}: {e}"
        )
    if save:
        target_model.save()

    return target_model


def convert_external_url_to_internal_url(url):
    if not settings.SITE_SUBDOMAIN_INTERNAL_SUFFIX:
        return url

    if settings.SITE_SUBDOMAIN_INTERNAL_SUFFIX not in url:
        # Add the internal subdomain suffix to the url
        url = f"{settings.SITE_SUBDOMAIN_INTERNAL_SUFFIX}.{settings.SITE_DOMAIN}".join(
            url.split("." + settings.SITE_DOMAIN)
        )
    return url


def convert_internal_url_to_external_url(url):
    if not settings.SITE_SUBDOMAIN_INTERNAL_SUFFIX:
        return url

    if settings.SITE_SUBDOMAIN_INTERNAL_SUFFIX in url:
        # remove '-internal'. This email is for external submitters
        url = "".join(url.split(settings.SITE_SUBDOMAIN_INTERNAL_SUFFIX))
    return url
