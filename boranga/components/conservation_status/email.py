import logging

from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.utils.encoding import smart_text
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from boranga.components.emails.emails import TemplateEmailBase
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from datetime import datetime

logger = logging.getLogger(__name__)

SYSTEM_NAME = settings.SYSTEM_NAME_SHORT + ' Automated Message'

class SubmitSendNotificationEmail(TemplateEmailBase):
    subject = 'A new Application has been submitted.'
    html_template = 'boranga/emails/cs_proposals/send_submit_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_submit_notification.txt'

class ExternalSubmitSendNotificationEmail(TemplateEmailBase):
    subject = '{} - Confirmation - Application submitted.'.format(settings.DEP_NAME)
    html_template = 'boranga/emails/cs_proposals/send_external_submit_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_external_submit_notification.txt'


def send_submit_email_notification(request, cs_proposal):
    email = SubmitSendNotificationEmail()
    url = request.build_absolute_uri(reverse('internal-conservation-status-detail',kwargs={'cs_proposal_pk': cs_proposal.id}))
    if "-internal" not in url:
        # add it. This email is for internal staff (assessors)
        url = '-internal.{}'.format(settings.SITE_DOMAIN).join(url.split('.' + settings.SITE_DOMAIN))

    context = {
        'cs_proposal': cs_proposal,
        'url': url
    }

    msg = email.send(cs_proposal.assessor_recipients, context=context)
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_conservation_status_email(msg, cs_proposal, sender=sender)
    # if cs_proposal.org_applicant:
    #     _log_org_email(msg, cs_proposal.org_applicant, cs_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, cs_proposal.submitter, cs_proposal.submitter, sender=sender)
    return msg

def send_external_submit_email_notification(request, cs_proposal):
    email = ExternalSubmitSendNotificationEmail()
    url = request.build_absolute_uri(reverse('external-conservation-status-detail',kwargs={'cs_proposal_pk': cs_proposal.id}))

    if "-internal" in url:
        # remove '-internal'. This email is for external submitters
        url = ''.join(url.split('-internal'))

    context = {
        'cs_proposal': cs_proposal,
        #'submitter': cs_proposal.submitter.get_full_name(),
        'submitter': EmailUser.objects.get(id=cs_proposal.submitter).get_full_name(),
        'url': url
    }
    all_ccs = []
    # if cs_proposal.org_applicant and cs_proposal.org_applicant.email:
    #     cc_list = cs_proposal.org_applicant.email
    #     if cc_list:
    #         all_ccs = [cc_list]

    msg = email.send(
        EmailUser.objects.get(id=cs_proposal.submitter).email,cc=all_ccs, 
        context=context
        )
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_conservation_status_email(msg, cs_proposal, sender=sender)
    # if proposal.org_applicant:
    #     _log_org_email(msg, cs_proposal.org_applicant, cs_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, cs_proposal.submitter, cs_proposal.submitter, sender=sender)
    #_log_user_email(msg, cs_proposal.submitter, cs_proposal.submitter, sender=sender)
    return msg

def _log_conservation_status_email(email_message, cs_proposal, sender=None, file_bytes=None, filename=None):
    from boranga.components.conservation_status.models import ConservationStatusLogEntry
    if isinstance(email_message, (EmailMultiAlternatives, EmailMessage,)):
        # TODO this will log the plain text body, should we log the html instead
        text = email_message.body
        subject = email_message.subject
        fromm = smart_text(sender) if sender else smart_text(email_message.from_email)
        # the to email is normally a list
        if isinstance(email_message.to, list):
            to = ','.join(email_message.to)
        else:
            to = smart_text(email_message.to)
        # we log the cc and bcc in the same cc field of the log entry as a ',' comma separated string
        all_ccs = []
        if email_message.cc:
            all_ccs += list(email_message.cc)
        if email_message.bcc:
            all_ccs += list(email_message.bcc)
        all_ccs = ','.join(all_ccs)

    else:
        text = smart_text(email_message)
        subject = ''
        #to = cs_proposal.submitter.email
        to = EmailUser.objects.get(id=cs_proposal.submitter).email
        fromm = smart_text(sender) if sender else SYSTEM_NAME
        all_ccs = ''

    customer = cs_proposal.submitter

    staff = sender.id

    kwargs = {
        'subject': subject,
        'text': text,
        'conservation_status': cs_proposal,
        'customer': customer,
        'staff': staff,
        'to': to,
        'fromm': fromm,
        'cc': all_ccs
    }

    email_entry = ConservationStatusLogEntry.objects.create(**kwargs)

    if file_bytes and filename:
        # attach the file to the comms_log also
        path_to_file = '{}/conservation_status/{}/communications/{}'.format(settings.MEDIA_APP_DIR, cs_proposal.id, filename)
        path = default_storage.save(path_to_file, ContentFile(file_bytes))
        email_entry.documents.get_or_create(_file=path_to_file, name=filename)

    return email_entry

def _log_user_email(email_message, emailuser, customer ,sender=None):
    from ledger_api_client.accounts.models import EmailUserLogEntry
    if isinstance(email_message, (EmailMultiAlternatives, EmailMessage,)):
        # TODO this will log the plain text body, should we log the html instead
        text = email_message.body
        subject = email_message.subject
        fromm = smart_text(sender) if sender else smart_text(email_message.from_email)
        # the to email is normally a list
        if isinstance(email_message.to, list):
            to = ','.join(email_message.to)
        else:
            to = smart_text(email_message.to)
        # we log the cc and bcc in the same cc field of the log entry as a ',' comma separated string
        all_ccs = []
        if email_message.cc:
            all_ccs += list(email_message.cc)
        if email_message.bcc:
            all_ccs += list(email_message.bcc)
        all_ccs = ','.join(all_ccs)

    else:
        text = smart_text(email_message)
        subject = ''
        to = customer
        fromm = smart_text(sender) if sender else SYSTEM_NAME
        all_ccs = ''

    customer = customer

    staff = sender

    kwargs = {
        'subject': subject,
        'text': text,
        'emailuser': emailuser,
        'customer': customer,
        'staff': staff,
        'to': to,
        'fromm': fromm,
        'cc': all_ccs
    }

    email_entry = EmailUserLogEntry.objects.create(**kwargs)

    return email_entry