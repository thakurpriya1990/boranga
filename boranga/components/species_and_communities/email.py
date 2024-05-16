import logging

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.urls import reverse
from django.utils.encoding import smart_text
from ledger_api_client.ledger_models import EmailUserRO as EmailUser

from boranga.components.emails.emails import TemplateEmailBase
from boranga.components.species_and_communities.models import private_storage
from boranga.helpers import convert_external_url_to_internal_url

logger = logging.getLogger(__name__)

SYSTEM_NAME = settings.SYSTEM_NAME_SHORT + " Automated Message"


def get_sender_user():
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except EmailUser.DoesNotExist:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)
    return sender_user


class CreateSpeciesSendNotificationEmail(TemplateEmailBase):
    subject = "A new Species has been created."
    html_template = "boranga/emails/send_create_notification.html"
    txt_template = "boranga/emails/send_create_notification.txt"


class UserCreateSpeciesSendNotificationEmail(TemplateEmailBase):
    subject = f"{settings.DEP_NAME} - Confirmation - Species submitted."
    html_template = "boranga/emails/send_user_create_notification.html"
    txt_template = "boranga/emails/send_user_create_notification.txt"


class SplitSpeciesSendNotificationEmail(TemplateEmailBase):
    subject = "A Species has been split."
    html_template = "boranga/emails/send_split_notification.html"
    txt_template = "boranga/emails/send_split_notification.txt"


class CombineSpeciesSendNotificationEmail(TemplateEmailBase):
    subject = "The Species has been combined."
    html_template = "boranga/emails/send_combine_notification.html"
    txt_template = "boranga/emails/send_combine_notification.txt"


class RenameSpeciesSendNotificationEmail(TemplateEmailBase):
    subject = "A Species has been renamed."
    html_template = "boranga/emails/send_rename_notification.html"
    txt_template = "boranga/emails/send_rename_notification.txt"


class CreateCommunitySendNotificationEmail(TemplateEmailBase):
    subject = "A new Community has been created."
    html_template = "boranga/emails/send_create_notification.html"
    txt_template = "boranga/emails/send_create_notification.txt"


class UserCreateCommunitySendNotificationEmail(TemplateEmailBase):
    subject = f"{settings.DEP_NAME} - Confirmation - Community submitted."
    html_template = "boranga/emails/send_user_create_notification.html"
    txt_template = "boranga/emails/send_user_create_notification.txt"


def send_species_create_email_notification(request, species_proposal):
    email = CreateSpeciesSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-species-detail",
            kwargs={"species_proposal_pk": species_proposal.id},
        )
    )
    # add the extra query params as need to load the species detail page
    url = url + "?group_type_name={}&action=view".format(
        species_proposal.group_type.name
    )
    url = convert_external_url_to_internal_url(url)

    context = {"species_community_proposal": species_proposal, "url": url}

    msg = email.send(species_proposal.approver_recipients, context=context)
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_species_email(msg, species_proposal, sender=sender)
    # if species_proposal.org_applicant:
    #     _log_org_email(msg, species_proposal.org_applicant, species_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, species_proposal.submitter, species_proposal.submitter, sender=sender)
    return msg


# created email send to the user who is internal not external
def send_user_species_create_email_notification(request, species_proposal):
    email = UserCreateSpeciesSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-species-detail",
            kwargs={"species_proposal_pk": species_proposal.id},
        )
    )
    # add the extra query params as need to load the species detail page
    url = url + "?group_type_name={}&action=view".format(
        species_proposal.group_type.name
    )

    url = convert_external_url_to_internal_url(url)

    context = {
        "species_community_proposal": species_proposal,
        # 'submitter': species_proposal.submitter.get_full_name(),
        "submitter": EmailUser.objects.get(
            id=species_proposal.submitter
        ).get_full_name(),
        "url": url,
    }
    all_ccs = []
    # if species_proposal.org_applicant and species_proposal.org_applicant.email:
    #     cc_list = species_proposal.org_applicant.email
    #     if cc_list:
    #         all_ccs = [cc_list]

    msg = email.send(
        EmailUser.objects.get(id=species_proposal.submitter).email,
        cc=all_ccs,
        context=context,
    )
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_species_email(msg, species_proposal, sender=sender)
    # if species_proposal.org_applicant:
    #     _log_org_email(msg, species_proposal.org_applicant, species_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, species_proposal.submitter, species_proposal.submitter, sender=sender)
    # _log_user_email(msg, species_proposal.submitter, species_proposal.submitter, sender=sender)
    return msg


# here species_proposal is the original species from split functionality
def send_species_split_email_notification(request, species_proposal):
    email = SplitSpeciesSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse("internal-conservation-status-dashboard", kwargs={})
    )
    url = convert_external_url_to_internal_url(url)

    context = {"species_proposal": species_proposal, "url": url}

    all_ccs = []

    msg = email.send(
        EmailUser.objects.get(id=species_proposal.submitter).email,
        cc=all_ccs,
        context=context,
    )
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_species_email(msg, species_proposal, sender=sender)
    # if species_proposal.org_applicant:
    #     _log_org_email(msg, species_proposal.org_applicant, species_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, species_proposal.submitter, species_proposal.submitter, sender=sender)
    return msg


#  here species_proposal is the new species created in combine species functionality
def send_species_combine_email_notification(request, species_proposal):
    email = CombineSpeciesSendNotificationEmail()
    # TODO this url is doe conservation status dash, will need to add one more url for occurrences dash
    url = request.build_absolute_uri(
        reverse("internal-conservation-status-dashboard", kwargs={})
    )
    url = convert_external_url_to_internal_url(url)

    context = {"species_proposal": species_proposal, "url": url}

    all_ccs = []

    msg = email.send(
        EmailUser.objects.get(id=species_proposal.submitter).email,
        cc=all_ccs,
        context=context,
    )
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_species_email(msg, species_proposal, sender=sender)
    # if species_proposal.org_applicant:
    #     _log_org_email(msg, species_proposal.org_applicant, species_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, species_proposal.submitter, species_proposal.submitter, sender=sender)
    return msg


# here species_proposal is the original species from rename functionality
def send_species_rename_email_notification(request, species_proposal):
    email = RenameSpeciesSendNotificationEmail()
    # TODO this url is doe conservation status dash, will need to add one more url for occurrences dash
    url = request.build_absolute_uri(
        reverse("internal-conservation-status-dashboard", kwargs={})
    )
    url = convert_external_url_to_internal_url(url)

    context = {"species_proposal": species_proposal, "url": url}

    all_ccs = []

    msg = email.send(
        EmailUser.objects.get(id=species_proposal.submitter).email,
        cc=all_ccs,
        context=context,
    )
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_species_email(msg, species_proposal, sender=sender)
    # if species_proposal.org_applicant:
    #     _log_org_email(msg, species_proposal.org_applicant, species_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, species_proposal.submitter, species_proposal.submitter, sender=sender)
    return msg


def send_community_create_email_notification(request, community_proposal):
    email = CreateCommunitySendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-community-detail",
            kwargs={"community_proposal_pk": community_proposal.id},
        )
    )
    # add the extra query params as need to load the species detail page
    url = url + "?group_type_name={}&action=view".format(
        community_proposal.group_type.name
    )
    url = convert_external_url_to_internal_url(url)

    context = {"species_community_proposal": community_proposal, "url": url}

    msg = email.send(community_proposal.approver_recipients, context=context)
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_community_email(msg, community_proposal, sender=sender)
    # if community_proposal.org_applicant:
    #     _log_org_email(msg, community_proposal.org_applicant, community_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, community_proposal.submitter, community_proposal.submitter, sender=sender)
    return msg


# created email send to the user who is internal not external
def send_user_community_create_email_notification(request, community_proposal):
    email = UserCreateCommunitySendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-community-detail",
            kwargs={"community_proposal_pk": community_proposal.id},
        )
    )
    # add the extra query params as need to load the species detail page
    url = url + "?group_type_name={}&action=view".format(
        community_proposal.group_type.name
    )

    url = convert_external_url_to_internal_url(url)

    context = {
        "species_community_proposal": community_proposal,
        # 'submitter': species_proposal.submitter.get_full_name(),
        "submitter": EmailUser.objects.get(
            id=community_proposal.submitter
        ).get_full_name(),
        "url": url,
    }
    all_ccs = []
    # if species_proposal.org_applicant and species_proposal.org_applicant.email:
    #     cc_list = species_proposal.org_applicant.email
    #     if cc_list:
    #         all_ccs = [cc_list]

    msg = email.send(
        EmailUser.objects.get(id=community_proposal.submitter).email,
        cc=all_ccs,
        context=context,
    )
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_community_email(msg, community_proposal, sender=sender)
    # if community_proposal.org_applicant:
    #     _log_org_email(msg, community_proposal.org_applicant, community_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, community_proposal.submitter, community_proposal.submitter, sender=sender)
    # _log_user_email(msg, community_proposal.submitter, community_proposal.submitter, sender=sender)
    return msg


def _log_species_email(
    email_message, species_proposal, sender=None, file_bytes=None, filename=None
):
    from boranga.components.species_and_communities.models import SpeciesLogEntry

    if isinstance(
        email_message,
        (
            EmailMultiAlternatives,
            EmailMessage,
        ),
    ):
        # TODO this will log the plain text body, should we log the html instead
        text = email_message.body
        subject = email_message.subject
        fromm = smart_text(sender) if sender else smart_text(email_message.from_email)
        # the to email is normally a list
        if isinstance(email_message.to, list):
            to = ",".join(email_message.to)
        else:
            to = smart_text(email_message.to)
        # we log the cc and bcc in the same cc field of the log entry as a ',' comma separated string
        all_ccs = []
        if email_message.cc:
            all_ccs += list(email_message.cc)
        if email_message.bcc:
            all_ccs += list(email_message.bcc)
        all_ccs = ",".join(all_ccs)

    else:
        text = smart_text(email_message)
        subject = ""
        # to = cs_proposal.submitter.email
        to = EmailUser.objects.get(id=species_proposal.submitter).email
        fromm = smart_text(sender) if sender else SYSTEM_NAME
        all_ccs = ""

    customer = species_proposal.submitter

    staff = sender.id

    kwargs = {
        "subject": subject,
        "text": text,
        "species": species_proposal,
        "customer": customer,
        "staff": staff,
        "to": to,
        "fromm": fromm,
        "cc": all_ccs,
    }

    email_entry = SpeciesLogEntry.objects.create(**kwargs)

    if file_bytes and filename:
        # attach the file to the comms_log also
        path_to_file = "{}/species/{}/communications/{}".format(
            settings.MEDIA_APP_DIR, species_proposal.id, filename
        )
        # path = default_storage.save(path_to_file, ContentFile(file_bytes))
        private_storage.save(path_to_file, ContentFile(file_bytes))
        email_entry.documents.get_or_create(_file=path_to_file, name=filename)

    return email_entry


def _log_community_email(
    email_message, community_proposal, sender=None, file_bytes=None, filename=None
):
    from boranga.components.species_and_communities.models import CommunityLogEntry

    if isinstance(
        email_message,
        (
            EmailMultiAlternatives,
            EmailMessage,
        ),
    ):
        # TODO this will log the plain text body, should we log the html instead
        text = email_message.body
        subject = email_message.subject
        fromm = smart_text(sender) if sender else smart_text(email_message.from_email)
        # the to email is normally a list
        if isinstance(email_message.to, list):
            to = ",".join(email_message.to)
        else:
            to = smart_text(email_message.to)
        # we log the cc and bcc in the same cc field of the log entry as a ',' comma separated string
        all_ccs = []
        if email_message.cc:
            all_ccs += list(email_message.cc)
        if email_message.bcc:
            all_ccs += list(email_message.bcc)
        all_ccs = ",".join(all_ccs)

    else:
        text = smart_text(email_message)
        subject = ""
        # to = cs_proposal.submitter.email
        to = EmailUser.objects.get(id=community_proposal.submitter).email
        fromm = smart_text(sender) if sender else SYSTEM_NAME
        all_ccs = ""

    customer = community_proposal.submitter

    staff = sender.id

    kwargs = {
        "subject": subject,
        "text": text,
        "community": community_proposal,
        "customer": customer,
        "staff": staff,
        "to": to,
        "fromm": fromm,
        "cc": all_ccs,
    }

    email_entry = CommunityLogEntry.objects.create(**kwargs)

    if file_bytes and filename:
        # attach the file to the comms_log also
        path_to_file = "{}/community/{}/communications/{}".format(
            settings.MEDIA_APP_DIR, community_proposal.id, filename
        )
        # path = default_storage.save(path_to_file, ContentFile(file_bytes))
        private_storage.save(path_to_file, ContentFile(file_bytes))
        email_entry.documents.get_or_create(_file=path_to_file, name=filename)

    return email_entry
