import logging

from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.utils.encoding import smart_text
from django.urls import reverse
from django.conf import settings
from django.core.files.base import ContentFile
from boranga.components.emails.emails import TemplateEmailBase
from ledger_api_client.ledger_models import EmailUserRO as EmailUser

logger = logging.getLogger(__name__)

SYSTEM_NAME = settings.SYSTEM_NAME_SHORT + " Automated Message"


def get_sender_user():
    sender = settings.DEFAULT_FROM_EMAIL
    try:
        sender_user = EmailUser.objects.get(email__icontains=sender)
    except:
        EmailUser.objects.create(email=sender, password="")
        sender_user = EmailUser.objects.get(email__icontains=sender)
    return sender_user


class SubmitSendNotificationEmail(TemplateEmailBase):
    subject = "A new Occurrence Report has been submitted."
    html_template = "boranga/emails/ocr_proposals/send_submit_notification.html"
    txt_template = "boranga/emails/ocr_proposals/send_submit_notification.txt"


class ExternalSubmitSendNotificationEmail(TemplateEmailBase):
    subject = "{} - Confirmation - Occurrence Report submitted.".format(
        settings.DEP_NAME
    )
    html_template = (
        "boranga/emails/ocr_proposals/send_external_submit_notification.html"
    )
    txt_template = "boranga/emails/ocr_proposals/send_external_submit_notification.txt"


class OccurrenceReportReferralSendNotificationEmail(TemplateEmailBase):
    subject = "A referral for an occurrence report has been sent to you."
    html_template = "boranga/emails/ocr_proposals/send_referral_notification.html"
    txt_template = "boranga/emails/ocr_proposals/send_referral_notification.txt"


class OccurrenceReportReferralRecallNotificationEmail(TemplateEmailBase):
    subject = "A referral for an occurrence report has been recalled."
    html_template = (
        "boranga/emails/ocr_proposals/send_referral_recall_notification.html"
    )
    txt_template = "boranga/emails/ocr_proposals/send_referral_recall_notification.txt"


class OccurrenceReportReferralCompleteNotificationEmail(TemplateEmailBase):
    subject = "A referral for an occurrence report has been completed."
    html_template = (
        "boranga/emails/ocr_proposals/send_referral_complete_notification.html"
    )
    txt_template = (
        "boranga/emails/ocr_proposals/send_referral_complete_notification.txt"
    )


def send_submit_email_notification(request, ocr_proposal):
    email = SubmitSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-occurrence-report-detail",
            kwargs={"ocr_proposal_pk": ocr_proposal.id},
        )
    )
    if "-internal" not in url:
        # add it. This email is for internal staff (assessors)
        url = "-internal.{}".format(settings.SITE_DOMAIN).join(
            url.split("." + settings.SITE_DOMAIN)
        )

    context = {"ocr_proposal": ocr_proposal, "url": url}

    msg = email.send(ocr_proposal.assessor_recipients, context=context)
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_occurrence_report_email(msg, ocr_proposal, sender=sender)
    # if ocr_proposal.org_applicant:
    #     _log_org_email(msg, ocr_proposal.org_applicant, ocr_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, ocr_proposal.submitter, ocr_proposal.submitter, sender=sender)
    return msg


def send_external_submit_email_notification(request, ocr_proposal):
    email = ExternalSubmitSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "external-occurrence-report-detail",
            kwargs={"ocr_proposal_pk": ocr_proposal.id},
        )
    )

    if "-internal" in url:
        # remove '-internal'. This email is for external submitters
        url = "".join(url.split("-internal"))

    context = {
        "ocr_proposal": ocr_proposal,
        "submitter": EmailUser.objects.get(id=ocr_proposal.submitter).get_full_name(),
        "url": url,
    }

    msg = email.send(
        EmailUser.objects.get(id=ocr_proposal.submitter).email, cc=None, context=context
    )
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_occurrence_report_email(msg, ocr_proposal, sender=sender)
    # if proposal.org_applicant:
    #     _log_org_email(msg, ocr_proposal.org_applicant, ocr_proposal.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, ocr_proposal.submitter, ocr_proposal.submitter, sender=sender)
    # _log_user_email(msg, ocr_proposal.submitter, ocr_proposal.submitter, sender=sender)
    return msg


def _log_occurrence_report_email(email_message, ocr_proposal, sender=None):
    from boranga.components.occurrence.models import OccurrenceReportLogEntry

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
        to = EmailUser.objects.get(id=ocr_proposal.submitter).email
        fromm = smart_text(sender) if sender else SYSTEM_NAME
        all_ccs = ""

    customer = ocr_proposal.submitter

    staff = sender.id

    kwargs = {
        "subject": subject,
        "text": text,
        "occurrence_report": ocr_proposal,
        "customer": customer,
        "staff": staff,
        "to": to,
        "fromm": fromm,
        "cc": all_ccs,
    }

    email_entry = OccurrenceReportLogEntry.objects.create(**kwargs)

    return email_entry


def send_occurrence_report_referral_email_notification(
    referral, request, reminder=False
):
    email = OccurrenceReportReferralSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-occurrence-report-referral-detail",
            kwargs={
                "ocr_proposal_pk": referral.occurrence_report.id,
                "referral_pk": referral.id,
            },
        )
    )

    context = {
        "occurrence_report": referral.occurrence_report,
        "url": url,
        "reminder": reminder,
        "comments": referral.text,
    }
    msg = email.send(EmailUser.objects.get(id=referral.referral).email, context=context)

    sender = get_sender_user()
    _log_occurrence_report_referral_email(msg, referral, sender=sender)
    # if referral.occurrence_report.applicant:
    #     _log_org_email(msg, referral.occurrence_report.applicant, referral.referral, sender=sender)


def send_occurrence_report_referral_recall_email_notification(referral, request):
    email = OccurrenceReportReferralRecallNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-occurrence-report-referral-detail",
            kwargs={
                "ocr_proposal_pk": referral.occurrence_report.id,
                "referral_pk": referral.id,
            },
        )
    )

    context = {
        "occurrence_report": referral.occurrence_report,
        "url": url,
    }

    msg = email.send(EmailUser.objects.get(id=referral.referral).email, context=context)

    sender = get_sender_user()
    _log_occurrence_report_referral_email(msg, referral, sender=sender)
    # if referral.proposal.applicant:
    #     _log_org_email(msg, referral.proposal.applicant, referral.referral, sender=sender)


def send_occurrence_report_referral_complete_email_notification(referral, request):
    email = OccurrenceReportReferralCompleteNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-occurrence-report-detail",
            kwargs={"ocr_proposal_pk": referral.occurrence_report.id},
        )
    )

    context = {
        "occurrence_report": referral.occurrence_report,
        "url": url,
        "referral_comments": referral.referral_comment,
    }

    msg = email.send(EmailUser.objects.get(id=referral.sent_by).email, context=context)

    sender = get_sender_user()
    _log_occurrence_report_referral_email(msg, referral, sender=sender)
    # if referral.proposal.applicant:
    #     _log_org_email(msg, referral.proposal.applicant, referral.referral, sender=sender)


def _log_occurrence_report_referral_email(email_message, referral, sender=None):
    from boranga.components.occurrence.models import OccurrenceReportLogEntry

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
        # TODO not sure if referral.occurrence_report.applicant.email will works here
        # import ipdb; ipdb.set_trace()
        to = (
            referral.occurrence_report.applicant.email
            if referral.occurrence_report.applicant.email
            else ""
        )
        fromm = smart_text(sender) if sender else SYSTEM_NAME
        all_ccs = ""

    customer = referral.referral

    staff = sender.id

    kwargs = {
        "subject": subject,
        "text": text,
        "occurrence_report": referral.occurrence_report,
        "customer": customer,
        "staff": staff,
        "to": to,
        "fromm": fromm,
        "cc": all_ccs,
    }

    email_entry = OccurrenceReportLogEntry.objects.create(**kwargs)

    return email_entry
