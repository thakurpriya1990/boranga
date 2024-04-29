import logging

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.urls import reverse
from django.utils.encoding import smart_text
from ledger_api_client.ledger_models import EmailUserRO as EmailUser

from boranga.components.emails.emails import TemplateEmailBase

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


class OccurrenceReportAmendmentRequestSendNotificationEmail(TemplateEmailBase):
    subject = "An amendment to your occurrence report is required."
    html_template = "boranga/emails/ocr_proposals/send_amendment_notification.html"
    txt_template = "boranga/emails/ocr_proposals/send_amendment_notification.txt"


class ApproverDeclineSendNotificationEmail(TemplateEmailBase):
    subject = "An Assessor has proposed to decline an Occurrence Report"
    html_template = (
        "boranga/emails/ocr_proposals/send_approver_decline_notification.html"
    )
    txt_template = "boranga/emails/ocr_proposals/send_approver_decline_notification.txt"


class DeclineSendNotificationEmail(TemplateEmailBase):
    subject = "Your Proposal has been declined."
    html_template = "boranga/emails/ocr_proposals/send_decline_notification.html"
    txt_template = "boranga/emails/ocr_proposals/send_decline_notification.txt"


class ApproverApproveSendNotificationEmail(TemplateEmailBase):
    subject = "An Occurrence Report has been recommended for approval."
    html_template = (
        "boranga/emails/ocr_proposals/send_approver_approve_notification.html"
    )
    txt_template = "boranga/emails/ocr_proposals/send_approver_approve_notification.txt"


class ApproverBackToAssessorSendNotificationEmail(TemplateEmailBase):
    subject = "An Occurrence Report has been sent back to the Assessor."
    html_template = (
        "boranga/emails/ocr_proposals/send_approver_back_to_assessor_notification.html"
    )
    txt_template = (
        "boranga/emails/ocr_proposals/send_approver_back_to_assessor_notification.txt"
    )


def send_submit_email_notification(request, occurrence_report):
    email = SubmitSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-occurrence-report-detail",
            kwargs={"occurrence_report_pk": occurrence_report.id},
        )
    )
    if "-internal" not in url:
        # add it. This email is for internal staff (assessors)
        url = f"-internal.{settings.SITE_DOMAIN}".join(
            url.split("." + settings.SITE_DOMAIN)
        )

    context = {"occurrence_report": occurrence_report, "url": url}

    msg = email.send(occurrence_report.assessor_recipients, context=context)
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_occurrence_report_email(msg, occurrence_report, sender=sender)
    # if occurrence_report.org_applicant:
    #     _log_org_email(msg, occurrence_report.org_applicant, occurrence_report.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, occurrence_report.submitter, occurrence_report.submitter, sender=sender)
    return msg


def send_external_submit_email_notification(request, occurrence_report):
    email = ExternalSubmitSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "external-occurrence-report-detail",
            kwargs={"occurrence_report_pk": occurrence_report.id},
        )
    )

    if "-internal" in url:
        # remove '-internal'. This email is for external submitters
        url = "".join(url.split("-internal"))

    context = {
        "occurrence_report": occurrence_report,
        "submitter": EmailUser.objects.get(
            id=occurrence_report.submitter
        ).get_full_name(),
        "url": url,
    }

    msg = email.send(
        EmailUser.objects.get(id=occurrence_report.submitter).email,
        cc=None,
        context=context,
    )
    sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    _log_occurrence_report_email(msg, occurrence_report, sender=sender)
    # if proposal.org_applicant:
    #     _log_org_email(msg, occurrence_report.org_applicant, occurrence_report.submitter, sender=sender)
    # else:
    #     _log_user_email(msg, occurrence_report.submitter, occurrence_report.submitter, sender=sender)
    # _log_user_email(msg, occurrence_report.submitter, occurrence_report.submitter, sender=sender)
    return msg


# send email when Occurrence Report is 'proposed to decline' by assessor.
def send_approver_decline_email_notification(reason, request, occurrence_report):
    email = ApproverDeclineSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-occurrence-report-detail",
            kwargs={"occurrence_report_pk": occurrence_report.id},
        )
    )
    context = {"occurrence_report": occurrence_report, "reason": reason, "url": url}

    msg = email.send(occurrence_report.approver_recipients, context=context)

    sender = get_sender_user()

    _log_occurrence_report_email(msg, occurrence_report, sender=sender)


def send_decline_email_notification(reason, request, occurrence_report):
    email = DeclineSendNotificationEmail()

    context = {"occurrence_report": occurrence_report, "reason": reason}

    submitter = EmailUser.objects.get(id=occurrence_report.submitter)

    msg = email.send(submitter.email, context=context)

    sender = get_sender_user()

    _log_occurrence_report_email(msg, occurrence_report, sender=sender)


# send email when Occurrence Report is 'proposed to approve' by assessor.
def send_approver_approve_email_notification(request, occurrence_report):
    email = ApproverApproveSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-occurrence-report-detail",
            kwargs={"occurrence_report_pk": occurrence_report.id},
        )
    )
    approval_details = occurrence_report.approval_details

    context = {
        "occurrence_report": occurrence_report,
        "approval_details": approval_details,
        "url": url,
    }

    msg = email.send(occurrence_report.approver_recipients, context=context)

    sender = get_sender_user()

    _log_occurrence_report_email(msg, occurrence_report, sender=sender)


def send_approver_back_to_assessor_email_notification(
    request, occurrence_report, reason
):
    email = ApproverBackToAssessorSendNotificationEmail()
    url = request.build_absolute_uri(
        reverse(
            "internal-occurrence-report-detail",
            kwargs={"occurrence_report_pk": occurrence_report.id},
        )
    )

    context = {
        "occurrence_report": occurrence_report,
        "reason": reason,
        "url": url,
    }

    msg = email.send(occurrence_report.assessor_recipients, context=context)

    sender = get_sender_user()

    _log_occurrence_report_email(msg, occurrence_report, sender=sender)


def _log_occurrence_report_email(email_message, occurrence_report, sender=None):
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
        to = EmailUser.objects.get(id=occurrence_report.submitter).email
        fromm = smart_text(sender) if sender else SYSTEM_NAME
        all_ccs = ""

    customer = occurrence_report.submitter

    staff = sender.id

    kwargs = {
        "subject": subject,
        "text": text,
        "occurrence_report": occurrence_report,
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
                "occurrence_report_pk": referral.occurrence_report.id,
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
                "occurrence_report_pk": referral.occurrence_report.id,
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
            kwargs={"occurrence_report_pk": referral.occurrence_report.id},
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


def send_occurrence_report_amendment_email_notification(
    amendment_request, request, occurrence_report
):
    email = OccurrenceReportAmendmentRequestSendNotificationEmail()
    reason = amendment_request.reason.reason
    url = request.build_absolute_uri(
        reverse(
            "external-occurrence-report-detail",
            kwargs={"occurrence_report_pk": occurrence_report.id},
        )
    )

    if "-internal" in url:
        # remove '-internal'. This email is for external submitters
        url = "".join(url.split("-internal"))

    attachments = []
    if amendment_request.amendment_request_documents:
        for doc in amendment_request.amendment_request_documents.all():
            # file_name = doc._file.name
            file_name = doc.name
            attachment = (file_name, doc._file.file.read())
            attachments.append(attachment)

    context = {
        "occurrence_report": occurrence_report,
        "reason": reason,
        "amendment_request_text": amendment_request.text,
        "url": url,
    }

    msg = email.send(
        EmailUser.objects.get(id=occurrence_report.submitter).email,
        cc=[],
        context=context,
        attachments=attachments,
    )

    sender = get_sender_user()

    _log_occurrence_report_email(msg, occurrence_report, sender=sender)
    # if occurrence_report.applicant:
    #     _log_org_email(msg, occurrence_report.applicant, occurrence_report.submitter, sender=sender)


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
