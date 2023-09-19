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

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
from django.db.models.query import QuerySet

from boranga.components.occurrence.models import( 
    OccurrenceReport,
    RockType,
    SoilType,
    SoilColour,
    SoilCondition,
    Drainage,
    HabitatComposition,
    HabitatCondition,
    LandForm,
    FireHistory,
    Intensity,
    AssociatedSpecies,
    ObservationMethod,
    ObservationDetail,
    PlantCountMethod,
    PlantCountAccuracy,
    PlantCondition,
    CountedSubject,
    PlantCount,
    AnimalObservation,
    PrimaryDetectionMethod,
    SecondarySign,
    ReproductiveMaturity,
    DeathReason,
    AnimalHealth,
    Identification,
    PermitType,
    IdentificationCertainty,
    SampleDestination,
    SampleType,
)
from boranga.components.occurrence.serializers import(
    ListOccurrenceReportSerializer,
    OccurrenceReportSerializer,
    SaveHabitatCompositionSerializer,
    SaveHabitatConditionSerializer,
    SaveFireHistorySerializer,
    SaveAssociatedSpeciesSerializer,
    SaveObservationDetailSerializer,
    SavePlantCountSerializer,
    SaveAnimalObservationSerializer,
    SaveIdentificationSerializer,
)

from boranga.components.main.utils import (
    check_db_connection,
    handle_validation_error,
)

import logging

logger = logging.getLogger(__name__)

class OccurrenceReportFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()

        flora = GroupType.GROUP_TYPE_FLORA
        fauna = GroupType.GROUP_TYPE_FAUNA
        community = GroupType.GROUP_TYPE_COMMUNITY
        
        filter_group_type = request.GET.get('filter_group_type')
        if filter_group_type and not filter_group_type.lower() == 'all':
            queryset = queryset.filter(group_type__name=filter_group_type)
        
        # filter_scientific_name is the species_id
        filter_scientific_name = request.GET.get('filter_scientific_name')
        if filter_scientific_name and not filter_scientific_name.lower() == 'all':
            queryset = queryset.filter(species=filter_scientific_name)

        # filter_community_name is the community_id
        filter_community_name = request.GET.get('filter_community_name')
        if filter_community_name and not filter_community_name.lower() == 'all':
            queryset = queryset.filter(community=filter_community_name)

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
            queryset = super(OccurrenceReportFilterBackend, self).filter_queryset(request, queryset, view)
        except Exception as e:
            print(e)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

class OccurrenceReportRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(OccurrenceReportRenderer, self).render(data, accepted_media_type, renderer_context)


class OccurrenceReportPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (OccurrenceReportFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (OccurrenceReportRenderer,)
    queryset = OccurrenceReport.objects.none()
    serializer_class = ListOccurrenceReportSerializer
    page_size = 10

    def get_queryset(self):
        request_user = self.request.user
        qs = OccurrenceReport.objects.all()

        if is_internal(self.request):
            qs = OccurrenceReport.objects.all()
        elif is_customer(self.request):
            #user_orgs = [org.id for org in request_user.mooringlicensing_organisations.all()]
            #qs = all.filter(Q(org_applicant_id__in=user_orgs) | Q(submitter=request_user) | Q(site_licensee_email=request_user.email))
            qs = qs.filter(Q(submitter=request_user.id))
            return qs

        return qs

    @list_route(methods=['GET',], detail=False)
    def occurrence_report_external(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = qs.filter(Q(internal_application=False))
        # TODO Not Sure but to filter for only WA listed conservation lists for external
        #qs = qs.filter(Q(conservation_list__applies_to_wa=True))
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListOccurrenceReportSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class OccurrenceReportViewSet(viewsets.ModelViewSet):
    queryset = OccurrenceReport.objects.none()
    serializer_class = OccurrenceReportSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request): #user.is_authenticated():
            qs= OccurrenceReport.objects.all()
            return qs
        elif is_customer(self.request):
            # user_orgs = [org.id for org in user.boranga_organisations.all()]
            queryset =  OccurrenceReport.objects.filter( Q(submitter = user.id) )
            return queryset
        logger.warn("User is neither customer nor internal user: {} <{}>".format(user.get_full_name(), user.email))
        return OccurrenceReport.objects.none()

    def get_serializer_class(self):
        try:
            return OccurrenceReportSerializer
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
        try:
            with transaction.atomic():
                group_type_id = GroupType.objects.get(id=request.data.get('group_type_id'))
                # internal_application = False
                # if request.data.get('internal_application'):
                #         internal_application = request.data.get('internal_application')
                new_instance = OccurrenceReport.objects.create(
                        submitter=request.user.id,
                        group_type=group_type_id,
                        # internal_application=internal_application
                        )
                data={
                    'occurrence_report_id': new_instance.id
                }
                
                # create HabitatComposition for new instance
                serializer=SaveHabitatCompositionSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # create HabitatCondition for new instance
                serializer=SaveHabitatConditionSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # create FireHistory for new instance
                serializer=SaveFireHistorySerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # create FireHistory for new instance
                serializer=SaveAssociatedSpeciesSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # create ObservationDetail for new instance
                serializer=SaveObservationDetailSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # create PlantCount for new instance
                serializer=SavePlantCountSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # create AnimalObservation for new instance
                serializer=SaveAnimalObservationSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                 # create Identification for new instance
                serializer=SaveIdentificationSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                headers = self.get_success_headers(serializer.data)
                return Response(
                    new_instance.id,
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
    
    #used for Occurrence Report external form 
    @list_route(methods=['GET',], detail=False)
    def list_of_values(self, request, *args, **kwargs):
        """ used for Occurrence Report external form  """
        qs =  self.get_queryset()
        land_form_list = []
        types = LandForm.objects.all()
        if types:
            for val in types:
                land_form_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        rock_type_list = []
        types = RockType.objects.all()
        if types:
            for val in types:
                rock_type_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        soil_type_list = []
        types = SoilType.objects.all()
        if types:
            for val in types:
                soil_type_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        soil_colour_list = []
        colours = SoilColour.objects.all()
        if colours:
            for val in colours:
                soil_colour_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        soil_condition_list = []
        conditions = SoilCondition.objects.all()
        if conditions:
            for val in conditions:
                soil_condition_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        drainage_list = []
        drainages = Drainage.objects.all()
        if drainages:
            for val in drainages:
                drainage_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        intensity_list = []
        intensities = Intensity.objects.all()
        if intensities:
            for val in intensities:
                intensity_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        res_json = {
        "land_form_list":land_form_list,
        "rock_type_list":rock_type_list,
        "soil_type_list": soil_type_list,
        "soil_colour_list": soil_colour_list,
        "soil_condition_list": soil_condition_list,
        "drainage_list":drainage_list,
        "intensity_list":intensity_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')
    
    #used for Occurrence Report Observation external form 
    @list_route(methods=['GET',], detail=False)
    def observation_list_of_values(self, request, *args, **kwargs):
        """ used for Occurrence Report external form  """
        qs =  self.get_queryset()
        observation_method_list = []
        values = ObservationMethod.objects.all()
        if values:
            for val in values:
                observation_method_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        plant_count_method_list = []
        values = PlantCountMethod.objects.all()
        if values:
            for val in values:
                plant_count_method_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        plant_count_accuracy_list = []
        values = PlantCountAccuracy.objects.all()
        if values:
            for val in values:
                plant_count_accuracy_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        plant_condition_list = []
        values = PlantCondition.objects.all()
        if values:
            for val in values:
                plant_condition_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        counted_subject_list = []
        values = CountedSubject.objects.all()
        if values:
            for val in values:
                counted_subject_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        primary_detection_method_list = []
        values = PrimaryDetectionMethod.objects.all()
        if values:
            for val in values:
                primary_detection_method_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        secondary_sign_list = []
        values = SecondarySign.objects.all()
        if values:
            for val in values:
                secondary_sign_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        reprod_maturity_list = []
        values = ReproductiveMaturity.objects.all()
        if values:
            for val in values:
                reprod_maturity_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        death_reason_list = []
        values = DeathReason.objects.all()
        if values:
            for val in values:
                death_reason_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        animal_health_list = []
        values = AnimalHealth.objects.all()
        if values:
            for val in values:
                animal_health_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        identification_certainty_list = []
        values = IdentificationCertainty.objects.all()
        if values:
            for val in values:
                identification_certainty_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        sample_type_list = []
        values = SampleType.objects.all()
        if values:
            for val in values:
                sample_type_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        sample_dest_list = []
        values = SampleDestination.objects.all()
        if values:
            for val in values:
                sample_dest_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        permit_type_list = []
        values = PermitType.objects.all()
        if values:
            for val in values:
                permit_type_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        res_json = {
        "observation_method_list":observation_method_list,
        "plant_count_method_list":plant_count_method_list,
        "plant_count_accuracy_list":plant_count_accuracy_list,
        "plant_condition_list":plant_condition_list,
        "counted_subject_list":counted_subject_list,
        "primary_detection_method_list":primary_detection_method_list,
        "secondary_sign_list":secondary_sign_list,
        "reprod_maturity_list":reprod_maturity_list,
        "death_reason_list":death_reason_list,
        "animal_health_list":animal_health_list,
        "identification_certainty_list":identification_certainty_list,
        "sample_type_list":sample_type_list,
        "sample_dest_list":sample_dest_list,
        "permit_type_list":permit_type_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')
    
    @list_route(methods=['POST',], detail=True)
    def update_habitat_composition_details(self, request, *args, **kwargs):
        try:
            ocr_instance = self.get_object()
            habitat_instance, created = HabitatComposition.objects.get_or_create(occurrence_report=ocr_instance)
            # the request.data is only the habitat composition data thats been sent from front end
            serializer = SaveHabitatCompositionSerializer(habitat_instance,data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
    
    @list_route(methods=['POST',], detail=True)
    def update_habitat_condition_details(self, request, *args, **kwargs):
        try:
            ocr_instance = self.get_object()
            habitat_instance, created = HabitatCondition.objects.get_or_create(occurrence_report=ocr_instance)
            # the request.data is only the habitat condition data thats been sent from front end
            serializer = SaveHabitatConditionSerializer(habitat_instance,data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
    
    @list_route(methods=['POST',], detail=True)
    def update_fire_history_details(self, request, *args, **kwargs):
        try:
            ocr_instance = self.get_object()
            fire_instance, created = FireHistory.objects.get_or_create(occurrence_report=ocr_instance)
            # the request.data is only the habitat composition data thats been sent from front end
            serializer = SaveFireHistorySerializer(fire_instance,data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
    
    @list_route(methods=['POST',], detail=True)
    def update_associated_species_details(self, request, *args, **kwargs):
        try:
            ocr_instance = self.get_object()
            assoc_species_instance, created = AssociatedSpecies.objects.get_or_create(occurrence_report=ocr_instance)
            # the request.data is only the habitat composition data thats been sent from front end
            serializer = SaveAssociatedSpeciesSerializer(assoc_species_instance,data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
    
    @list_route(methods=['POST',], detail=True)
    def update_observation_details(self, request, *args, **kwargs):
        try:
            ocr_instance = self.get_object()
            obs_det_instance, created = ObservationDetail.objects.get_or_create(occurrence_report=ocr_instance)
            # the request.data is only the observation detail data thats been sent from front end
            serializer = SaveObservationDetailSerializer(obs_det_instance,data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
    
    @list_route(methods=['POST',], detail=True)
    def update_plant_count_details(self, request, *args, **kwargs):
        try:
            ocr_instance = self.get_object()
            plant_count_instance, created = PlantCount.objects.get_or_create(occurrence_report=ocr_instance)
            # the request.data is only the plant count data thats been sent from front end
            serializer = SavePlantCountSerializer(plant_count_instance,data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
    
    @list_route(methods=['POST',], detail=True)
    def update_animal_observation_details(self, request, *args, **kwargs):
        try:
            ocr_instance = self.get_object()
            animal_obs_instance, created = AnimalObservation.objects.get_or_create(occurrence_report=ocr_instance)
            # the request.data is only the animal obs data thats been sent from front end
            serializer = SaveAnimalObservationSerializer(animal_obs_instance,data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
    
    @list_route(methods=['POST',], detail=True)
    def update_identification_details(self, request, *args, **kwargs):
        try:
            ocr_instance = self.get_object()
            identification_instance, created = Identification.objects.get_or_create(occurrence_report=ocr_instance)
            # the request.data is only the identification data thats been sent from front end
            serializer = SaveIdentificationSerializer(identification_instance,data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
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



