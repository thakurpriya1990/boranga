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

from boranga.components.main.decorators import basic_exception_handler
from boranga.components.main.related_item import RelatedItemsSerializer

from boranga.components.species_and_communities.models import (
    GroupType,
    Species,
    TaxonVernacular,
    ScientificName,
    Taxonomy,
    Family,
    PhylogeneticGroup,
    Genus,
    NameAuthority,
    CommunityName,
    Community,
    Region,
    District,
    SpeciesDistribution,
    CommunityDistribution,
    FloweringPeriod,
    FruitingPeriod,
    FloraRecruitmentType,
    SeedViabilityGerminationInfo,
    RootMorphology,
    PollinatorInformation,
    PostFireHabitatInteraction,
    BreedingPeriod,
    FaunaBreeding,
    SpeciesConservationAttributes,
    CommunityConservationAttributes,
    DocumentCategory,
    DocumentSubCategory,
    SpeciesDocument,
    CommunityDocument,
    ThreatCategory,
    CurrentImpact,
    PotentialImpact,
    PotentialThreatOnset,
    ConservationThreat,
    CommunityUserAction,
    SpeciesUserAction,
)
from boranga.components.conservation_status.models import(
    ConservationCategory,
    ConservationCriteria,
    ConservationChangeCode,
    ConservationStatus,
    ConservationList,
)
from boranga.components.species_and_communities.serializers import (
    ListSpeciesSerializer,
    ListCommunitiesSerializer,
    InternalSpeciesSerializer,
    SpeciesSerializer,
    SaveSpeciesSerializer,
    CreateSpeciesSerializer,
    SpeciesDistributionSerializer,
    SaveSpeciesDistributionSerializer,
    SpeciesConservationAttributesSerializer,
    SaveSpeciesConservationAttributesSerializer,
    TaxonomySerializer,
    # SaveTaxonomySerializer,
    InternalCommunitySerializer,
    CommunityDistributionSerializer,
    SaveCommunityDistributionSerializer,
    SaveCommunitySerializer,
    CreateCommunitySerializer,
    CommunityConservationAttributesSerializer,
    SaveCommunityConservationAttributesSerializer,
    SpeciesDocumentSerializer,
    CommunityDocumentSerializer,
    SaveSpeciesDocumentSerializer,
    SaveCommunityDocumentSerializer,
    SpeciesLogEntrySerializer,
    SpeciesUserActionSerializer,
    ConservationThreatSerializer,
    SaveConservationThreatSerializer,
    CommunityLogEntrySerializer,
    CommunityUserActionSerializer,
)

                            

class GetGroupTypeDict(views.APIView):
    def get(self, request, format=None):
        group_type_list = []
        group_types = GroupType.objects.all()
        if group_types:
            for group in group_types:
                #group_type_list.append(group.name)
                group_type_list.append({'id': group.id,'name':group.name, 'display':group.get_name_display()});
        return Response(group_type_list)


class GetScientificName(views.APIView):
    def get(self, request, format=None):
        #private_moorings = request.GET.get('private_moorings')
        search_term = request.GET.get('term', '')
        if search_term:
            if search_term:
                data = ScientificName.objects.filter(name__icontains=search_term).values('id', 'name')[:10]
            data_transform = [{'id': species['id'], 'text': species['name']} for species in data]
            return Response({"results": data_transform})
        return Response()


# class GetSpeciesDict(views.APIView):
#     def get(self, request, format=None):
#         group_type = request.GET.get('group_type_name','')
#         species_list = []
#         if group_type:
#             species = Species.objects.filter(group_type__name=group_type)
#             if species:
#                 for specimen in species:
#                     species_list.append({
#                         'species_id': specimen.id,
#                         'common_name':specimen.common_name,
#                         });
#         scientific_name_list = []
#         if group_type:
#             names = ScientificName.objects.all()
#             if names:
#                 for name in names:
#                     scientific_name_list.append({
#                         'id': name.id,
#                         'name': name.name,
#                         });
#         res_json = {
#         "species_list":species_data_list,
#         }
#         res_json = json.dumps(res_json)
#         return HttpResponse(res_json, content_type='application/json')


class GetSpeciesFilterDict(views.APIView):
    def get(self, request, format=None):
        group_type = request.GET.get('group_type_name','')
        # species_data_list = []
        # if group_type:
        #     species = Species.objects.filter(group_type__name=group_type)
        #     if species:
        #         for specimen in species:
        #             species_data_list.append({
        #                 'species_id': specimen.id,
        #                 'common_name':specimen.common_name,
        #                 });
        scientific_name_list = []
        if group_type:
            names = Taxonomy.objects.all() # TODO will need to filter according to  group  selection
            if names:
                for name in names:
                    scientific_name_list.append({
                        'id': name.id,
                        'name': name.scientific_name,
                        });
        common_name_list = []
        if group_type:
            names = TaxonVernacular.objects.all() # TODO will need to filter according to  group  selection
            if names:
                for name in names:
                    common_name_list.append({
                        'id': name.id,
                        'name': name.vernacular_name,
                        });
        family_list = []
        if group_type:
            families = Family.objects.all() # TODO will need to filter according to  group  selection
            if families:
                for family in families:
                    family_list.append({
                        'id': family.id,
                        'name': family.name,
                        });
        phylogenetic_group_list = []
        if group_type:
            phylo_groups = PhylogeneticGroup.objects.all() # TODO will need to filter according to  group  selection
            if phylo_groups:
                for group in phylo_groups:
                    phylogenetic_group_list.append({
                        'id': group.id,
                        'name': group.name,
                        });
        genus_list = []
        if group_type:
            generas = Genus.objects.all() # TODO will need to filter according to  group  selection
            if generas:
                for genus in generas:
                    genus_list.append({
                        'id': genus.id,
                        'name': genus.name,
                        });
        conservation_list_dict = []
        conservation_lists = ConservationList.objects.filter(applies_to_species=True)
        if conservation_lists:
            for choice in conservation_lists:
                conservation_list_dict.append({'id': choice.id,
                    'code': choice.code,
                    });
 
        conservation_category_list = []
        conservation_categories = ConservationCategory.objects.all()
        if conservation_categories:
            for choice in conservation_categories:
                conservation_category_list.append({
                    'id': choice.id,
                    'code': choice.code,
                    'conservation_list_id': choice.conservation_list_id,
                    });
        res_json = {
        "scientific_name_list": scientific_name_list,
        "common_name_list": common_name_list,
        "family_list": family_list,
        "phylogenetic_group_list":phylogenetic_group_list,
        "genus_list":genus_list,
        "conservation_list_dict":conservation_list_dict,
        "conservation_category_list":conservation_category_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')

class GetCommunityFilterDict(views.APIView):
    def get(self, request, format=None):
        group_type = request.GET.get('group_type_name','')
        community_data_list = []
        if group_type:
            communities = Community.objects.filter(group_type__name=group_type)
            if communities:
                for community in communities:
                    community_data_list.append({
                        'id': community.id,
                        'community_migrated_id': community.community_migrated_id,
                        'community_status':community.community_status
                        });
        community_name_list = []
        names = CommunityName.objects.all()
        if names:
            for choice in names:
                community_name_list.append({
                    'id': choice.id,
                    'name': choice.name,
                    });
        conservation_list_dict = []
        conservation_lists = ConservationList.objects.filter(applies_to_communities=True)
        if conservation_lists:
            for choice in conservation_lists:
                conservation_list_dict.append({'id': choice.id,
                    'code': choice.code,
                    });
 
        conservation_category_list = []
        conservation_categories = ConservationCategory.objects.all()
        if conservation_categories:
            for choice in conservation_categories:
                conservation_category_list.append({
                    'id': choice.id,
                    'code': choice.code,
                    'conservation_list_id': choice.conservation_list_id,
                    });
        res_json = {
        "community_data_list":community_data_list,
        "community_name_list":community_name_list,
        "conservation_list_dict":conservation_list_dict,
        "conservation_category_list":conservation_category_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')

class GetRegionDistrictFilterDict(views.APIView):
    def get(self, request, format=None):
        region_list = []
        regions = Region.objects.all()
        if regions:
            for region in regions:
                region_list.append({'id': region.id,
                    'name': region.name,
                    });
        district_list = []
        districts = District.objects.all()
        if districts:
            for district in districts:
                district_list.append({'id': district.id,
                    'name': district.name,
                    'region_id': district.region_id,
                    });
        res_json = {
        "region_list":region_list,
        "district_list":district_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')


class TaxonomyViewSet(viewsets.ModelViewSet):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer

    def get_queryset(self):
        qs = Taxonomy.objects.all()
        return qs

    @list_route(methods=['GET',], detail=False)
    def taxon_names(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = TaxonomySerializer(qs, context={'request': request}, many=True)
        return Response(serializer.data)

class GetSpeciesProfileDict(views.APIView):
    def get(self, request, format=None):
        scientific_name_list = []
        taxons = Taxonomy.objects.all()
        if taxons:
            for taxon in taxons:
                scientific_name_list.append({'id': taxon.id,
                    'name': taxon.scientific_name,
                    'taxon_name_id': taxon.taxon_name_id,
                    'previous_name': taxon.previous_name,
                    'family_id': taxon.family_id,
                    'phylogenetic_group_id': taxon.phylogenetic_group_id,
                    'genus_id': taxon.genus_id,
                    'name_authority_id': taxon.name_authority_id,
                    'name_comments': taxon.name_comments,
                    });
        name_authority_list = []
        name_authorities = NameAuthority.objects.all()
        if name_authorities:
            for name in name_authorities:
                name_authority_list.append({'id': name.id,
                    'name':name.name,
                    });
        family_list = []
        families = Family.objects.all()
        if families:
            for family in families:
                family_list.append({'id': family.id,
                    'name':family.name,
                    });
        phylo_group_list = []
        phylo_groups = PhylogeneticGroup.objects.all()
        if phylo_groups:
            for group in phylo_groups:
                phylo_group_list.append({'id': group.id,
                    'name':group.name,
                    });
        genus_list = []
        generas = Genus.objects.all()
        if generas:
            for genus in generas:
                genus_list.append({'id': genus.id,
                    'name':genus.name,
                    });
        flowering_period_list = []
        periods = FloweringPeriod.objects.all()
        if periods:
            for option in periods:
                flowering_period_list.append({'id': option.id,
                    'name':option.period,
                    });
        fruiting_period_list = []
        periods = FruitingPeriod.objects.all()
        if periods:
            for option in periods:
                fruiting_period_list.append({'id': option.id,
                    'name':option.period,
                    });
        flora_recruitment_type_list = []
        types = FloraRecruitmentType.objects.all()
        if types:
            for option in types:
                flora_recruitment_type_list.append({'id': option.id,
                    'name':option.recruitment_type,
                    });
        seed_viability_germination_info_list = []
        types = SeedViabilityGerminationInfo.objects.all()
        if types:
            for option in types:
                seed_viability_germination_info_list.append({'id': option.id,
                    'name':option.name,
                    });
        root_morphology_list = []
        types = RootMorphology.objects.all()
        if types:
            for option in types:
                root_morphology_list.append({'id': option.id,
                    'name':option.name,
                    });
        pollinator_info_list = []
        types = PollinatorInformation.objects.all()
        if types:
            for option in types:
                pollinator_info_list.append({'id': option.id,
                    'name':option.name,
                    });
        post_fire_habitatat_interactions_list = []
        types = PostFireHabitatInteraction.objects.all()
        if types:
            for option in types:
                post_fire_habitatat_interactions_list.append({'id': option.id,
                    'name':option.name,
                    });
        breeding_period_list = []
        periods = BreedingPeriod.objects.all()
        if periods:
            for option in periods:
                breeding_period_list.append({'id': option.id,
                    'name':option.period,
                    });
        fauna_breeding_list = []
        types = FaunaBreeding.objects.all()
        if types:
            for option in types:
                fauna_breeding_list.append({'id': option.id,
                    'name':option.breeding_type,
                    });
        res_json = {
        "scientific_name_list": scientific_name_list,
        "name_authority_list": name_authority_list,
        "family_list": family_list,
        "genus_list": genus_list,
        "phylo_group_list": phylo_group_list,
        "flowering_period_list": flowering_period_list,
        "fruiting_period_list": fruiting_period_list,
        "flora_recruitment_type_list": flora_recruitment_type_list,
        "seed_viability_germination_info_list": seed_viability_germination_info_list,
        "root_morphology_list": root_morphology_list,
        "pollinator_info_list": pollinator_info_list,
        "post_fire_habitatat_interactions_list": post_fire_habitatat_interactions_list,
        "breeding_period_list": breeding_period_list,
        "fauna_breeding_list": fauna_breeding_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')


class GetCommunityProfileDict(views.APIView):
    def get(self, request, format=None):
        community_name_list = []
        names = CommunityName.objects.all()
        if names:
            for name in names:
                community_name_list.append({'id': name.id,
                    'name':name.name,
                    });
        name_authority_list = []
        name_authorities = NameAuthority.objects.all()
        if name_authorities:
            for name in name_authorities:
                name_authority_list.append({'id': name.id,
                    'name':name.name,
                    });
        pollinator_info_list = []
        types = PollinatorInformation.objects.all()
        if types:
            for option in types:
                pollinator_info_list.append({'id': option.id,
                    'name':option.name,
                    });
        post_fire_habitatat_interactions_list = []
        types = PostFireHabitatInteraction.objects.all()
        if types:
            for option in types:
                post_fire_habitatat_interactions_list.append({'id': option.id,
                    'name':option.name,
                    });
        res_json = {
        "community_name_list":community_name_list,
        "name_authority_list":name_authority_list,
        "pollinator_info_list": pollinator_info_list,
        "post_fire_habitatat_interactions_list": post_fire_habitatat_interactions_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')


class SpeciesFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()
        # filter_group_type
        filter_group_type = request.GET.get('filter_group_type')
        if filter_group_type:
            queryset = queryset.filter(group_type__name=filter_group_type)
        # filter_scientific_name
        filter_scientific_name = request.GET.get('filter_scientific_name')
        if filter_scientific_name and not filter_scientific_name.lower() == 'all':
            queryset = queryset.filter(taxonomy__scientific_name=filter_scientific_name)

        filter_common_name = request.GET.get('filter_common_name')
        if filter_common_name and not filter_common_name.lower() == 'all':
            queryset = queryset.filter(taxonomy__vernaculars__id=filter_common_name)

        filter_phylogenetic_group = request.GET.get('filter_phylogenetic_group')
        if filter_phylogenetic_group and not filter_phylogenetic_group.lower() == 'all':
            queryset = queryset.filter(taxonomy__phylogenetic_group__id=filter_phylogenetic_group)
        
        filter_family = request.GET.get('filter_family')
        if filter_family and not filter_family.lower() == 'all':
            queryset = queryset.filter(taxonomy__family__id=filter_family)

        filter_genus = request.GET.get('filter_genus')
        if filter_genus and not filter_genus.lower() == 'all':
            queryset = queryset.filter(taxonomy__genus__id=filter_genus)
        
        filter_conservation_list = request.GET.get('filter_conservation_list')
        if filter_conservation_list and not filter_conservation_list.lower() == 'all':
            queryset = queryset.filter(conservation_status__conservation_list=filter_conservation_list)

        filter_conservation_category = request.GET.get('filter_conservation_category')
        if filter_conservation_category and not filter_conservation_category.lower() == 'all':
            queryset = queryset.filter(conservation_status__conservation_category=filter_conservation_category)

        filter_application_status = request.GET.get('filter_application_status')
        if filter_application_status and not filter_application_status.lower() == 'all':
                queryset = queryset.filter(processing_status=filter_application_status)

        filter_region = request.GET.get('filter_region')
        if filter_region and not filter_region.lower() == 'all':
            queryset = queryset.filter(region=filter_region)

        filter_district = request.GET.get('filter_district')
        if filter_district and not filter_district.lower() == 'all':
            queryset = queryset.filter(district=filter_district)

        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        try:
            queryset = super(SpeciesFilterBackend, self).filter_queryset(request, queryset, view)
        except Exception as e:
            print(e)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

class SpeciesRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(SpeciesRenderer, self).render(data, accepted_media_type, renderer_context)

class SpeciesPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (SpeciesFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (SpeciesRenderer,)
    queryset = Species.objects.none()
    serializer_class = ListSpeciesSerializer
    page_size = 10

    def get_queryset(self):
        request_user = self.request.user
        qs = Species.objects.none()

        if is_internal(self.request):
            qs = Species.objects.all()

        return qs

    @list_route(methods=['GET',], detail=False)
    def species_internal(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListSpeciesSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)

class CommunitiesFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()
        
        # filter_group_type
        filter_group_type = request.GET.get('filter_group_type')
        if filter_group_type:
            queryset = queryset.filter(group_type__name=filter_group_type)
        
        #filter_community_migrated_id
        filter_community_migrated_id = request.GET.get('filter_community_migrated_id')
        if filter_community_migrated_id and not filter_community_migrated_id.lower() == 'all':
            queryset = queryset.filter(community_migrated_id=filter_community_migrated_id)

        # filter_community_name
        filter_community_name = request.GET.get('filter_community_name')
        if filter_community_name and not filter_community_name.lower() == 'all':
            queryset = queryset.filter(community_name=filter_community_name)

        # filter_community_status
        filter_community_status = request.GET.get('filter_community_status')
        if filter_community_status and not filter_community_status.lower() == 'all':
            queryset = queryset.filter(community_status=filter_community_status)

        filter_conservation_list = request.GET.get('filter_conservation_list')
        if filter_conservation_list and not filter_conservation_list.lower() == 'all':
            queryset = queryset.filter(conservation_status__conservation_list=filter_conservation_list)

        filter_conservation_category = request.GET.get('filter_conservation_category')
        if filter_conservation_category and not filter_conservation_category.lower() == 'all':
            queryset = queryset.filter(conservation_status__conservation_category=filter_conservation_category)

        filter_application_status = request.GET.get('filter_application_status')
        if filter_application_status and not filter_application_status.lower() == 'all':
                queryset = queryset.filter(processing_status=filter_application_status)

        filter_region = request.GET.get('filter_region')
        if filter_region and not filter_region.lower() == 'all':
            queryset = queryset.filter(region=filter_region)

        filter_district = request.GET.get('filter_district')
        if filter_district and not filter_district.lower() == 'all':
            queryset = queryset.filter(district=filter_district)

        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        try:
            queryset = super(CommunitiesFilterBackend, self).filter_queryset(request, queryset, view)
        except Exception as e:
            print(e)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

class CommunitiesRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(CommunitiesRenderer, self).render(data, accepted_media_type, renderer_context)

class CommunitiesPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (CommunitiesFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (CommunitiesRenderer,)
    queryset = Community.objects.none()
    serializer_class = ListCommunitiesSerializer
    page_size = 10

    def get_queryset(self):
        #request_user = self.request.user
        qs = Community.objects.none()

        if is_internal(self.request):
            qs = Community.objects.all()

        return qs

    @list_route(methods=['GET',], detail=False)
    def communities_internal(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListCommunitiesSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = Species.objects.none()
    serializer_class = InternalSpeciesSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request): #user.is_authenticated():
            qs= Species.objects.all()
            return qs
        return Species.objects.none()

    @detail_route(methods=['GET',], detail=True)
    def internal_species(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InternalSpeciesSerializer(instance,context={'request':request})
       
        res_json = {
         "species_obj":serializer.data
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')
        #return Response(d)
    
    @list_route(methods=['GET',], detail=False)
    def filter_list(self, request, *args, **kwargs):
        """ Used by the Related Items dashboard filters """
        related_type =  Species.RELATED_ITEM_CHOICES
        res_json = json.dumps(related_type) 
        return HttpResponse(res_json, content_type='application/json')

    @detail_route(methods=['GET',], detail=False)
    @renderer_classes((JSONRenderer,))
    def species_list(self, request, *args, **kwargs):
        # TODO filter Species that's approved(submitted) only 
        qs= Species.objects.all()
        serializer = SpeciesSerializer(qs, many=True)
        res_json = {
         "data":serializer.data
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')

    @detail_route(methods=['post'], detail=True)
    @renderer_classes((JSONRenderer,))
    def species_save(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object() 
                request_data = request.data
                if(request_data.get('distribution')):
                    distribution_instance, created = SpeciesDistribution.objects.get_or_create(species=instance)
                    serializer = SpeciesDistributionSerializer(distribution_instance, data = request_data.get('distribution'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()
                # No need to submit Taxonomy details due to NOMOS Api
                # if(request_data.get('taxonomy_details')):
                #     taxonomy_instance, created = Taxonomy.objects.get_or_create(species=instance)
                #     serializer = SaveTaxonomySerializer(taxonomy_instance, data = request_data.get('taxonomy_details'))
                #     serializer.is_valid(raise_exception=True)
                #     if serializer.is_valid():
                #         serializer.save()

                if(request_data.get('conservation_attributes')):
                    conservation_attributes_instance, created = SpeciesConservationAttributes.objects.get_or_create(species=instance)
                    serializer = SaveSpeciesConservationAttributesSerializer(conservation_attributes_instance, data = request_data.get('conservation_attributes'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()

                serializer = SaveSpeciesSerializer(instance, data = request_data)
                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    saved_instance = serializer.save()
                    return_serializer = InternalSpeciesSerializer(instance=saved_instance, context={'request': request})
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

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                request_data = request.data
                serializer = CreateSpeciesSerializer(data=request_data)
                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    new_instance = serializer.save()
                    new_returned = serializer.data

                    data={
                        'species_id': new_instance.id
                    }
                    
                    # create SpeciesConservationAttributes for new instance
                    serializer=SaveSpeciesConservationAttributesSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    # create SpeciesDistribution for new instance
                    serializer=SaveSpeciesDistributionSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    
                    headers = self.get_success_headers(serializer.data)
                    return Response(
                        new_returned,
                        status=status.HTTP_201_CREATED,
                        headers=headers
                    )
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
    def documents(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.species_documents.all()
            qs = qs.order_by('-uploaded_date')
            serializer = SpeciesDocumentSerializer(qs,many=True, context={'request':request})
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
    def threats(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.species_threats.all()
            qs = qs.order_by('-date_observed')
            serializer = ConservationThreatSerializer(qs,many=True, context={'request':request})
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
            serializer = SpeciesLogEntrySerializer(qs,many=True)
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
                request.data['species'] = u'{}'.format(instance.id)
                request.data['staff'] = u'{}'.format(request.user.id)
                request.data._mutable=mutable
                serializer = SpeciesLogEntrySerializer(data=request.data)
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
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = SpeciesUserActionSerializer(qs,many=True)
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
    
    @detail_route(methods=["get"], detail=True)
    @basic_exception_handler
    def get_related_items(self, request, *args, **kwargs):
        instance = self.get_object()
        related_filter_type= request.GET.get('related_filter_type')
        related_items = instance.get_related_items(related_filter_type)
        serializer = RelatedItemsSerializer(related_items, many=True)
        return Response(serializer.data)

    @detail_route(methods=['POST',], detail=True)
    def upload_image(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            #import ipdb; ipdb.set_trace()
            instance.upload_image(request)
            with transaction.atomic():
                instance.save()
                instance.log_user_action(SpeciesUserAction.ACTION_IMAGE_UPDATE.format(
                '{} '.format(instance.id)), request)
            serializer = InternalSpeciesSerializer(instance, partial=True)
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
    def delete_image(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            #import ipdb; ipdb.set_trace()
            #instance.upload_image(request)
            with transaction.atomic():
                instance.image_doc=None
                instance.save()
                instance.log_user_action(SpeciesUserAction.ACTION_IMAGE_DELETE.format(
                '{} '.format(instance.id)), request)
            serializer = InternalSpeciesSerializer(instance, partial=True)
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
    


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.none()
    serializer_class = InternalCommunitySerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request): #user.is_authenticated():
            qs= Community.objects.all()
            return qs
        return Community.objects.none()

    @detail_route(methods=['GET',], detail=True)
    def internal_community(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InternalCommunitySerializer(instance,context={'request':request})

        res_json = {
         "community_obj":serializer.data
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')
        #return Response(d)
    
    @list_route(methods=['GET',], detail=False)
    def filter_list(self, request, *args, **kwargs):
        """ Used by the Related Items dashboard filters """
        related_type =  Community.RELATED_ITEM_CHOICES 
        res_json = json.dumps(related_type) 
        return HttpResponse(res_json, content_type='application/json')


    @detail_route(methods=['post'], detail=True)
    @renderer_classes((JSONRenderer,))
    def community_save(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                request_data = request.data
                if(request_data.get('species')):
                    species = request_data.get('species')
                    instance.species.clear()  # first clear all the species set relatedM:M to community instance
                    for species_id in species:
                        species_instance = Species.objects.get(pk=species_id)
                        instance.species.add(species_instance)

                if(request_data.get('distribution')):
                    distribution_instance, created = CommunityDistribution.objects.get_or_create(community=instance)
                    serializer = CommunityDistributionSerializer(distribution_instance, data = request_data.get('distribution'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()

                if(request_data.get('conservation_attributes')):
                    conservation_attributes_instance, created = CommunityConservationAttributes.objects.get_or_create(community=instance)
                    serializer = SaveCommunityConservationAttributesSerializer(conservation_attributes_instance, data = request_data.get('conservation_attributes'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()

                serializer = SaveCommunitySerializer(instance, data = request_data)
                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    saved_instance = serializer.save()
                    return_serializer = InternalCommunitySerializer(instance=saved_instance, context={'request': request})
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

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                request_data = request.data
                serializer = CreateCommunitySerializer(data=request_data)
                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    new_instance = serializer.save()
                    new_returned = serializer.data

                    data={
                        'community_id': new_instance.id
                    }
                    # create CommunityDistribution for new instance
                    serializer=SaveCommunityDistributionSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    # create CommunityConservationAttributes for new instance
                    serializer=SaveCommunityConservationAttributesSerializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    
                    headers = self.get_success_headers(serializer.data)
                    return Response(
                        new_returned,
                        status=status.HTTP_201_CREATED,
                        headers=headers
                    )
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
    def documents(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.community_documents.all()
            qs = qs.order_by('-uploaded_date')
            serializer = CommunityDocumentSerializer(qs,many=True, context={'request':request})
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
    def threats(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.community_threats.all()
            qs = qs.order_by('-date_observed')
            serializer = ConservationThreatSerializer(qs,many=True, context={'request':request})
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
    
    @detail_route(methods=["get"], detail=True)
    @basic_exception_handler
    def get_related_items(self, request, *args, **kwargs):
        instance = self.get_object()
        related_filter_type= request.GET.get('related_filter_type')
        related_items = instance.get_related_items(related_filter_type)
        serializer = RelatedItemsSerializer(related_items, many=True)
        return Response(serializer.data)

    @detail_route(methods=['GET',], detail=True)
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = CommunityLogEntrySerializer(qs,many=True)
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
                request.data['community'] = u'{}'.format(instance.id)
                request.data['staff'] = u'{}'.format(request.user.id)
                request.data._mutable=mutable
                serializer = CommunityLogEntrySerializer(data=request.data)
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
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = CommunityUserActionSerializer(qs,many=True)
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
    def upload_image(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            #import ipdb; ipdb.set_trace()
            instance.upload_image(request)
            with transaction.atomic():
                instance.save()
                instance.log_user_action(CommunityUserAction.ACTION_IMAGE_UPDATE.format(
                '{} '.format(instance.id)), request)
            serializer = InternalCommunitySerializer(instance, partial=True)
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
    def delete_image(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            #import ipdb; ipdb.set_trace()
            #instance.upload_image(request)
            with transaction.atomic():
                instance.image_doc=None
                instance.save()
                instance.log_user_action(CommunityUserAction.ACTION_IMAGE_DELETE.format(
                '{} '.format(instance.id)), request)
            serializer = InternalCommunitySerializer(instance, partial=True)
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
    


class DocumentCategoryViewSet(viewsets.ModelViewSet):
    queryset = DocumentCategory.objects.all()

    def get_queryset(self):
        return DocumentCategory.objects.none()

    @list_route(methods=['GET', ], detail = False)    
    def document_category_choices(self, request, *args, **kwargs):
        res_obj = [] 
        for choice in DocumentCategory.objects.all():
            res_obj.append({'id': choice.id, 'name': choice.document_category_name})
        res_json = json.dumps(res_obj)
        return HttpResponse(res_json, content_type='application/json')


class DocumentSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = DocumentSubCategory.objects.all()

    def get_queryset(self):
        return DocumentSubCategory.objects.none()

    @list_route(methods=['GET', ], detail = False)    
    def document_sub_category_choices(self, request, *args, **kwargs):
        res_obj = [] 
        for choice in DocumentSubCategory.objects.all():
            res_obj.append({'id': choice.id, 'name': choice.document_sub_category_name, 'category_id': choice.document_category_id,})
        res_json = json.dumps(res_obj)
        return HttpResponse(res_json, content_type='application/json')


class SpeciesDocumentViewSet(viewsets.ModelViewSet):
    queryset = SpeciesDocument.objects.all().order_by('id')
    serializer_class = SpeciesDocumentSerializer

    @detail_route(methods=['GET',], detail=True)
    def discard(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.visible = False
            instance.save()
            serializer = self.get_serializer(instance)
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
    def reinstate(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.visible = True
            instance.save()
            serializer = self.get_serializer(instance)
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

    # @detail_route(methods=['POST',], detail=True)
    # @renderer_classes((JSONRenderer,))
    # def delete_document(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #         RequirementDocument.objects.get(id=request.data.get('id')).delete()
    #         return Response([dict(id=i.id, name=i.name,_file=i._file.url) for i in instance.requirement_documents.all()])
    #     except serializers.ValidationError:
    #         print(traceback.print_exc())
    #         raise
    #     except ValidationError as e:
    #         print(traceback.print_exc())
    #         raise serializers.ValidationError(repr(e.error_dict))
    #     except Exception as e:
    #         print(traceback.print_exc())
    #         raise serializers.ValidationError(str(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = SaveSpeciesDocumentSerializer(instance, data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance.add_documents(request)
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


    def create(self, request, *args, **kwargs):
        try:
            serializer = SaveSpeciesDocumentSerializer(data= json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception = True)
            instance = serializer.save()
            instance.add_documents(request)
            return Response(serializer.data)
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


class CommunityDocumentViewSet(viewsets.ModelViewSet):
    queryset = CommunityDocument.objects.all().order_by('id')
    serializer_class = CommunityDocumentSerializer

    @detail_route(methods=['GET',], detail=True)
    def discard(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.visible = False
            instance.save()
            serializer = self.get_serializer(instance)
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
    def reinstate(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.visible = True
            instance.save()
            serializer = self.get_serializer(instance)
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

    # @detail_route(methods=['POST',], detail=True)
    # @renderer_classes((JSONRenderer,))
    # def delete_document(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #         RequirementDocument.objects.get(id=request.data.get('id')).delete()
    #         return Response([dict(id=i.id, name=i.name,_file=i._file.url) for i in instance.requirement_documents.all()])
    #     except serializers.ValidationError:
    #         print(traceback.print_exc())
    #         raise
    #     except ValidationError as e:
    #         print(traceback.print_exc())
    #         raise serializers.ValidationError(repr(e.error_dict))
    #     except Exception as e:
    #         print(traceback.print_exc())
    #         raise serializers.ValidationError(str(e))

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = SaveCommunityDocumentSerializer(instance, data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance.add_documents(request)
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


    def create(self, request, *args, **kwargs):
        try:
            serializer = SaveCommunityDocumentSerializer(data= json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception = True)
            instance = serializer.save()
            instance.add_documents(request)
            return Response(serializer.data)
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


class ThreatCategoryViewSet(viewsets.ModelViewSet):
    queryset = ThreatCategory.objects.all()

    def get_queryset(self):
        return ThreatCategory.objects.none()

    @list_route(methods=['GET', ], detail = False)
    def threat_category_choices(self, request, *args, **kwargs):
        res_obj = []
        for choice in ThreatCategory.objects.all():
            res_obj.append({'id': choice.id, 'name': choice.name})
        res_json = json.dumps(res_obj)
        return HttpResponse(res_json, content_type='application/json')


class CurrentImpactViewSet(viewsets.ModelViewSet):
    queryset = CurrentImpact.objects.all()

    def get_queryset(self):
        return CurrentImpact.objects.none()

    @list_route(methods=['GET', ], detail = False)
    def current_impact_choices(self, request, *args, **kwargs):
        res_obj = []
        for choice in CurrentImpact.objects.all():
            res_obj.append({'id': choice.id, 'name': choice.name})
        res_json = json.dumps(res_obj)
        return HttpResponse(res_json, content_type='application/json')


class PotentialImpactViewSet(viewsets.ModelViewSet):
    queryset = PotentialImpact.objects.all()

    def get_queryset(self):
        return PotentialImpact.objects.none()

    @list_route(methods=['GET', ], detail = False)    
    def potential_impact_choices(self, request, *args, **kwargs):
        res_obj = [] 
        for choice in PotentialImpact.objects.all():
            res_obj.append({'id': choice.id, 'name': choice.name})
        res_json = json.dumps(res_obj)
        return HttpResponse(res_json, content_type='application/json')


class PotentialThreatOnsetViewSet(viewsets.ModelViewSet):
    queryset = PotentialThreatOnset.objects.all()

    def get_queryset(self):
        return PotentialThreatOnset.objects.none()

    @list_route(methods=['GET', ], detail = False)
    def potential_threat_onset_choices(self, request, *args, **kwargs):
        res_obj = []
        for choice in PotentialThreatOnset.objects.all():
            res_obj.append({'id': choice.id, 'name': choice.name})
        res_json = json.dumps(res_obj)
        return HttpResponse(res_json, content_type='application/json')


class ConservationThreatViewSet(viewsets.ModelViewSet):
    queryset = ConservationThreat.objects.all().order_by('id')
    serializer_class = ConservationThreatSerializer

    @detail_route(methods=['GET',], detail=True)
    def discard(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.visible = False
            instance.save()
            serializer = self.get_serializer(instance)
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
    def reinstate(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.visible = True
            instance.save()
            serializer = self.get_serializer(instance)
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

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = SaveConservationThreatSerializer(instance, data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


    def create(self, request, *args, **kwargs):
        try:
            serializer = SaveConservationThreatSerializer(data= json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception = True)
            instance = serializer.save()
            return Response(serializer.data)
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