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

from boranga.components.conservation_status.models import(
    ConservationCategory,
    ConservationCriteria,
    ConservationChangeCode,
    ConservationStatus,
    ConservationList,
    Species,
    Community,
)
from boranga.components.conservation_status.serializers import(
    ListSpeciesConservationStatusSerializer,
    ListCommunityConservationStatusSerializer,
    ListConservationStatusSerializer,
    InternalSpeciesConservationStatusSerializer,
    SaveSpeciesConservationStatusSerializer,
    CreateSpeciesConservationStatusSerializer,
    InternalCommunityConservationStatusSerializer,
    ConservationStatusLogEntrySerializer,
    ConservationStatusUserActionSerializer,
    #SpeciesConservationStatusLogEntrySerializer,
    #SpeciesConservationStatusUserActionSerializer,
)

import logging

logger = logging.getLogger(__name__)

class GetConservationListDict(views.APIView):
    def get(self, request, format=None):
        species_list = []
        species = Species.objects.all()
        species = species.filter(~Q(scientific_name=None)) # TODO remove later as every species will have scientific name
        if species:
            for specimen in species:
                species_list.append({
                    'id': specimen.id,
                    'name':specimen.scientific_name.name,
                    });
        community_list = []
        communities = Community.objects.all()
        communities = communities.filter(~Q(community_name=None)) # TODO remove later as every community will have community name
        if communities:
            for specimen in communities:
                community_list.append({
                    'id': specimen.id,
                    'name':specimen.community_name.name,
                    });
        conservation_list = []
        lists = ConservationList.objects.filter(applies_to_wa=True)
        if lists:
            for choice in lists:
                conservation_list.append({'id': choice.id,
                    'code': choice.code,
                    });

        conservation_category_list = []
        conservation_categories = ConservationCategory.objects.filter(conservation_list__applies_to_wa=True)
        if conservation_categories:
            for choice in conservation_categories:
                conservation_category_list.append({
                    'id': choice.id,
                    'code': choice.code,
                    'conservation_list_id': choice.conservation_list_id,
                    });
        res_json = {
        "species_list":species_list,
        "community_list":community_list,
        "conservation_list":conservation_list,
        "conservation_category_list":conservation_category_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')


class GetCSProfileDict(views.APIView):
    def get(self, request, format=None):
        group_type = request.GET.get('group_type_name','')
        species_list = []
        if group_type:
            species = Species.objects.filter(group_type__name=group_type)
            species = species.filter(~Q(scientific_name=None)) # TODO remove later as every species will have scientific name
            if species:
                for specimen in species:
                    species_list.append({
                        'id': specimen.id,
                        'name':specimen.scientific_name.name,
                        });
        community_list = []
        communities = Community.objects.all()
        communities = communities.filter(~Q(community_name=None)) # TODO remove later as every community will have community name
        if communities:
            for specimen in communities:
                community_list.append({
                    'id': specimen.id,
                    'name':specimen.community_name.name,
                    });
        conservation_list_values = []
        if group_type and (group_type == GroupType.GROUP_TYPE_FLORA or group_type == GroupType.GROUP_TYPE_FAUNA):
            lists = ConservationList.objects.filter(applies_to_species=True)
        elif group_type and group_type == GroupType.GROUP_TYPE_COMMUNITY:
            lists = ConservationList.objects.filter(applies_to_communities=True)
        if lists:
            for option in lists:
                conservation_list_values.append({
                    'id': option.id,
                    'code':option.code,
                    });
        conservation_category_list = []
        if group_type:
            categories = ConservationCategory.objects.filter()
            if categories:
                for option in categories:
                    conservation_category_list.append({
                        'id': option.id,
                        'code':option.code,
                        'conservation_list_id':option.conservation_list_id,
                        });
        conservation_criteria_list = []
        if group_type:
            criterias = ConservationCriteria.objects.filter()
            if criterias:
                for option in criterias:
                    conservation_criteria_list.append({
                        'id': option.id,
                        'code':option.code,
                        'conservation_list_id':option.conservation_list_id,
                        });
        res_json = {
        "species_list":species_list,
        "community_list":community_list,
        "conservation_list_values":conservation_list_values,
        "conservation_category_list":conservation_category_list,
        "conservation_criteria_list":conservation_criteria_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')


class SpeciesConservationStatusFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()
        # filter_group_type
        filter_group_type = request.GET.get('filter_group_type')
        if filter_group_type:
            queryset = queryset.filter(species__group_type__name=filter_group_type)
        # filter_scientific_name
        filter_scientific_name = request.GET.get('filter_scientific_name')
        if filter_scientific_name and not filter_scientific_name.lower() == 'all':
            queryset = queryset.filter(species__scientific_name=filter_scientific_name)

        filter_common_name = request.GET.get('filter_common_name')
        if filter_common_name and not filter_common_name.lower() == 'all':
            queryset = queryset.filter(species__common_name=filter_common_name)

        filter_phylogenetic_group = request.GET.get('filter_phylogenetic_group')
        if filter_phylogenetic_group and not filter_phylogenetic_group.lower() == 'all':
            queryset = queryset.filter(species__species_taxonomy__phylogenetic_group__id=filter_phylogenetic_group)
        
        filter_family = request.GET.get('filter_family')
        if filter_family and not filter_family.lower() == 'all':
            queryset = queryset.filter(species__species_taxonomy__family__id=filter_family)

        filter_genus = request.GET.get('filter_genus')
        if filter_genus and not filter_genus.lower() == 'all':
            queryset = queryset.filter(species__species_taxonomy__genus__id=filter_genus)
        
        filter_conservation_list = request.GET.get('filter_conservation_list')
        if filter_conservation_list and not filter_conservation_list.lower() == 'all':
            queryset = queryset.filter(current_conservation_list=filter_conservation_list)

        filter_conservation_category = request.GET.get('filter_conservation_category')
        if filter_conservation_category and not filter_conservation_category.lower() == 'all':
            queryset = queryset.filter(current_conservation_category=filter_conservation_category)
        
        filter_region = request.GET.get('filter_region')
        if filter_region and not filter_region.lower() == 'all':
            queryset = queryset.filter(species__region=filter_region)

        filter_district = request.GET.get('filter_district')
        if filter_district and not filter_district.lower() == 'all':
            queryset = queryset.filter(species__district=filter_district)

        filter_application_status = request.GET.get('filter_application_status')
        if filter_application_status and not filter_application_status.lower() == 'all':
            queryset = queryset.filter(processing_status=filter_application_status)

        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        try:
            queryset = super(SpeciesConservationStatusFilterBackend, self).filter_queryset(request, queryset, view)
        except Exception as e:
            print(e)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

class SpeciesConservationStatusRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(SpeciesConservationStatusRenderer, self).render(data, accepted_media_type, renderer_context)

class SpeciesConservationStatusPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (SpeciesConservationStatusFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (SpeciesConservationStatusRenderer,)
    queryset = ConservationStatus.objects.none()
    serializer_class = ListSpeciesConservationStatusSerializer
    page_size = 10

    def get_queryset(self):
        #request_user = self.request.user
        qs = ConservationStatus.objects.none()

        if is_internal(self.request):
            qs = ConservationStatus.objects.all()

        return qs

    @list_route(methods=['GET',], detail=False)
    def species_cs_internal(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListSpeciesConservationStatusSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class CommunityConservationStatusFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()
        
        # filter_group_type
        filter_group_type = request.GET.get('filter_group_type')
        if filter_group_type:
            queryset = queryset.filter(community__group_type__name=filter_group_type)
        
        #filter_community_migrated_id
        filter_community_migrated_id = request.GET.get('filter_community_migrated_id')
        if filter_community_migrated_id and not filter_community_migrated_id.lower() == 'all':
            queryset = queryset.filter(community__community_migrated_id=filter_community_migrated_id)

        # filter_community_name
        filter_community_name = request.GET.get('filter_community_name')
        if filter_community_name and not filter_community_name.lower() == 'all':
            queryset = queryset.filter(community__community_name=filter_community_name)

        # filter_community_status
        filter_community_status = request.GET.get('filter_community_status')
        if filter_community_status and not filter_community_status.lower() == 'all':
            queryset = queryset.filter(community__community_status=filter_community_status)

        filter_conservation_list = request.GET.get('filter_conservation_list')
        if filter_conservation_list and not filter_conservation_list.lower() == 'all':
            queryset = queryset.filter(current_conservation_list=filter_conservation_list)

        filter_conservation_category = request.GET.get('filter_conservation_category')
        if filter_conservation_category and not filter_conservation_category.lower() == 'all':
            queryset = queryset.filter(current_conservation_category=filter_conservation_category)

        filter_region = request.GET.get('filter_region')
        if filter_region and not filter_region.lower() == 'all':
            queryset = queryset.filter(community__region=filter_region)

        filter_district = request.GET.get('filter_district')
        if filter_district and not filter_district.lower() == 'all':
            queryset = queryset.filter(community__district=filter_district)

        filter_application_status = request.GET.get('filter_application_status')
        if filter_application_status and not filter_application_status.lower() == 'all':
            queryset = queryset.filter(processing_status=filter_application_status)

        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        try:
            queryset = super(CommunityConservationStatusFilterBackend, self).filter_queryset(request, queryset, view)
        except Exception as e:
            print(e)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

class CommunityConservationStatusRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(CommunityConservationStatusRenderer, self).render(data, accepted_media_type, renderer_context)

class CommunityConservationStatusPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (CommunityConservationStatusFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (CommunityConservationStatusRenderer,)
    queryset = ConservationStatus.objects.none()
    serializer_class = ListCommunityConservationStatusSerializer
    page_size = 10

    def get_queryset(self):
        #request_user = self.request.user
        qs = ConservationStatus.objects.none()

        if is_internal(self.request):
            qs = ConservationStatus.objects.all()

        return qs

    @list_route(methods=['GET',], detail=False)
    def community_cs_internal(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListCommunityConservationStatusSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class ConservationStatusFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()

        flora = GroupType.GROUP_TYPE_FLORA
        fauna = GroupType.GROUP_TYPE_FAUNA
        community = GroupType.GROUP_TYPE_COMMUNITY
        
        filter_group_type = request.GET.get('filter_group_type')
        if filter_group_type and filter_group_type == flora or filter_group_type == fauna:
            queryset = queryset.filter(species__group_type__name=filter_group_type)
        elif filter_group_type and filter_group_type == community:
            queryset = queryset.filter(community__group_type__name=filter_group_type)
        
        # filter_scientific_name
        filter_scientific_name = request.GET.get('filter_scientific_name')
        if filter_scientific_name and not filter_scientific_name.lower() == 'all':
            queryset = queryset.filter(species=filter_scientific_name)

        # filter_community_name
        filter_community_name = request.GET.get('filter_community_name')
        if filter_community_name and not filter_community_name.lower() == 'all':
            queryset = queryset.filter(community=filter_community_name)

        filter_conservation_list = request.GET.get('filter_conservation_list')
        if filter_conservation_list and not filter_conservation_list.lower() == 'all':
            queryset = queryset.filter(current_conservation_list=filter_conservation_list)

        filter_conservation_category = request.GET.get('filter_conservation_category')
        if filter_conservation_category and not filter_conservation_category.lower() == 'all':
            queryset = queryset.filter(current_conservation_category=filter_conservation_category)

        filter_application_status = request.GET.get('filter_application_status')
        if filter_application_status and not filter_application_status.lower() == 'all':
            queryset = queryset.filter(customer_status=filter_application_status)

        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        try:
            queryset = super(ConservationStatusFilterBackend, self).filter_queryset(request, queryset, view)
        except Exception as e:
            print(e)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

class ConservationStatusRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(ConservationStatusRenderer, self).render(data, accepted_media_type, renderer_context)

class ConservationStatusPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (ConservationStatusFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (ConservationStatusRenderer,)
    queryset = ConservationStatus.objects.none()
    serializer_class = ListConservationStatusSerializer
    page_size = 10

    def get_queryset(self):
        request_user = self.request.user
        qs = ConservationStatus.objects.all()

        if is_internal(self.request):
            qs = ConservationStatus.objects.all()
        elif is_customer(self.request):
            #user_orgs = [org.id for org in request_user.mooringlicensing_organisations.all()]
            #qs = all.filter(Q(org_applicant_id__in=user_orgs) | Q(submitter=request_user) | Q(site_licensee_email=request_user.email))
            qs = qs.filter(Q(submitter=request_user.id))
            return qs

        return qs

    @list_route(methods=['GET',], detail=False)
    def conservation_status_external(self, request, *args, **kwargs):
        qs = self.get_queryset()
        # Not Sure but to filter for only WA listed conservation lists for external
        qs = qs.filter(Q(current_conservation_list__applies_to_wa=True))
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListConservationStatusSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class ConservationStatusViewSet(viewsets.ModelViewSet):
    queryset = ConservationStatus.objects.none()
    serializer_class = InternalSpeciesConservationStatusSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request): #user.is_authenticated():
            qs= ConservationStatus.objects.all()
            return qs
        return ConservationStatus.objects.none()

    def internal_serializer_class(self):
        try:
            instance = self.get_object()
            if instance.species_id:
                return InternalSpeciesConservationStatusSerializer
            elif instance.community_id:
                return InternalCommunityConservationStatusSerializer
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e,'message'):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',], detail=True)
    def internal_conservation_status(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.internal_serializer_class()
        serializer = serializer_class(instance,context={'request':request})
       
        res_json = {
         "conservation_status_obj":serializer.data
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')

    @detail_route(methods=['post'], detail=True)
    @renderer_classes((JSONRenderer,))
    def conservation_status_save(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object() 
                request_data = request.data
                if request_data.get('group_type_name') == GroupType.GROUP_TYPE_FLORA or GroupType.GROUP_TYPE_FAUNA:
                    serializer=SaveSpeciesConservationStatusSerializer(instance, data = request_data)
                else:
                    serializer=SaveCommunityConservationStatusSerializer(instance, data = request_data)

                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    saved_instance = serializer.save()

                    # add the updated Current conservation criteria list [1,2] to the cs instance,
                    saved_instance.current_conservation_criteria.set(request_data.get('current_conservation_criteria'))

                    # add the updated Proposed conservation criteria list [1,2] to the cs instance,
                    saved_instance.proposed_conservation_criteria.set(request_data.get('proposed_conservation_criteria'))
                    
                    serializer_class = self.internal_serializer_class()
                    return_serializer = serializer_class(instance=saved_instance, context={'request': request})
                    #return Response(return_serializer.data)
                    return Response()
        
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',], detail=True)
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = ConservationStatusUserActionSerializer(qs,many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',], detail=True)
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = ConservationStatusLogEntrySerializer(qs,many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',], detail=True)
    @renderer_classes((JSONRenderer,))
    def add_comms_log(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                mutable=request.data._mutable
                request.data._mutable=True
                request.data['conservation_status'] = u'{}'.format(instance.id)
                request.data['staff'] = u'{}'.format(request.user.id)
                request.data._mutable=mutable
                serializer = ConservationStatusLogEntrySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                comms = serializer.save()
                # Save the files
                for f in request.FILES:
                    document = comms.documents.create()
                    document.name = str(request.FILES[f])
                    document._file = request.FILES[f]
                    document.save()
                # End Save Documents

                return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


# class SpeciesConservationStatusViewSet(viewsets.ModelViewSet):
#     queryset = ConservationStatus.objects.none()
#     serializer_class = InternalSpeciesConservationStatusSerializer
#     lookup_field = 'id'

#     def get_queryset(self):
#         user = self.request.user
#         if is_internal(self.request): #user.is_authenticated():
#             qs= ConservationStatus.objects.all()
#             return qs
#         return ConservationStatus.objects.none()

#     @detail_route(methods=['GET',], detail=True)
#     def internal_species_conservation_status(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = InternalSpeciesConservationStatusSerializer(instance,context={'request':request})
       
#         res_json = {
#          "species_conservation_status_obj":serializer.data
#         }
#         res_json = json.dumps(res_json)
#         return HttpResponse(res_json, content_type='application/json')

#     @detail_route(methods=['post'], detail=True)
#     @renderer_classes((JSONRenderer,))
#     def species_conservation_status_save(self, request, *args, **kwargs):
#         try:
#             with transaction.atomic():
#                 instance = self.get_object() 
#                 request_data = request.data
#                 serializer = SaveSpeciesConservationStatusSerializer(instance, data = request_data)
#                 serializer.is_valid(raise_exception=True)
#                 if serializer.is_valid():
#                     saved_instance = serializer.save()

#                     # add the updated Current conservation criteria list [1,2] to the cs instance,
#                     saved_instance.current_conservation_criteria.set(request_data.get('current_conservation_criteria'))

#                     # add the updated Proposed conservation criteria list [1,2] to the cs instance,
#                     saved_instance.proposed_conservation_criteria.set(request_data.get('proposed_conservation_criteria'))
                    
#                     return_serializer = InternalSpeciesConservationStatusSerializer(instance=saved_instance, context={'request': request})
#                     #return Response(return_serializer.data)
#                     return Response()
        
#         except serializers.ValidationError:
#             print(traceback.print_exc())
#             raise
#         except ValidationError as e:
#             raise serializers.ValidationError(repr(e.error_dict))
#         except Exception as e:
#             print(traceback.print_exc())
#             raise serializers.ValidationError(str(e))

#     @detail_route(methods=['GET',], detail=True)
#     def action_log(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             qs = instance.action_logs.all()
#             serializer = SpeciesConservationStatusUserActionSerializer(qs,many=True)
#             return Response(serializer.data)
#         except serializers.ValidationError:
#             print(traceback.print_exc())
#             raise
#         except ValidationError as e:
#             print(traceback.print_exc())
#             raise serializers.ValidationError(repr(e.error_dict))
#         except Exception as e:
#             print(traceback.print_exc())
#             raise serializers.ValidationError(str(e))

#     @detail_route(methods=['GET',], detail=True)
#     def comms_log(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             qs = instance.comms_logs.all()
#             serializer = SpeciesConservationStatusLogEntrySerializer(qs,many=True)
#             return Response(serializer.data)
#         except serializers.ValidationError:
#             print(traceback.print_exc())
#             raise
#         except ValidationError as e:
#             print(traceback.print_exc())
#             raise serializers.ValidationError(repr(e.error_dict))
#         except Exception as e:
#             print(traceback.print_exc())
#             raise serializers.ValidationError(str(e))

#     @detail_route(methods=['POST',], detail=True)
#     @renderer_classes((JSONRenderer,))
#     def add_comms_log(self, request, *args, **kwargs):
#         try:
#             with transaction.atomic():
#                 instance = self.get_object()
#                 mutable=request.data._mutable
#                 request.data._mutable=True
#                 request.data['species_conservation_status'] = u'{}'.format(instance.id)
#                 request.data['staff'] = u'{}'.format(request.user.id)
#                 request.data._mutable=mutable
#                 serializer = SpeciesConservationStatusLogEntrySerializer(data=request.data)
#                 serializer.is_valid(raise_exception=True)
#                 comms = serializer.save()
#                 # Save the files
#                 for f in request.FILES:
#                     document = comms.documents.create()
#                     document.name = str(request.FILES[f])
#                     document._file = request.FILES[f]
#                     document.save()
#                 # End Save Documents

#                 return Response(serializer.data)
#         except serializers.ValidationError:
#             print(traceback.print_exc())
#             raise
#         except ValidationError as e:
#             print(traceback.print_exc())
#             raise serializers.ValidationError(repr(e.error_dict))
#         except Exception as e:
#             print(traceback.print_exc())
#             raise serializers.ValidationError(str(e))


# class CommunityConservationStatusViewSet(viewsets.ModelViewSet):
#     queryset = ConservationStatus.objects.none()
#     serializer_class = InternalCommunityConservationStatusSerializer
#     lookup_field = 'id'

#     def get_queryset(self):
#         user = self.request.user
#         if is_internal(self.request): #user.is_authenticated():
#             qs= ConservationStatus.objects.all()
#             return qs
#         return ConservationStatus.objects.none()

#     @detail_route(methods=['GET',], detail=True)
#     def internal_community_conservation_status(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = InternalCommunityConservationStatusSerializer(instance,context={'request':request})
       
#         res_json = {
#          "community_conservation_status_obj":serializer.data
#         }
#         res_json = json.dumps(res_json)
#         return HttpResponse(res_json, content_type='application/json')
 