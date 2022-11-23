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

def get_sender_user():
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except:
        EmailUser.objects.create(email=sender, password='')
        sender_user = EmailUser.objects.get(email__icontains=sender)
    return sender_user

class SubmitSendNotificationEmail(TemplateEmailBase):
    subject = 'A new Application has been submitted.'
    html_template = 'boranga/emails/cs_proposals/send_submit_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_submit_notification.txt'

class ExternalSubmitSendNotificationEmail(TemplateEmailBase):
    subject = '{} - Confirmation - Application submitted.'.format(settings.DEP_NAME)
    html_template = 'boranga/emails/cs_proposals/send_external_submit_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_external_submit_notification.txt'

class ConservationStatusReferralSendNotificationEmail(TemplateEmailBase):
    subject = 'A referral for a conservation status proposal has been sent to you.'
    html_template = 'boranga/emails/cs_proposals/send_referral_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_referral_notification.txt'

class ConservationStatusReferralRecallNotificationEmail(TemplateEmailBase):
    subject = 'A referral for a conservation status proposal has been recalled.'
    html_template = 'boranga/emails/cs_proposals/send_referral_recall_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_referral_recall_notification.txt'

class ConservationStatusReferralCompleteNotificationEmail(TemplateEmailBase):
    subject = 'A referral for a conservation status has been completed.'
    html_template = 'boranga/emails/cs_proposals/send_referral_complete_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_referral_complete_notification.txt'

class ConservationStatusAmendmentRequestSendNotificationEmail(TemplateEmailBase):
    subject = 'An amendment to your conservation status proposal is required.'
    html_template = 'boranga/emails/cs_proposals/send_amendment_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_amendment_notification.txt'

class ApproverDeclineSendNotificationEmail(TemplateEmailBase):
    subject = 'An Application has been recommended for decline.'
    html_template = 'boranga/emails/cs_proposals/send_approver_decline_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_approver_decline_notification.txt'

class ApproverApproveSendNotificationEmail(TemplateEmailBase):
    subject = 'An Application has been recommended for approval.'
    html_template = 'boranga/emails/cs_proposals/send_approver_approve_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_approver_approve_notification.txt'

class ApproverSendBackNotificationEmail(TemplateEmailBase):
    subject = 'An Application has been sent back by approver.'
    html_template = 'boranga/emails/cs_proposals/send_approver_sendback_notification.html'
    txt_template = 'boranga/emails/cs_proposals/send_approver_sendback_notification.txt'


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

def send_conservation_status_referral_email_notification(referral,request,reminder=False):
    email = ConservationStatusReferralSendNotificationEmail()
    url = request.build_absolute_uri(reverse('internal-conservation-status-referral-detail',kwargs={'cs_proposal_pk':referral.conservation_status.id,'referral_pk':referral.id}))

    context = {
        'cs_proposal': referral.conservation_status,
        'url': url,
        'reminder':reminder,
        'comments': referral.text
    }
    msg = email.send(EmailUser.objects.get(id=referral.referral).email, context=context)
    #sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    sender = get_sender_user()
    _log_conservation_status_referral_email(msg, referral, sender=sender)
    # if referral.conservation_status.applicant:
    #     _log_org_email(msg, referral.conservation_status.applicant, referral.referral, sender=sender)

def send_conservation_status_referral_recall_email_notification(referral,request):
    email = ConservationStatusReferralRecallNotificationEmail()
    url = request.build_absolute_uri(reverse('internal-conservation-status-referral-detail',kwargs={'cs_proposal_pk':referral.conservation_status.id,'referral_pk':referral.id}))

    context = {
        'cs_proposal': referral.conservation_status,
        'url': url,
    }

    msg = email.send(EmailUser.objects.get(id=referral.referral).email, context=context)
    #sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    sender = get_sender_user()
    _log_conservation_status_referral_email(msg, referral, sender=sender)
    # if referral.proposal.applicant:
    #     _log_org_email(msg, referral.proposal.applicant, referral.referral, sender=sender)

def send_conservation_status_referral_complete_email_notification(referral,request):
    email = ConservationStatusReferralCompleteNotificationEmail()
    url = request.build_absolute_uri(reverse('internal-conservation-status-detail',kwargs={'cs_proposal_pk': referral.conservation_status.id}))

    context = {
        'cs_proposal': referral.conservation_status,
        'url': url,
        'referral_comments': referral.referral_comment
    }

    msg = email.send(EmailUser.objects.get(id=referral.sent_by).email, context=context)
    #sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    sender = get_sender_user()
    _log_conservation_status_referral_email(msg, referral, sender=sender)
    # if referral.proposal.applicant:
    #     _log_org_email(msg, referral.proposal.applicant, referral.referral, sender=sender)

def _log_conservation_status_referral_email(email_message, referral, sender=None):
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
        # TODO not sure if referral.conservation_status.applicant.email will works here
        #import ipdb; ipdb.set_trace()
        to = referral.conservation_status.applicant.email if referral.conservation_status.applicant.email else ''
        fromm = smart_text(sender) if sender else SYSTEM_NAME
        all_ccs = ''

    customer = referral.referral

    staff = sender.id

    kwargs = {
        'subject': subject,
        'text': text,
        'conservation_status': referral.conservation_status,
        'customer': customer,
        'staff': staff,
        'to': to,
        'fromm': fromm,
        'cc': all_ccs
    }

    email_entry = ConservationStatusLogEntry.objects.create(**kwargs)

    return email_entry

def send_conservation_status_amendment_email_notification(amendment_request, request, conservation_status):
    email = ConservationStatusAmendmentRequestSendNotificationEmail()
    reason = amendment_request.reason.reason
    url = request.build_absolute_uri(reverse('external-conservation-status-detail',kwargs={'cs_proposal_pk': conservation_status.id}))

    if "-internal" in url:
        # remove '-internal'. This email is for external submitters
        url = ''.join(url.split('-internal'))

    attachments = []
    if amendment_request.cs_amendment_request_documents:
        for doc in amendment_request.cs_amendment_request_documents.all():
            #file_name = doc._file.name
            file_name = doc.name
            attachment = (file_name, doc._file.file.read())
            attachments.append(attachment)


    context = {
        'cs_proposal': conservation_status,
        'reason': reason,
        'amendment_request_text': amendment_request.text,
        'url': url
    }

    all_ccs = []
    # if conservation_status.applicant and conservation_status.applicant.email != conservation_status.submitter.email and conservation_status.applicant.email:
    #         cc_list = conservation_status.applicant.email
    #         if cc_list:
    #             all_ccs = [cc_list]

    msg = email.send(
        EmailUser.objects.get(id=conservation_status.submitter).email,cc=all_ccs,
        context=context,
        attachments=attachments
        )
    #sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    sender = get_sender_user()
    _log_conservation_status_email(msg, conservation_status, sender=sender)
    # if conservation_status.applicant:
    #     _log_org_email(msg, conservation_status.applicant, conservation_status.submitter, sender=sender)

    #send email when Conservation Status Proposal is 'proposed to decline' by assessor.
def send_approver_decline_email_notification(reason, request, conservation_status):
    email = ApproverDeclineSendNotificationEmail()
    url = request.build_absolute_uri(reverse('internal-conservation-status-detail',kwargs={'cs_proposal_pk': conservation_status.id}))
    context = {
        'cs_proposal': conservation_status,
        'reason': reason,
        'url': url
    }

    msg = email.send(
        conservation_status.approver_recipients, 
        context=context
        )
    #sender = request.user if request else EmailUser.objects.get(email__icontains=settings.DEFAULT_FROM_EMAIL)
    sender = get_sender_user()
    _log_conservation_status_email(msg, conservation_status, sender=sender)
    # if conservation_status.org_applicant:
    #     _log_org_email(msg, conservation_status.org_applicant, conservation_status.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, conservation_status.submitter, conservation_status.submitter, sender=sender)

def send_approver_approve_email_notification(request, conservation_status):
    email = ApproverApproveSendNotificationEmail()
    url = request.build_absolute_uri(reverse('internal-conservation-status-detail',kwargs={'cs_proposal_pk': conservation_status.id}))
    context = {
        'effective_from_date' : conservation_status.proposed_issuance_approval.get('effective_from_date'),
        'effective_to_date' : conservation_status.proposed_issuance_approval.get('effective_to_date'),
        'details': conservation_status.proposed_issuance_approval.get('details'),
        'cs_proposal': conservation_status,
        'url': url
    }

    msg = email.send(
        conservation_status.approver_recipients, 
        context=context
        )
    #sender = request.user if request else EmailUser.objects.get(email__icontains=settings.DEFAULT_FROM_EMAIL)
    sender = get_sender_user()
    _log_conservation_status_email(msg, conservation_status, sender=sender)
    # if conservation_status.org_applicant:
    #     _log_org_email(msg, conservation_status.org_applicant, conservation_status.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, conservation_status.submitter, conservation_status.submitter, sender=sender)

def send_proposal_approver_sendback_email_notification(request, conservation_status):
    email = ApproverSendBackNotificationEmail()
    url = request.build_absolute_uri(reverse('internal-conservation-status-detail',kwargs={'cs_proposal_pk': conservation_status.id}))

    if 'test-emails' in request.path_info:
        approver_comment = 'This is my test comment'
    else:
        approver_comment = conservation_status.approver_comment


    context = {
        'cs_proposal': conservation_status,
        'url': url,
        'approver_comment': approver_comment
    }

    msg = email.send(conservation_status.assessor_recipients, context=context)
    #sender = request.user if request else EmailUser.objects.get(email__icontains=settings.DEFAULT_FROM_EMAIL)
    sender = get_sender_user()
    _log_conservation_status_email(msg, conservation_status, sender=sender)
    # if conservation_status.org_applicant:
    #     _log_org_email(msg, conservation_status.org_applicant, conservation_status.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, conservation_status.submitter, conservation_status.submitter, sender=sender)