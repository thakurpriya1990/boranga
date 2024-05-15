import logging

from django.conf import settings
from django.db import models
from ledger_api_client.ledger_models import EmailUserRO
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from ledger_api_client.managed_models import SystemGroup

from boranga.settings import (
    GROUP_NAME_CONSERVATION_STATUS_APPROVER,
    GROUP_NAME_CONSERVATION_STATUS_ASSESSOR,
    GROUP_NAME_EXTERNAL_CONTRIBUTOR,
    GROUP_NAME_INTERNAL_CONTRIBUTOR,
    GROUP_NAME_OCCURRENCE_APPROVER,
    GROUP_NAME_OCCURRENCE_ASSESSOR,
    GROUP_NAME_SPECIES_COMMUNITIES_APPROVER,
)

logger = logging.getLogger(__name__)


def belongs_to_by_user_id(user_id, group_name):
    system_group = SystemGroup.objects.filter(name=group_name).first()
    return system_group and user_id in system_group.get_system_group_member_ids()


def belongs_to(request, group_name):
    if not request.user.is_authenticated:
        return False
    if request.user.is_superuser:
        return True

    return belongs_to_by_user_id(request.user.id, group_name)


def is_django_admin(request):
    return belongs_to(request, settings.DJANGO_ADMIN_GROUP)


def is_readonly_user(user_id):
    if isinstance(user_id, EmailUser) or isinstance(user_id, EmailUserRO):
        user_id = user_id.id
    readonly_group = SystemGroup.objects.get(name=settings.GROUP_NAME_READONLY_USER)
    return True if user_id in readonly_group.get_system_group_member_ids() else False


def is_species_communities_approver(user_id):
    if isinstance(user_id, EmailUser) or isinstance(user_id, EmailUserRO):
        user_id = user_id.id
    assessor_group = SystemGroup.objects.get(
        name=GROUP_NAME_SPECIES_COMMUNITIES_APPROVER
    )
    return True if user_id in assessor_group.get_system_group_member_ids() else False


def is_conservation_status_referee(request, cs_proposal=None):
    from boranga.components.conservation_status.models import ConservationStatusReferral

    qs = ConservationStatusReferral.objects.filter(referral=request.user.id)
    if cs_proposal:
        qs = qs.filter(conservation_status=cs_proposal)

    return qs.exists()


def is_conservation_status_assessor(user_id):
    if isinstance(user_id, EmailUser) or isinstance(user_id, EmailUserRO):
        user_id = user_id.id
    assessor_group = SystemGroup.objects.get(
        name=GROUP_NAME_CONSERVATION_STATUS_ASSESSOR
    )
    return True if user_id in assessor_group.get_system_group_member_ids() else False


def is_conservation_status_approver(user_id):
    if isinstance(user_id, EmailUser) or isinstance(user_id, EmailUserRO):
        user_id = user_id.id
    assessor_group = SystemGroup.objects.get(
        name=GROUP_NAME_CONSERVATION_STATUS_APPROVER
    )
    return True if user_id in assessor_group.get_system_group_member_ids() else False


def is_external_contributor(user_id):
    if isinstance(user_id, EmailUser) or isinstance(user_id, EmailUserRO):
        user_id = user_id.id
    assessor_group = SystemGroup.objects.get(name=GROUP_NAME_EXTERNAL_CONTRIBUTOR)
    return True if user_id in assessor_group.get_system_group_member_ids() else False


def is_internal_contributor(user_id):
    if isinstance(user_id, EmailUser) or isinstance(user_id, EmailUserRO):
        user_id = user_id.id
    assessor_group = SystemGroup.objects.get(name=GROUP_NAME_INTERNAL_CONTRIBUTOR)
    return True if user_id in assessor_group.get_system_group_member_ids() else False


def is_occurrence_assessor(user_id):
    if isinstance(user_id, EmailUser) or isinstance(user_id, EmailUserRO):
        user_id = user_id.id
    assessor_group = SystemGroup.objects.get(name=GROUP_NAME_OCCURRENCE_ASSESSOR)
    return True if user_id in assessor_group.get_system_group_member_ids() else False


def is_occurrence_approver(user_id):
    if isinstance(user_id, EmailUser) or isinstance(user_id, EmailUserRO):
        user_id = user_id.id
    assessor_group = SystemGroup.objects.get(name=GROUP_NAME_OCCURRENCE_APPROVER)
    return True if user_id in assessor_group.get_system_group_member_ids() else False


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
    return is_departmentUser(request)


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
