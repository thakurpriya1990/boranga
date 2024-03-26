from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import View, TemplateView
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.db import transaction

from datetime import datetime, timedelta

from boranga.helpers import (is_internal, is_customer,
is_boranga_admin, is_django_admin, is_assessor, is_approver,
is_species_processor, is_community_processor, is_conservation_status_referee,
is_conservation_status_editor)
from boranga.forms import *
from boranga.components.conservation_status.models import ConservationStatus,ConservationStatusReferral
from boranga.components.species_and_communities.models import Species, Community
from boranga.components.meetings.models import Meeting
from boranga.components.occurrence.models import OccurrenceReport
from boranga.components.proposals.models import ( 
    # Referral, 
    # Proposal, 
    HelpPage
)
# from boranga.components.compliances.models import Compliance
from boranga.components.proposals.mixins import ReferralOwnerMixin
from boranga.forms import FirstTimeForm, LoginForm

#from ledger.checkout.utils import create_basket_session, create_checkout_session, place_order_submission, get_cookie_basket
from django.core.management import call_command
import json
import os
import mimetypes

from decimal import Decimal

import logging
logger = logging.getLogger('payment_checkout')


class InternalView(UserPassesTestMixin, TemplateView):
    template_name = 'boranga/dash/index.html'

    def test_func(self):
        return is_internal(self.request)

    def get_context_data(self, **kwargs):
        context = super(InternalView, self).get_context_data(**kwargs)
        context['dev'] = settings.DEV_STATIC
        context['dev_url'] = settings.DEV_STATIC_URL
        if hasattr(settings, 'DEV_APP_BUILD_URL') and settings.DEV_APP_BUILD_URL:
            context['app_build_url'] = settings.DEV_APP_BUILD_URL
        return context

class ExternalView(LoginRequiredMixin, TemplateView):
    template_name = 'boranga/dash/index.html'

    def get_context_data(self, **kwargs):
        context = super(ExternalView, self).get_context_data(**kwargs)
        context['dev'] = settings.DEV_STATIC
        context['dev_url'] = settings.DEV_STATIC_URL
        if hasattr(settings, 'DEV_APP_BUILD_URL') and settings.DEV_APP_BUILD_URL:
            context['app_build_url'] = settings.DEV_APP_BUILD_URL
        return context

class InternalSpeciesView(DetailView):
    model = Species
    template_name = 'boranga/dash/index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if is_internal(self.request):
                #return redirect('internal-proposal-detail')
                return super(InternalSpeciesView, self).get(*args, **kwargs)
        kwargs['form'] = LoginForm
        return super(BorangaRoutingView, self).get(*args, **kwargs)

class InternalCommunityView(DetailView):
    model = Community
    template_name = 'boranga/dash/index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if is_internal(self.request):
                #return redirect('internal-proposal-detail')
                return super(InternalCommunityView, self).get(*args, **kwargs)
        kwargs['form'] = LoginForm
        return super(BorangaRoutingView, self).get(*args, **kwargs)

class ExternalConservationStatusView(DetailView):
    model = ConservationStatus
    template_name = 'boranga/dash/index.html'

class InternalConservationStatusView(DetailView):
    model = ConservationStatus
    template_name = 'boranga/dash/index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if is_internal(self.request):
                #return redirect('internal-proposal-detail')
                return super(InternalConservationStatusView, self).get(*args, **kwargs)
            return redirect('external-conservation-status-detail')
        kwargs['form'] = LoginForm
        return super(BorangaRoutingView, self).get(*args, **kwargs)

class InternalConservationStatusDashboardView(DetailView):
    model = ConservationStatus
    template_name = 'boranga/dash/index.html'

class ConservationStatusReferralView(ReferralOwnerMixin, DetailView):
    model = ConservationStatusReferral
    template_name = 'boranga/dash/index.html'

class InternalMeetingDashboardView(DetailView):
    model = Meeting
    template_name = 'boranga/dash/index.html'

# class ReferralView(ReferralOwnerMixin, DetailView):
#     model = Referral
#     template_name = 'boranga/dash/index.html'

class ExternalOccurrenceReportView(DetailView):
    model = OccurrenceReport
    template_name = 'boranga/dash/index.html'

class InternalOccurrenceReportView(DetailView):
    model = OccurrenceReport
    template_name = 'boranga/dash/index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if is_internal(self.request):
                #return redirect('internal-proposal-detail')
                return super(InternalOccurrenceReportView, self).get(*args, **kwargs)
            return redirect('external-occurrence-report-detail')
        kwargs['form'] = LoginForm
        return super(BorangaRoutingView, self).get(*args, **kwargs)

# class ExternalProposalView(DetailView):
#     model = Proposal
#     template_name = 'boranga/dash/index.html'

# class ExternalComplianceView(DetailView):
#     model = Compliance
#     template_name = 'boranga/dash/index.html'

# class InternalComplianceView(DetailView):
#     model = Compliance
#     template_name = 'boranga/dash/index.html'

class BorangaRoutingView(TemplateView):
    template_name = 'boranga/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = settings
        return context

    # def get(self, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #        if is_internal(self.request):
    #            return redirect('internal')
    #        return redirect('external')
    #     kwargs['form'] = LoginForm
    #     return super(BorangaRoutingView, self).get(*args, **kwargs)
    #     return redirect('/accounts/login')


class BorangaContactView(TemplateView):
    template_name = 'boranga/contact.html'

class BorangaFurtherInformationView(TemplateView):
    template_name = 'boranga/further_info.html'

# class InternalProposalView(DetailView):
#     #template_name = 'boranga/index.html'
#     model = Proposal
#     template_name = 'boranga/dash/index.html'

#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             if is_internal(self.request):
#                 #return redirect('internal-proposal-detail')
#                 return super(InternalProposalView, self).get(*args, **kwargs)
#             return redirect('external-proposal-detail')
#         kwargs['form'] = LoginForm
#         return super(BorangaRoutingView, self).get(*args, **kwargs)


@login_required(login_url='home')
def first_time(request):
    context = {}
    if request.method == 'POST':
        form = FirstTimeForm(request.POST)
        redirect_url = form.data['redirect_url']
        if not redirect_url:
            redirect_url = '/'
        if form.is_valid():
            # set user attributes
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.dob = form.cleaned_data['dob']
            request.user.save()
            return redirect(redirect_url)
        context['form'] = form
        context['redirect_url'] = redirect_url
        return render(request, 'boranga/user_profile.html', context)
    # GET default
    if 'next' in request.GET:
        context['redirect_url'] = request.GET['next']
    else:
        context['redirect_url'] = '/'
    context['dev'] = settings.DEV_STATIC
    context['dev_url'] = settings.DEV_STATIC_URL
    #return render(request, 'boranga/user_profile.html', context)
    return render(request, 'boranga/dash/index.html', context)


class HelpView(LoginRequiredMixin, TemplateView):
    template_name = 'boranga/help.html'

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            application_type = kwargs.get('application_type', None)
            if kwargs.get('help_type', None)=='assessor':
                if is_internal(self.request):
                    qs = HelpPage.objects.filter(application_type__name__icontains=application_type, help_type=HelpPage.HELP_TEXT_INTERNAL).order_by('-version')
                    context['help'] = qs.first()
#                else:
#                    return TemplateResponse(self.request, 'boranga/not-permitted.html', context)
#                    context['permitted'] = False
            else:
                qs = HelpPage.objects.filter(application_type__name__icontains=application_type, help_type=HelpPage.HELP_TEXT_EXTERNAL).order_by('-version')
                context['help'] = qs.first()
        return context


class ManagementCommandsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'boranga/mgt-commands.html'

    def test_func(self):
        return self.request.user.is_superuser or (
        is_internal(self.request) and 
        (is_boranga_admin(self.request) or
        is_django_admin(self.request)))

    def post(self, request):
        data = {}
        command_script = request.POST.get('script', None)
        if command_script:
            print ('running {}'.format(command_script))
            call_command(command_script)
            data.update({command_script: 'true'})

        return render(request, self.template_name, data)

def is_authorised_to_access_community_document(request,document_id):
    if is_internal(request):
        #check auth
        return (
            request.user.is_superuser or
            is_boranga_admin(request) or
            is_django_admin(request) or
            is_assessor(request.user) or
            is_approver(request.user) or
            is_community_processor(request.user)
        )

def is_authorised_to_access_species_document(request,document_id):
    if is_internal(request):
        #check auth
        return (
            request.user.is_superuser or
            is_boranga_admin(request) or
            is_django_admin(request) or
            is_assessor(request.user) or
            is_approver(request.user) or
            is_species_processor(request.user)
        )

def is_authorised_to_access_meeting_document(request,document_id):
    if is_internal(request):
        #check auth #TODO review
        return (
            request.user.is_superuser or
            is_boranga_admin(request) or
            is_django_admin(request) or
            is_assessor(request) or
            is_approver(request) or
            is_species_processor(request.user) or
            is_community_processor(request.user) or
            is_conservation_status_editor(request.user) or
            is_conservation_status_referee(request)
        )

def is_authorised_to_access_occurrence_report_document(request,document_id):
    if is_internal(request):
        #check auth
        return (
            request.user.is_superuser or
            is_boranga_admin(request) or
            is_django_admin(request) or
            is_assessor(request.user) or
            is_approver(request.user)
        )
    elif is_customer(request):
        user = request.user
        return OccurrenceReport.objects.filter(internal_application=False,id=document_id).filter(
                submitter=user.id).exists()
    
def is_authorised_to_access_conservation_status_document(request,document_id):
    if is_internal(request):
        #check auth
        return (
            request.user.is_superuser or
            is_boranga_admin(request) or
            is_django_admin(request) or
            is_assessor(request.user) or
            is_approver(request.user) or
            is_conservation_status_editor(request.user) or
            is_conservation_status_referee(request)
        )
    elif is_customer(request):
        user = request.user
        return ConservationStatus.objects.filter(internal_application=False,id=document_id).filter(
                submitter=user.id).exists()

def get_file_path_id(check_str,file_path):
    file_name_path_split = file_path.split("/")
    #if the check_str is in the file path, the next value should be the id
    if check_str in file_name_path_split:
        id_index = file_name_path_split.index(check_str)+1
        if len(file_name_path_split) > id_index and file_name_path_split[id_index].isnumeric():
            return int(file_name_path_split[id_index])
        else:
            return False
    else:
        return False

def is_authorised_to_access_document(request):

        #occurrence reports
        o_document_id = get_file_path_id("occurrence_report",request.path)
        if o_document_id:
            return is_authorised_to_access_occurrence_report_document(request,o_document_id)
    
        #conservation status
        cs_document_id = get_file_path_id("conservation_status",request.path)
        if cs_document_id:
            return is_authorised_to_access_conservation_status_document(request,cs_document_id)

        #meeting
        m_document_id = get_file_path_id("meeting",request.path)
        if m_document_id:
            return is_authorised_to_access_meeting_document(request,m_document_id)
        
        #species
        s_document_id = get_file_path_id("species",request.path)
        if s_document_id:
            return is_authorised_to_access_species_document(request,s_document_id)
        
        #community
        c_document_id = get_file_path_id("community",request.path)
        if c_document_id:
            return is_authorised_to_access_community_document(request,c_document_id)

        return False

def getPrivateFile(request):

    if is_authorised_to_access_document(request):
        file_name_path =  request.path 
        #norm path will convert any traversal or repeat / in to its normalised form
        full_file_path= os.path.normpath(settings.BASE_DIR+file_name_path) 
        #we then ensure the normalised path is within the BASE_DIR (and the file exists)
        if full_file_path.startswith(settings.BASE_DIR) and os.path.isfile(full_file_path):
            extension = file_name_path.split(".")[-1]
            the_file = open(full_file_path, 'rb')
            the_data = the_file.read()
            the_file.close()
            if extension == 'msg':
                return HttpResponse(the_data, content_type="application/vnd.ms-outlook")
            if extension == 'eml':
                return HttpResponse(the_data, content_type="application/vnd.ms-outlook")

            return HttpResponse(the_data, content_type=mimetypes.types_map['.'+str(extension)])
    
    return HttpResponse('Unauthorized', status=401)

