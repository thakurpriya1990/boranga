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
from boranga.components.conservation_status.utils import cs_proposal_submit
from ledger_api_client.ledger_models import EmailUserRO as EmailUser

from boranga.components.conservation_status.models import(
    ConservationCategory,
    ConservationCriteria,
    ConservationChangeCode,
    ConservationStatus,
    ConservationList,
    ConservationStatusReferral,
    Species,
    Community,
)
from boranga.components.conservation_status.serializers import(
    SendReferralSerializer,
    ListSpeciesConservationStatusSerializer,
    ListCommunityConservationStatusSerializer,
    ListConservationStatusSerializer,
    ConservationStatusSerializer,
    CreateConservationStatusSerializer,
    InternalConservationStatusSerializer,
    InternalSpeciesConservationStatusSerializer,
    SaveSpeciesConservationStatusSerializer,
    CreateSpeciesConservationStatusSerializer,
    InternalCommunityConservationStatusSerializer,
    SaveCommunityConservationStatusSerializer,
    ConservationStatusLogEntrySerializer,
    ConservationStatusUserActionSerializer,
    #SpeciesConservationStatusLogEntrySerializer,
    #SpeciesConservationStatusUserActionSerializer,
    ConservationStatusReferralSerializer,
)
from boranga.components.main.utils import (
    check_db_connection,
    handle_validation_error,
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
        group_type = request.GET.get('group_type','')
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
            #queryset = queryset.filter(species__group_type__name=filter_group_type)
            #changed to application_type (ie group_type)
            queryset = queryset.filter(application_type__name=filter_group_type)
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
            queryset = queryset.filter(conservation_list=filter_conservation_list)

        filter_conservation_category = request.GET.get('filter_conservation_category')
        if filter_conservation_category and not filter_conservation_category.lower() == 'all':
            queryset = queryset.filter(conservation_category=filter_conservation_category)
        
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
            #queryset = queryset.filter(community__group_type__name=filter_group_type)
            #changed to application_type (ie group_type)
            queryset = queryset.filter(application_type__name=filter_group_type)
        
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
            queryset = queryset.filter(conservation_list=filter_conservation_list)

        filter_conservation_category = request.GET.get('filter_conservation_category')
        if filter_conservation_category and not filter_conservation_category.lower() == 'all':
            queryset = queryset.filter(conservation_category=filter_conservation_category)

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
        # if filter_group_type and filter_group_type == flora or filter_group_type == fauna:
        #     queryset = queryset.filter(species__group_type__name=filter_group_type)
        # elif filter_group_type and filter_group_type == community:
        #     queryset = queryset.filter(community__group_type__name=filter_group_type)
        if filter_group_type and not filter_group_type.lower() == 'all':
            queryset = queryset.filter(application_type__name=filter_group_type)
        
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
            queryset = queryset.filter(conservation_list=filter_conservation_list)

        filter_conservation_category = request.GET.get('filter_conservation_category')
        if filter_conservation_category and not filter_conservation_category.lower() == 'all':
            queryset = queryset.filter(conservation_category=filter_conservation_category)

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
        # TODO Not Sure but to filter for only WA listed conservation lists for external
        #qs = qs.filter(Q(conservation_list__applies_to_wa=True))
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListConservationStatusSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class ConservationStatusViewSet(viewsets.ModelViewSet):
    queryset = ConservationStatus.objects.none()
    serializer_class = ConservationStatusSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request): #user.is_authenticated():
            qs= ConservationStatus.objects.all()
            return qs
        elif is_customer(self.request):
            user_orgs = [org.id for org in user.boranga_organisations.all()]
            queryset =  ConservationStatus.objects.filter( Q(submitter = user.id) )
            return queryset
        logger.warn("User is neither customer nor internal user: {} <{}>".format(user.get_full_name(), user.email))
        return ConservationStatus.objects.none()

    def get_serializer_class(self):
        try:
            # application_type = Proposal.objects.get(id=self.kwargs.get('id')).application_type.name
            # if application_type == ApplicationType.TCLASS:
            #     return ProposalSerializer
            # elif application_type == ApplicationType.FILMING:
            #     return ProposalFilmingSerializer
            # elif application_type == ApplicationType.EVENT:
            #     return ProposalEventSerializer
            return ConservationStatusSerializer
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

    def internal_serializer_class(self):
        try:
            instance = self.get_object()
            # if instance.application_type.name == GroupType.GROUP_TYPE_FLORA or instance.application_type.name == GroupType.GROUP_TYPE_FAUNA:
            #     return InternalSpeciesConservationStatusSerializer
            # elif instance.application_type.name == GroupType.GROUP_TYPE_COMMUNITY:
            #     return InternalCommunityConservationStatusSerializer
            # TODO try to use below serializer than two above
            return InternalConservationStatusSerializer
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
                if instance.application_type.name == GroupType.GROUP_TYPE_FLORA or instance.application_type.name == GroupType.GROUP_TYPE_FAUNA:
                    serializer=SaveSpeciesConservationStatusSerializer(instance, data = request_data)
                elif instance.application_type.name == GroupType.GROUP_TYPE_COMMUNITY:
                    serializer=SaveCommunityConservationStatusSerializer(instance, data = request_data)

                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    saved_instance = serializer.save()

                    # add the updated Current conservation criteria list [1,2] to the cs instance,
                    saved_instance.conservation_criteria.set(request_data.get('conservation_criteria'))

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

    @detail_route(methods=['post'], detail=True)
    @renderer_classes((JSONRenderer,))
    def draft(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                request_data = request.data
                #request.data['submitter'] = u'{}'.format(request.user.id)
                if instance.application_type.name == GroupType.GROUP_TYPE_FLORA or instance.application_type.name == GroupType.GROUP_TYPE_FAUNA:
                    serializer=SaveSpeciesConservationStatusSerializer(instance, data = request_data, partial=True)
                elif instance.application_type.name == GroupType.GROUP_TYPE_COMMUNITY:
                    serializer=SaveCommunityConservationStatusSerializer(instance, data = request_data, partial=True)

                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    saved_instance = serializer.save()

                    # add the updated Current conservation criteria list [1,2] to the cs instance,
                    saved_instance.conservation_criteria.set(request_data.get('conservation_criteria'))

            return redirect(reverse('external'))
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

    @detail_route(methods=['post'], detail=True)
    @renderer_classes((JSONRenderer,))
    def submit(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            #instance.submit(request,self)
            cs_proposal_submit(instance, request)
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
            #return redirect(reverse('external'))
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

    def create(self, request, *args, **kwargs):
        group_type_id = GroupType.objects.get(id=request.data.get('application_type_id'))
        obj = ConservationStatus.objects.create(
                #submitter=request.user.id,
                application_type=group_type_id,
                )
        serialized_obj = CreateConservationStatusSerializer(obj)
        return Response(serialized_obj.data)

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

    @detail_route(methods=['GET',], detail=True)
    def assign_request_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.assign_officer(request,request.user)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
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
    def assign_to(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_id = request.data.get('assessor_id',None)
            user = None
            if not user_id:
                raise serializers.ValidationError('An assessor id is required')
            try:
                user = EmailUser.objects.get(id=user_id)
            except EmailUser.DoesNotExist:
                raise serializers.ValidationError('A user with the id passed in does not exist')
            instance.assign_officer(request,user)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
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
    def unassign(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.unassign(request)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
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

    @detail_route(methods=['post'], detail=True)
    def assesor_send_referral(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = SendReferralSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            #text=serializer.validated_data['text']
            #instance.send_referral(request,serializer.validated_data['email'])
            instance.send_referral(request,serializer.validated_data['email'], serializer.validated_data['text'])
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            handle_validation_error(e)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class ConservationStatusReferralViewSet(viewsets.ModelViewSet):
    #queryset = Referral.objects.all()
    queryset = ConservationStatusReferral.objects.none()
    serializer_class = ConservationStatusReferralSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and is_internal(self.request):
            #queryset =  Referral.objects.filter(referral=user)
            queryset =  ConservationStatusReferral.objects.all()
            return queryset
        return ConservationStatusReferral.objects.none()

    # @list_route(methods=['GET',])
    # def filter_list(self, request, *args, **kwargs):
    #     """ Used by the external dashboard filters """
    #     #qs =  self.get_queryset().filter(referral=request.user)
    #     qs =  self.get_queryset()
    #     region_qs =  qs.filter(proposal__region__isnull=False).values_list('proposal__region__name', flat=True).distinct()
    #     #district_qs =  qs.filter(proposal__district__isnull=False).values_list('proposal__district__name', flat=True).distinct()
    #     activity_qs =  qs.filter(proposal__activity__isnull=False).order_by('proposal__activity').distinct('proposal__activity').values_list('proposal__activity', flat=True).distinct()
    #     submitter_qs = qs.filter(proposal__submitter__isnull=False).order_by('proposal__submitter').distinct('proposal__submitter').values_list('proposal__submitter__first_name','proposal__submitter__last_name','proposal__submitter__email')
    #     submitters = [dict(email=i[2], search_term='{} {} ({})'.format(i[0], i[1], i[2])) for i in submitter_qs]
    #     processing_status_qs =  qs.filter(proposal__processing_status__isnull=False).order_by('proposal__processing_status').distinct('proposal__processing_status').values_list('proposal__processing_status', flat=True)
    #     processing_status = [dict(value=i, name='{}'.format(' '.join(i.split('_')).capitalize())) for i in processing_status_qs]
    #     application_types=ApplicationType.objects.filter(visible=True).values_list('name', flat=True)
    #     data = dict(
    #         regions=region_qs,
    #         #districts=district_qs,
    #         activities=activity_qs,
    #         submitters=submitters,
    #         processing_status_choices=processing_status,
    #         application_types=application_types,
    #     )
    #     return Response(data)


    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, context={'request':request})
    #     return Response(serializer.data)

    # @list_route(methods=['GET',])
    # def user_list(self, request, *args, **kwargs):
    #     qs = self.get_queryset().filter(referral=request.user)
    #     serializer = DTReferralSerializer(qs, many=True)
    #     #serializer = DTReferralSerializer(self.get_queryset(), many=True)
    #     return Response(serializer.data)

    # @detail_route(methods=["post"], detail=True)
    # def send_referral(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #         serializer = SendReferralSerializer(
    #             data=request.data, context={"request": request}
    #         )
    #         serializer.is_valid(raise_exception=True)
    #         instance.send_referral(
    #             request,
    #             serializer.validated_data["email"],
    #             serializer.validated_data["text"],
    #         )
    #         serializer = self.get_serializer(instance, context={"request": request})
    #         return Response(serializer.data)
    #     except serializers.ValidationError:
    #         print(traceback.print_exc())
    #         raise
    #     except ValidationError as e:
    #         if hasattr(e, "error_dict"):
    #             raise serializers.ValidationError(repr(e.error_dict))
    #         else:
    #             if hasattr(e, "message"):
    #                 raise serializers.ValidationError(e.message)
    #     except Exception as e:
    #         print(traceback.print_exc())
    #         raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',],detail=True,)
    def remind(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.remind(request)
            serializer = InternalConservationStatusSerializer(instance.conservation_status,context={'request':request})
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
