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

from boranga.helpers import is_internal
from boranga.forms import *
from boranga.components.conservation_status.models import ConservationStatus,ConservationStatusReferral
from boranga.components.species_and_communities.models import Species, Community
from boranga.components.proposals.models import Referral, Proposal, HelpPage
from boranga.components.compliances.models import Compliance
from boranga.components.proposals.mixins import ReferralOwnerMixin

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
        return super(BorangaRoutingDetailView, self).get(*args, **kwargs)

class InternalCommunityView(DetailView):
    model = Community
    template_name = 'boranga/dash/index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if is_internal(self.request):
                #return redirect('internal-proposal-detail')
                return super(InternalCommunityView, self).get(*args, **kwargs)
        kwargs['form'] = LoginForm
        return super(BorangaRoutingDetailView, self).get(*args, **kwargs)

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
        return super(BorangaRoutingDetailView, self).get(*args, **kwargs)

class InternalConservationStatusDashboardView(DetailView):
    model = ConservationStatus
    template_name = 'boranga/dash/index.html'

class ConservationStatusReferralView(ReferralOwnerMixin, DetailView):
    model = ConservationStatusReferral
    template_name = 'boranga/dash/index.html'

class ReferralView(ReferralOwnerMixin, DetailView):
    model = Referral
    template_name = 'boranga/dash/index.html'

class ExternalProposalView(DetailView):
    model = Proposal
    template_name = 'boranga/dash/index.html'

class ExternalComplianceView(DetailView):
    model = Compliance
    template_name = 'boranga/dash/index.html'

class InternalComplianceView(DetailView):
    model = Compliance
    template_name = 'boranga/dash/index.html'

class BorangaRoutingView(TemplateView):
    template_name = 'boranga/index.html'

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

class InternalProposalView(DetailView):
    #template_name = 'boranga/index.html'
    model = Proposal
    template_name = 'boranga/dash/index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if is_internal(self.request):
                #return redirect('internal-proposal-detail')
                return super(InternalProposalView, self).get(*args, **kwargs)
            return redirect('external-proposal-detail')
        kwargs['form'] = LoginForm
        return super(BorangaRoutingDetailView, self).get(*args, **kwargs)


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


class ManagementCommandsView(LoginRequiredMixin, TemplateView):
    template_name = 'boranga/mgt-commands.html'

    def post(self, request):
        data = {}
        command_script = request.POST.get('script', None)
        if command_script:
            print ('running {}'.format(command_script))
            call_command(command_script)
            data.update({command_script: 'true'})

        return render(request, self.template_name, data)


def getPrivateFile(request):
  allow_access = False
  # Add permission rules
  allow_access = True
  ####

  #if request.user.is_superuser:
  if allow_access == True:
      file_name_path =  request.path 
      full_file_path= settings.BASE_DIR+file_name_path
      if os.path.isfile(full_file_path) is True:
              extension = file_name_path[-3:] 
              the_file = open(full_file_path, 'rb')
              the_data = the_file.read()
              the_file.close()
              if extension == 'msg':
                  return HttpResponse(the_data, content_type="application/vnd.ms-outlook")
              if extension == 'eml':
                  return HttpResponse(the_data, content_type="application/vnd.ms-outlook")

              return HttpResponse(the_data, content_type=mimetypes.types_map['.'+str(extension)])
  else:
              return

