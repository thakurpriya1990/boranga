import logging
import mimetypes
import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from django.views.generic.base import TemplateView

from boranga.components.conservation_status.mixins import ReferralOwnerMixin
from boranga.components.conservation_status.models import (
    ConservationStatus,
    ConservationStatusDocument,
    ConservationStatusReferral,
)
from boranga.components.meetings.models import Meeting
from boranga.components.occurrence.models import OccurrenceReport, Occurrence
from boranga.components.species_and_communities.models import Community, Species
from boranga.forms import LoginForm
from boranga.helpers import (
    is_conservation_status_assessor,
    is_conservation_status_referee,
    is_django_admin,
    is_external_contributor,
    is_internal,
    is_occurrence_approver,
    is_occurrence_assessor,
    is_species_communities_approver,
)

logger = logging.getLogger(__name__)


class InternalView(UserPassesTestMixin, TemplateView):
    template_name = "boranga/dash/index.html"

    def test_func(self):
        return is_internal(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dev"] = settings.DEV_STATIC
        context["dev_url"] = settings.DEV_STATIC_URL
        if hasattr(settings, "DEV_APP_BUILD_URL") and settings.DEV_APP_BUILD_URL:
            context["app_build_url"] = settings.DEV_APP_BUILD_URL
        return context


class PublicView(TemplateView):
    template_name = "boranga/dash/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dev"] = settings.DEV_STATIC
        context["dev_url"] = settings.DEV_STATIC_URL
        if hasattr(settings, "DEV_APP_BUILD_URL") and settings.DEV_APP_BUILD_URL:
            context["app_build_url"] = settings.DEV_APP_BUILD_URL
        return context


class ExternalView(LoginRequiredMixin, TemplateView):
    template_name = "boranga/dash/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dev"] = settings.DEV_STATIC
        context["dev_url"] = settings.DEV_STATIC_URL
        if hasattr(settings, "DEV_APP_BUILD_URL") and settings.DEV_APP_BUILD_URL:
            context["app_build_url"] = settings.DEV_APP_BUILD_URL
        return context


class SpeciesView(TemplateView):
    template_name = "boranga/dash/index.html"


class InternalSpeciesView(DetailView):
    model = Species
    template_name = "boranga/dash/index.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if is_internal(self.request):
                # return redirect('internal-proposal-detail')
                return super().get(*args, **kwargs)
        kwargs["form"] = LoginForm
        return super(BorangaRoutingView, self).get(*args, **kwargs)


class InternalCommunityView(DetailView):
    model = Community
    template_name = "boranga/dash/index.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if is_internal(self.request):
                # return redirect('internal-proposal-detail')
                return super().get(*args, **kwargs)
        kwargs["form"] = LoginForm
        return super(BorangaRoutingView, self).get(*args, **kwargs)


class ExternalConservationStatusView(DetailView):
    model = ConservationStatus
    template_name = "boranga/dash/index.html"


class InternalConservationStatusView(DetailView):
    model = ConservationStatus
    template_name = "boranga/dash/index.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if is_internal(self.request):
                # return redirect('internal-proposal-detail')
                return super().get(*args, **kwargs)
            return redirect("external-conservation-status-detail")
        kwargs["form"] = LoginForm
        return super(BorangaRoutingView, self).get(*args, **kwargs)


class InternalConservationStatusDashboardView(DetailView):
    model = ConservationStatus
    template_name = "boranga/dash/index.html"


class ConservationStatusReferralView(ReferralOwnerMixin, DetailView):
    model = ConservationStatusReferral
    template_name = "boranga/dash/index.html"


class InternalMeetingDashboardView(DetailView):
    model = Meeting
    template_name = "boranga/dash/index.html"


class ExternalOccurrenceReportView(DetailView):
    model = OccurrenceReport
    template_name = "boranga/dash/index.html"

class InternalOccurrenceView(DetailView):
    model = Occurrence
    template_name = "boranga/dash/index.html"


class InternalOccurrenceReportView(DetailView):
    model = OccurrenceReport
    template_name = "boranga/dash/index.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if is_internal(self.request):
                return super().get(*args, **kwargs)
            return redirect("external-occurrence-report-detail")
        kwargs["form"] = LoginForm
        return super(BorangaRoutingView, self).get(*args, **kwargs)


class InternalOccurrenceReportReferralView(TemplateView):
    template_name = "boranga/dash/index.html"


class BorangaRoutingView(TemplateView):
    template_name = "boranga/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        return context


class BorangaContactView(TemplateView):
    template_name = "boranga/contact.html"


class BorangaFurtherInformationView(TemplateView):
    template_name = "boranga/further_info.html"


class ManagementCommandsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "boranga/mgt-commands.html"

    def test_func(self):
        return self.request.user.is_superuser or (
            is_internal(self.request) and is_django_admin(self.request)
        )

    def post(self, request):
        data = {}
        command_script = request.POST.get("script", None)
        if command_script:
            call_command(command_script)
            data.update({command_script: "true"})

        return render(request, self.template_name, data)


def is_authorised_to_access_community_document(request, document_id):
    if is_internal(request):
        # check auth
        return (
            request.user.is_superuser
            or is_django_admin(request)
            or is_species_communities_approver(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
        )
    else:
        return False


def is_authorised_to_access_species_document(request, document_id):
    if is_internal(request):
        # check auth
        return (
            request.user.is_superuser
            or is_django_admin(request)
            or is_species_communities_approver(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
        )
    else:
        return False


def is_authorised_to_access_meeting_document(request, document_id):
    if is_internal(request):
        # check auth #TODO review
        return (
            request.user.is_superuser
            or is_django_admin(request)
            or is_species_communities_approver(request)
            or is_conservation_status_assessor(request)
            or is_conservation_status_referee(request)
        )
    else:
        return False


def check_allowed_path(document_id, path, allowed_paths):
    try:
        file_name_path_split = path.split("/")
        id_index = file_name_path_split.index(str(document_id))
        # take all after the id_index, except the last (the file name) - join and check if in allowed_paths
        check_str = "/".join(file_name_path_split[id_index + 1 : -1])
        return check_str in allowed_paths
    except Exception as e:
        logger.exception(f"Error checking allowed path: {e}")
        return False


def is_authorised_to_access_occurrence_report_document(request, document_id):
    if is_internal(request):
        # check auth
        return (
            request.user.is_superuser
            or is_django_admin(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
        )
    elif is_external_contributor(request):
        allowed_paths = ["documents"]
        path = request.path
        user = request.user
        return OccurrenceReport.objects.filter(
            internal_application=False, id=document_id
        ).filter(submitter=user.id).exists() and check_allowed_path(
            document_id, path, allowed_paths
        )
    else:
        return False


def is_authorised_to_access_occurrence_document(request, document_id):
    if is_internal(request):
        # check auth
        return (
            request.user.is_superuser
            or is_django_admin(request)
            or is_occurrence_assessor(request)
            or is_occurrence_approver(request)
        )
    else:
        return False


def is_authorised_to_access_conservation_status_document(request, document_id):
    if is_internal(request):
        # check auth
        return (
            request.user.is_superuser
            or is_django_admin(request)
            or is_species_communities_approver(request)
            or is_conservation_status_assessor(request)
        )

    if is_external_contributor(request):
        # TODO: Would be nice if the document id was included in the upload path to simplify this query
        file_name = get_file_name_from_path(request.path)
        return ConservationStatusDocument.objects.filter(
            visible=True,
            can_submitter_access=True,
            conservation_status__submitter=request.user.id,
            conservation_status_id=document_id,
            _file=file_name,
        ).exists()

    return False


def get_file_path_id(check_str, file_path):
    file_name_path_split = file_path.split("/")
    # if the check_str is in the file path, the next value should be the id
    if check_str in file_name_path_split:
        id_index = file_name_path_split.index(check_str) + 1
        if (
            len(file_name_path_split) > id_index
            and file_name_path_split[id_index].isnumeric()
        ):
            return int(file_name_path_split[id_index])
        else:
            return False
    else:
        return False


def get_file_name_from_path(file_path):
    file_name_path_split = file_path.split("/private-media/")
    return file_name_path_split[-1]


def is_authorised_to_access_document(request):
    # occurrence reports
    or_document_id = get_file_path_id("occurrence_report", request.path)
    if or_document_id:
        return is_authorised_to_access_occurrence_report_document(
            request, or_document_id
        )

    # occurrence
    o_document_id = get_file_path_id("occurrence", request.path)
    if o_document_id:
        return is_authorised_to_access_occurrence_document(request, o_document_id)

    # conservation status
    # TODO: This 'document id' is actually the conservation status id. Consider renaming these variables
    cs_document_id = get_file_path_id("conservation_status", request.path)
    if cs_document_id:
        return is_authorised_to_access_conservation_status_document(
            request, cs_document_id
        )

    # meeting
    m_document_id = get_file_path_id("meeting", request.path)
    if m_document_id:
        return is_authorised_to_access_meeting_document(request, m_document_id)

    # species
    s_document_id = get_file_path_id("species", request.path)
    if s_document_id:
        return is_authorised_to_access_species_document(request, s_document_id)

    # community
    c_document_id = get_file_path_id("community", request.path)
    if c_document_id:
        return is_authorised_to_access_community_document(request, c_document_id)

    return False


def getPrivateFile(request):

    file_name_path = request.path
    # norm path will convert any traversal or repeat / in to its normalised form
    full_file_path = os.path.normpath(settings.BASE_DIR + file_name_path)

    if not full_file_path.startswith(settings.BASE_DIR):
        return HttpResponse("Unauthorized", status=401)

    if not os.path.isfile(full_file_path):
        return HttpResponse("Not Found", status=404)

    if is_authorised_to_access_document(request):
        # we then ensure the normalised path is within the BASE_DIR (and the file exists)
        extension = file_name_path.split(".")[-1]
        the_file = open(full_file_path, "rb")
        the_data = the_file.read()
        the_file.close()
        if extension == "msg":
            return HttpResponse(the_data, content_type="application/vnd.ms-outlook")
        if extension == "eml":
            return HttpResponse(the_data, content_type="application/vnd.ms-outlook")

        return HttpResponse(
            the_data, content_type=mimetypes.types_map["." + str(extension)]
        )

    return HttpResponse("Unauthorized", status=401)
