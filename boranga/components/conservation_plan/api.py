import traceback
import pytz
import json
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import viewsets, serializers, status, views
from rest_framework.decorators import action as detail_route, renderer_classes
from rest_framework.decorators import action as list_route
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from ledger_api_client.settings_base import TIME_ZONE
from boranga import settings
from boranga import exceptions
from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from boranga.helpers import is_customer, is_internal
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer
from copy import deepcopy
from django.shortcuts import render, redirect, get_object_or_404

from boranga.components.species_and_communities.models import GroupType
from boranga.components.conservation_status.utils import cs_proposal_submit
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from boranga.components.main.decorators import basic_exception_handler

from boranga.components.main.related_item import RelatedItemsSerializer

from boranga.components.species_and_communities.models import(
    Species,
    Community,
    Region,
    District,
    GroupType,
)

# from boranga.components.conservation_plan.models import( 
#     ConservationPlan,
#     ConservationPlanSpecies,
#     ConservationPlanCommunity,
# )
# from boranga.components.conservation_plan.serializers import(
# ListSpeciesConservationPlanSerializer,) 
from boranga.components.main.utils import (
    check_db_connection,
    handle_validation_error,
)

import logging

logger = logging.getLogger(__name__)

# class SpeciesConservationPlansFilterBackend(DatatablesFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         total_count = queryset.count()

#         # filter_group_type
#         filter_group_type = request.GET.get('filter_group_type')
#         if queryset.model is ConservationPlan:
#             if filter_group_type:
#                 #queryset = queryset.filter(species__group_type__name=filter_group_type)
#                 #changed to application_type (ie group_type)
#                 queryset = queryset.filter(application_type__name=filter_group_type)
#         # elif queryset.model is ConservationStatusReferral:
#         #     if filter_group_type:
#         #         #queryset = queryset.filter(species__group_type__name=filter_group_type)
#         #         #changed to application_type (ie group_type)
#         #         queryset = queryset.filter(conservation_status__application_type__name=filter_group_type)

#         # filter_scientific_name
#         filter_plan_type = request.GET.get('filter_plan_type')
#         if queryset.model is ConservationPlan:
#             if filter_plan_type and not filter_plan_type.lower() == 'all':
#                 queryset = queryset.filter(plan_type__plan_name=filter_plan_type)
#         # elif queryset.model is ConservationStatusReferral:
#         #     if filter_scientific_name and not filter_scientific_name.lower() == 'all':
#         #         queryset = queryset.filter(conservation_status__species__taxonomy__id=filter_scientific_name)
        
#         filter_region = request.GET.get('filter_region')
#         if queryset.model is ConservationPlan:
#             if filter_region and not filter_region.lower() == 'all':
#                 queryset = queryset.filter(region=filter_region)
#         # elif queryset.model is ConservationStatusReferral:
#         #     if filter_region and not filter_region.lower() == 'all':
#         #         queryset = queryset.filter(conservation_status__species__region=filter_region)

#         filter_district = request.GET.get('filter_district')
#         if queryset.model is ConservationPlan:
#             if filter_district and not filter_district.lower() == 'all':
#                 queryset = queryset.filter(district=filter_district)
#         # elif queryset.model is ConservationStatusReferral:
#         #     if filter_district and not filter_district.lower() == 'all':
#         #         queryset = queryset.filter(conservation_status__species__district=filter_district)

#         filter_effective_from_date = request.GET.get('filter_effective_from_date')
#         filter_effective_to_date = request.GET.get('filter_effective_to_date')
#         if queryset.model is ConservationPlan:
#             if filter_effective_from_date:
#                 queryset = queryset.filter(effective_from__gte=filter_effective_from_date)

#             if filter_effective_to_date:
#                 queryset = queryset.filter(effective_to__lte=filter_effective_to_date)

#         filter_review_date = request.GET.get('filter_review_date')
#         if queryset.model is ConservationPlan:
#             if filter_review_date:
#                 queryset = queryset.filter(next_review_date=filter_review_date)

#         # elif queryset.model is ConservationStatusReferral:
#         #     if filter_effective_from_date:
#         #         queryset = queryset.filter(conservation_status__conservationstatusissuanceapprovaldetails__effective_from_date__gte=filter_effective_from_date)

#         #     if filter_effective_to_date:
#         #         queryset = queryset.filter(conservation_status__conservationstatusissuanceapprovaldetails__effective_to_date__lte=filter_effective_to_date)

#         filter_application_status = request.GET.get('filter_application_status')
#         if queryset.model is ConservationPlan:
#             if filter_application_status and not filter_application_status.lower() == 'all':
#                 queryset = queryset.filter(processing_status=filter_application_status)
#         # elif queryset.model is ConservationStatusReferral:
#         #     if filter_application_status and not filter_application_status.lower() == 'all':
#         #         queryset = queryset.filter(conservation_status__processing_status=filter_application_status)

#         getter = request.query_params.get
#         fields = self.get_fields(getter)
#         ordering = self.get_ordering(getter, fields)
#         queryset = queryset.order_by(*ordering)
#         if len(ordering):
#             queryset = queryset.order_by(*ordering)

#         try:
#             queryset = super(SpeciesConservationPlansFilterBackend, self).filter_queryset(request, queryset, view)
#         except Exception as e:
#             print(e)
#         setattr(view, '_datatables_total_count', total_count)
#         return queryset

# class SpeciesConservationPlansRenderer(DatatablesRenderer):
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
#             data['recordsTotal'] = renderer_context['view']._datatables_total_count
#         return super(SpeciesConservationPlansRenderer, self).render(data, accepted_media_type, renderer_context)


# class SpeciesConservationPlansPaginatedViewSet(viewsets.ModelViewSet):
#     filter_backends = (SpeciesConservationPlansFilterBackend,)
#     pagination_class = DatatablesPageNumberPagination
#     renderer_classes = (SpeciesConservationPlansRenderer,)
#     queryset = ConservationPlan.objects.none()
#     serializer_class = ListSpeciesConservationPlanSerializer
#     page_size = 10

#     def get_queryset(self):
#         #request_user = self.request.user
#         qs = ConservationPlan.objects.none()

#         if is_internal(self.request):
#             qs = ConservationPlan.objects.all()

#         return qs

#     @list_route(methods=['GET',], detail=False)
#     def species_cp_internal(self, request, *args, **kwargs):
#         qs = self.get_queryset()
#         qs = self.filter_queryset(qs)

#         self.paginator.page_size = qs.count()
#         result_page = self.paginator.paginate_queryset(qs, request)
#         serializer = ListSpeciesConservationPlanSerializer(result_page, context={'request': request}, many=True)
#         return self.paginator.get_paginated_response(serializer.data)
