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
from datetime import datetime, time
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
from boranga.components.occurrence.utils import ocr_proposal_submit, validate_map_files
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from boranga.components.main.decorators import basic_exception_handler

from boranga.components.main.related_item import RelatedItemsSerializer

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO
from django.db.models.query import QuerySet
from django.contrib.gis.geos import GEOSGeometry

from boranga.components.occurrence.models import (
    Occurrence,
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
    Datum,
    CoordinationSource,
    LocationAccuracy,
    Location,
    ObserverDetail,
    OccurrenceReportDocument,
    OCRConservationThreat,
    OccurrenceReportUserAction,
)
from boranga.components.occurrence.serializers import (
    ListOccurrenceReportSerializer,
    ListOccurrenceSerializer,
    OccurrenceLogEntrySerializer,
    OccurrenceReportSerializer,
    OccurrenceSerializer,
    OccurrenceUserActionSerializer,
    SaveHabitatCompositionSerializer,
    SaveHabitatConditionSerializer,
    SaveFireHistorySerializer,
    SaveAssociatedSpeciesSerializer,
    SaveObservationDetailSerializer,
    SavePlantCountSerializer,
    SaveAnimalObservationSerializer,
    SaveIdentificationSerializer,
    SaveLocationSerializer,
    ObserverDetailSerializer,
    ListOCRReportMinimalSerializer,
    SaveOccurrenceReportSerializer,
    ListInternalOccurrenceReportSerializer,
    OccurrenceReportUserActionSerializer,
    OccurrenceReportLogEntrySerializer,
    OccurrenceReportDocumentSerializer,
    SaveOccurrenceReportDocumentSerializer,
    OCRConservationThreatSerializer,
    SaveOCRConservationThreatSerializer,
)

from boranga.components.occurrence.utils import (
    save_geometry,
    process_shapefile_document,
)

from boranga.components.main.utils import (
    check_db_connection,
    handle_validation_error,
)

import logging

logger = logging.getLogger(__name__)

class OccurrenceReportFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'internal' in view.name:
            total_count = queryset.count()

            filter_group_type = request.GET.get('filter_group_type')
            if filter_group_type and not filter_group_type.lower() == 'all':
                queryset = queryset.filter(group_type__name=filter_group_type)

            # To do - change group_type__name based on the relevant model
            # filter_occurrence = request.GET.get('filter_occurrence')
            # if filter_occurrence and not filter_occurrence.lower() == 'all':
            #     queryset = queryset.filter(group_type__name=filter_occurrence)

            filter_scientific_name = request.GET.get('filter_scientific_name')
            if filter_scientific_name and not filter_scientific_name.lower() == 'all':
                queryset = queryset.filter(species__taxonomy__id=filter_scientific_name)

            filter_status = request.GET.get('filter_status')
            if filter_status and not filter_status.lower() == 'all':
                queryset = queryset.filter(processing_status=filter_status)

            def get_date(filter_date):
                date = request.GET.get(filter_date)
                if date:
                    date = datetime.strptime(date,'%Y-%m-%d')
                return date

            filter_submitted_from_date = get_date('filter_submitted_from_date')
            filter_submitted_to_date = get_date('filter_submitted_to_date')
            if filter_submitted_to_date: 
                filter_submitted_to_date = datetime.combine(filter_submitted_to_date , time.max)

            if filter_submitted_from_date and not filter_submitted_to_date:
                queryset = queryset.filter(reported_date__gte=filter_submitted_from_date)

            if filter_submitted_from_date and filter_submitted_to_date:
                queryset = queryset.filter(reported_date__range=[filter_submitted_from_date, filter_submitted_to_date])

            if filter_submitted_to_date and not filter_submitted_from_date:
                queryset = queryset.filter(reported_date__lte=filter_submitted_to_date)

        if 'external' in view.name:
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

        fields = self.get_fields(request)
        ordering = self.get_ordering(request, view, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        try:
            queryset = super(OccurrenceReportFilterBackend, self).filter_queryset(request, queryset, view)
        except Exception as e:
            print(e)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

# class OccurrenceReportRenderer(DatatablesRenderer):
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
#             data['recordsTotal'] = renderer_context['view']._datatables_total_count
#         return super(OccurrenceReportRenderer, self).render(data, accepted_media_type, renderer_context)


class OccurrenceReportPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (OccurrenceReportFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    queryset = OccurrenceReport.objects.none()
    serializer_class = ListOccurrenceReportSerializer
    page_size = 10

    def get_queryset(self):
        qs = OccurrenceReport.objects.all()
        if is_customer(self.request):
            qs = qs.filter(submitter=self.request.user.id)

        return qs

    @list_route(methods=['GET',], detail=False)
    def occurrence_report_external(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = qs.filter(Q(internal_application=False))
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListOccurrenceReportSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    @list_route(methods=['GET',], detail=False)
    def occurrence_report_internal(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListInternalOccurrenceReportSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)
    
    @list_route(methods=['GET',], detail=False)
    def occurrence_report_external_export(self, request, *args, **kwargs):
        
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        export_format = request.GET.get('export_format')
        allowed_fields = ['group_type', 'scientific_name', 'community_name', 'customer_status', 'occurrence_report_number']

        serializer = ListOccurrenceReportSerializer(qs, context={'request': request}, many=True)
        serialized_data = serializer.data

        try:
            filtered_data = []
            for obj in serialized_data:
                filtered_obj = {key: value for key, value in obj.items() if key in allowed_fields}
                filtered_data.append(filtered_obj)

            def flatten_dict(d, parent_key='', sep='_'):
                flattened_dict = {}
                for k, v in d.items():
                    new_key = parent_key + sep + k if parent_key else k
                    if isinstance(v, dict):
                        flattened_dict.update(flatten_dict(v, new_key, sep))
                    else:
                        flattened_dict[new_key] = v
                return flattened_dict

            flattened_data = [flatten_dict(item) for item in filtered_data]
            df = pd.DataFrame(flattened_data)
            new_headings = ['Number', 'Type', 'Scientific Name', 'Community Name', 'Status']
            df.columns = new_headings
            column_order = ['Number', 'Type', 'Scientific Name', 'Community Name', 'Status']
            df = df[column_order]

            if export_format is not None:
                if export_format == "excel":
                    buffer = BytesIO()
                    workbook = Workbook()
                    sheet_name = 'Sheet1'
                    sheet = workbook.active
                    sheet.title = sheet_name

                    for row in dataframe_to_rows(df, index=False, header=True):
                        sheet.append(row)
                    for cell in sheet[1]:
                        cell.font = Font(bold=True)

                    workbook.save(buffer)
                    buffer.seek(0)
                    response = HttpResponse(buffer.read(), content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename=DBCA_ExternalOccurrenceReports.xlsx'
                    final_response = response
                    buffer.close()
                    return final_response
                
                elif export_format == "csv":
                    csv_data = df.to_csv(index=False)
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename=DBCA_ExternalOccurrenceReports.csv'
                    response.write(csv_data)
                    return response
                
                else:
                    return Response(status=400, data="Format not valid")
        except:
            return Response(status=500, data="Internal Server Error")
    
    @list_route(methods=['GET',], detail=False)
    def occurrence_report_internal_export(self, request, *args, **kwargs):
        
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        export_format = request.GET.get('export_format')
        allowed_fields = ['species', 'scientific_name', 'reported_date', 'submitter', 'processing_status', 'occurrence_report_number']

        serializer = ListInternalOccurrenceReportSerializer(qs, context={'request': request}, many=True)
        serialized_data = serializer.data

        try:
            filtered_data = []
            for obj in serialized_data:
                filtered_obj = {key: value for key, value in obj.items() if key in allowed_fields}
                filtered_data.append(filtered_obj)

            def flatten_dict(d, parent_key='', sep='_'):
                flattened_dict = {}
                for k, v in d.items():
                    new_key = parent_key + sep + k if parent_key else k
                    if isinstance(v, dict):
                        flattened_dict.update(flatten_dict(v, new_key, sep))
                    else:
                        flattened_dict[new_key] = v
                return flattened_dict

            flattened_data = [flatten_dict(item) for item in filtered_data]
            df = pd.DataFrame(flattened_data)
            new_headings = ['Number', 'Occurrence', 'Scientific Name', 'Submission date/time', 'Submitter',  'Processing Status']
            df.columns = new_headings
            column_order = ['Number', 'Occurrence', 'Scientific Name', 'Submission date/time', 'Submitter',  'Processing Status']
            df = df[column_order]

            if export_format is not None:
                if export_format == "excel":
                    buffer = BytesIO()
                    workbook = Workbook()
                    sheet_name = 'Sheet1'
                    sheet = workbook.active
                    sheet.title = sheet_name

                    for row in dataframe_to_rows(df, index=False, header=True):
                        sheet.append(row)
                    for cell in sheet[1]:
                        cell.font = Font(bold=True)

                    workbook.save(buffer)
                    buffer.seek(0)
                    response = HttpResponse(buffer.read(), content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = 'attachment; filename=DBCA_OccurrenceReport_Species.xlsx'
                    final_response = response
                    buffer.close()
                    return final_response
                
                elif export_format == "csv":
                    csv_data = df.to_csv(index=False)
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename=DBCA_OccurrenceReport_Species.csv'
                    response.write(csv_data)
                    return response
                
                else:
                    return Response(status=400, data="Format not valid")
        except:
            return Response(status=500, data="Internal Server Error")

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
            qs =  OccurrenceReport.objects.filter( Q(submitter = user.id) )
            return qs
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

                # create Locatiob for new instance
                serializer=SaveLocationSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
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
    
    #used for Location Tab of Occurrence Report external form 
    @list_route(methods=['GET',], detail=False)
    def location_list_of_values(self, request, *args, **kwargs):
        """ used for Occurrence Report external form  """
        qs =  self.get_queryset()
        datum_list = []
        values = Datum.objects.all()
        if values:
            for val in values:
                datum_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        coordination_source_list = []
        values = CoordinationSource.objects.all()
        if values:
            for val in values:
                coordination_source_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        location_accuracy_list = []
        values = LocationAccuracy.objects.all()
        if values:
            for val in values:
                location_accuracy_list.append({
                    'id': val.id,
                    'name':val.name,
                    });
        res_json = {
        "datum_list":datum_list,
        "coordination_source_list":coordination_source_list,
        "location_accuracy_list": location_accuracy_list,
        }
        res_json = json.dumps(res_json)
        return HttpResponse(res_json, content_type='application/json')
    
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
    def update_location_details(self, request, *args, **kwargs):
        try:
            ocr_instance = self.get_object()

            location_instance, created = Location.objects.get_or_create(occurrence_report=ocr_instance)
            # species_id saved seperately as its not field of Location but OCR
            species = request.data.get('species_id')
            ocr_instance.species_id = species
            ocr_instance.save()
            # community_id saved seperately as its not field of Location but OCR
            community = request.data.get('community_id')
            ocr_instance.community_id = community
            ocr_instance.save()

            # ocr geometry data to save seperately
            geometry_data = request.data.get('ocr_geometry')
            if geometry_data:
                  save_geometry(request, ocr_instance, geometry_data)
                 
            # print(request.data.get('geojson_polygon'))
            # polygon = request.data.get('geojson_polygon')
            # if polygon:
            #     coords_list = [list(map(float, coord.split(' '))) for coord in polygon.split(',')]
            #     coords_list.append(coords_list[0])
            #     request.data['geojson_polygon'] = GEOSGeometry(f'POLYGON(({", ".join(map(lambda x: " ".join(map(str, x)), coords_list))}))')

            # the request.data is only the habitat composition data thats been sent from front end
            location_data = request.data.get('location')
            serializer = SaveLocationSerializer(location_instance,data=location_data, context={'request':request})
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
    
    # used for observer detail datatable on location tab
    @detail_route(methods=['GET',], detail=True)
    def observer_details(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.observer_detail.all()
            serializer = ObserverDetailSerializer(qs,many=True, context={'request':request})
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
    
    @list_route(methods=["GET"], detail=False)
    def list_for_map(self, request, *args, **kwargs):
        """Returns the proposals for the map"""
        proposal_ids = [
            int(id)
            for id in request.query_params.get("proposal_ids", "").split(",")
            if id.lstrip("-").isnumeric()
        ]
        # application_type = request.query_params.get("application_type", None)
        # processing_status = request.query_params.get("processing_status", None)

        # cache_key = settings.CACHE_KEY_MAP_PROPOSALS
        # qs = cache.get(cache_key)
        # priya added qs=None as we don't have cache data yet
        qs = None
        if qs is None:
            qs = (
                self.get_queryset()
                .exclude(ocr_geometry__isnull=True)
                .prefetch_related("ocr_geometry")
            )
            # cache.set(cache_key, qs, settings.CACHE_TIMEOUT_2_HOURS)

        if len(proposal_ids) > 0:
            qs = qs.filter(id__in=proposal_ids)

        # if (
        #     application_type
        #     and application_type.isnumeric()
        #     and int(application_type) > 0
        # ):
        #     qs = qs.filter(application_type_id=application_type)

        # if processing_status:
        #     qs = qs.filter(processing_status=processing_status)

        # qs = self.filter_queryset(qs)
        serializer = ListOCRReportMinimalSerializer(
            qs, context={"request": request}, many=True
        )
        return Response(serializer.data)
    
    @detail_route(methods=['post'], detail=True)
    @renderer_classes((JSONRenderer,))
    def draft(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                # request_data = request.data
                proposal_data = request.data.get("proposal") if request.data.get("proposal") else {}
                #request.data['submitter'] = u'{}'.format(request.user.id)
                if proposal_data['submitter']:
                    request.data.get("proposal")['submitter'] = u'{}'.format(proposal_data['submitter'].get('id'))
                if(proposal_data.get('habitat_composition')):
                    habitat_instance, created = HabitatComposition.objects.get_or_create(occurrence_report=instance)
                    serializer = SaveHabitatCompositionSerializer(habitat_instance, data = proposal_data.get('habitat_composition'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()
                
                if(proposal_data.get('habitat_condition')):
                    hab_cond_instance, created = HabitatCondition.objects.get_or_create(occurrence_report=instance)
                    serializer = SaveHabitatConditionSerializer(hab_cond_instance, data = proposal_data.get('habitat_condition'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()
                
                if(proposal_data.get('fire_history')):
                    fire_instance, created = FireHistory.objects.get_or_create(occurrence_report=instance)
                    serializer = SaveFireHistorySerializer(fire_instance, data = proposal_data.get('fire_history'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()
                
                if(proposal_data.get('associated_species')):
                    assoc_species_instance, created = AssociatedSpecies.objects.get_or_create(occurrence_report=instance)
                    serializer = SaveAssociatedSpeciesSerializer(assoc_species_instance, data = proposal_data.get('associated_species'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()
                
                if(proposal_data.get('observation_detail')):
                    obs_det_instance, created = ObservationDetail.objects.get_or_create(occurrence_report=instance)
                    serializer = SaveObservationDetailSerializer(obs_det_instance, data = proposal_data.get('observation_detail'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()
                
                if(proposal_data.get('plant_count')):
                    plant_count_instance, created = PlantCount.objects.get_or_create(occurrence_report=instance)
                    serializer = SavePlantCountSerializer(plant_count_instance, data = proposal_data.get('plant_count'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()
                
                if(proposal_data.get('animal_observation')):
                    animal_obs_instance, created = AnimalObservation.objects.get_or_create(occurrence_report=instance)
                    serializer = SaveAnimalObservationSerializer(animal_obs_instance, data = proposal_data.get('animal_observation'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()
                
                if(proposal_data.get('identification')):
                    identification_instance, created = Identification.objects.get_or_create(occurrence_report=instance)
                    serializer = SaveIdentificationSerializer(identification_instance, data = proposal_data.get('identification'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()
                
                if(proposal_data.get('location')):
                    location_instance, created = Location.objects.get_or_create(occurrence_report=instance)
                    serializer = SaveLocationSerializer(location_instance, data = proposal_data.get('location'))
                    serializer.is_valid(raise_exception=True)
                    if serializer.is_valid():
                        serializer.save()
                
                # ocr geometry data to save seperately
                geometry_data = proposal_data.get("ocr_geometry", None)
                if geometry_data:
                    save_geometry(request, instance, geometry_data)

                serializer=SaveOccurrenceReportSerializer(instance, data = proposal_data, partial=True)

                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    saved_instance = serializer.save()

            # return redirect(reverse('external'))
            serializer = self.get_serializer(saved_instance)
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
    
    @detail_route(methods=['post'], detail=True)
    @renderer_classes((JSONRenderer,))
    def submit(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            #instance.submit(request,self)
            ocr_proposal_submit(instance, request)
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
    
    @detail_route(methods=['GET',], detail=True)
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = OccurrenceReportUserActionSerializer(qs,many=True)
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
            serializer = OccurrenceReportLogEntrySerializer(qs,many=True)
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
                request.data['occurrence_report'] = u'{}'.format(instance.id)
                request.data['staff'] = u'{}'.format(request.user.id)
                request.data._mutable=mutable
                serializer = OccurrenceReportLogEntrySerializer(data=request.data)
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
    def documents(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # qs = instance.documents.all()
            if is_internal(self.request):
                qs = instance.documents.all()
            elif is_customer(self.request):
                qs = instance.documents.filter(Q(uploaded_by=request.user.id))
            # qs = qs.exclude(input_name='occurrence_report_approval_doc') # TODO do we need/not to show approval doc in cs documents tab
            qs = qs.order_by('-uploaded_date')
            serializer = OccurrenceReportDocumentSerializer(qs,many=True, context={'request':request})
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
            # qs = instance.ocr_threats.all()
            if is_internal(self.request):
                qs = instance.ocr_threats.all()
            elif is_customer(self.request):
                # TODO Do we need to sort the threats for external user (similar like documents)
                # qs = qs.filter(Q(uploaded_by=request.user.id))
                qs = instance.ocr_threats.all()
            qs = qs.order_by('-date_observed')
            serializer = OCRConservationThreatSerializer(qs,many=True, context={'request':request})
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

    @detail_route(methods=["POST"], detail=True)
    @renderer_classes((JSONRenderer,))
    @basic_exception_handler
    def process_shapefile_document(self, request, *args, **kwargs):
        instance = self.get_object()
        returned_data = None
        returned_data = process_shapefile_document(
            request, instance
        )
        if returned_data:
            return Response(returned_data)
        else:
            return Response({})

    @detail_route(methods=["POST"], detail=True)
    @renderer_classes((JSONRenderer,))
    @basic_exception_handler
    def validate_map_files(self, request, *args, **kwargs):
        instance = self.get_object()
        validate_map_files(request, instance, "occurrence_report")
        instance.save()
        serializer = self.get_serializer(instance)
        logger.debug(f"validate_map_files response: {serializer.data}")
        return Response(serializer.data)


class ObserverDetailViewSet(viewsets.ModelViewSet):
    # queryset = ObserverDetail.objects.all().order_by('id')
    queryset = ObserverDetail.objects.none()
    serializer_class = ObserverDetailSerializer

    def get_queryset(self):
        request_user = self.request.user
        qs = ObserverDetail.objects.none()

        if is_internal(self.request):
            qs = ObserverDetail.objects.all().order_by('id')
        elif is_customer(self.request):
            # not sure what qs it should be for api security check
            qs = ObserverDetail.objects.all().order_by('id')
            return qs
        return qs

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ObserverDetailSerializer(instance, data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # instance.community.log_user_action(CommunityUserAction.ACTION_ADD_THREAT.format(instance.threat_number,instance.community.community_number),request)
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


    def create(self, request, *args, **kwargs):
        try:
            serializer = ObserverDetailSerializer(data= json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception = True)
            instance = serializer.save()
            # instance.community.log_user_action(CommunityUserAction.ACTION_ADD_THREAT.format(instance.threat_number,instance.community.community_number),request)
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


class OccurrenceReportDocumentViewSet(viewsets.ModelViewSet):
    queryset = OccurrenceReportDocument.objects.none()
    serializer_class = OccurrenceReportDocumentSerializer

    def get_queryset(self):
        request_user = self.request.user
        qs = OccurrenceReportDocument.objects.none()

        if is_internal(self.request):
            qs = OccurrenceReportDocument.objects.all().order_by('id')
        elif is_customer(self.request):
            qs = OccurrenceReportDocument.objects.filter(Q(uploaded_by=request_user.id))
            return qs
        return qs

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
            with transaction.atomic():
                instance = self.get_object()
                serializer = SaveOccurrenceReportDocumentSerializer(instance, data=json.loads(request.data.get('data')))
                serializer.is_valid(raise_exception=True)
                serializer.save()
                instance.add_documents(request)
                instance.uploaded_by = request.user.id
                instance.save()
                return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = SaveOccurrenceReportDocumentSerializer(data= json.loads(request.data.get('data')))
                serializer.is_valid(raise_exception = True)
                instance = serializer.save()
                instance.add_documents(request)
                instance.uploaded_by = request.user.id
                instance.save()
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


class OCRConservationThreatViewSet(viewsets.ModelViewSet):
    queryset = OCRConservationThreat.objects.none()
    serializer_class = OCRConservationThreatSerializer

    def get_queryset(self):
        request_user = self.request.user
        qs = OCRConservationThreat.objects.none()

        if is_internal(self.request):
            qs = OCRConservationThreat.objects.all().order_by('id')
        elif is_customer(self.request):
            # TODO filter qs as per added_by
            qs = OCRConservationThreat.objects.all().order_by('id')
            return qs
        return qs

    @detail_route(methods=['GET',], detail=True)
    def discard(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.visible = False
            instance.save()
            if instance.occurrence_report:
                instance.occurrence_report.log_user_action(OccurrenceReportUserAction.ACTION_DISCARD_THREAT.format(instance.threat_number,instance.occurrence_report.occurrence_report_number),request)
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
            if instance.occurrence_report:
                instance.occurrence_report.log_user_action(OccurrenceReportUserAction.ACTION_REINSTATE_THREAT.format(instance.threat_number,instance.occurrence_report.occurrence_report_number),request)
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
            with transaction.atomic():
                instance = self.get_object()
                serializer = SaveOCRConservationThreatSerializer(instance, data=json.loads(request.data.get('data')))
                serializer.is_valid(raise_exception=True)
                serializer.save()
                if instance.occurrence_report:
                    instance.occurrence_report.log_user_action(OccurrenceReportUserAction.ACTION_UPDATE_THREAT.format(instance.threat_number,instance.occurrence_report.occurrence_report_number),request)
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = SaveOCRConservationThreatSerializer(data= json.loads(request.data.get('data')))
                serializer.is_valid(raise_exception = True)
                instance = serializer.save()
                if instance.occurrence_report:
                    instance.occurrence_report.log_user_action(OccurrenceReportUserAction.ACTION_ADD_THREAT.format(instance.threat_number,instance.occurrence_report.occurrence_report_number),request)
                serializer = self.get_serializer(instance)
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


class OccurrenceFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        logger.debug(f"OccurrenceFilterBackend:filter_queryset: {view.name}")

        total_count = queryset.count()

        if view.name and "internal" in view.name:

            filter_group_type = request.GET.get("filter_group_type")
            if filter_group_type and not filter_group_type.lower() == "all":
                queryset = queryset.filter(group_type__name=filter_group_type)

            filter_scientific_name = request.GET.get("filter_scientific_name")
            if filter_scientific_name and not filter_scientific_name.lower() == "all":
                queryset = queryset.filter(species__taxonomy__id=filter_scientific_name)

            filter_status = request.GET.get("filter_status")
            if filter_status and not filter_status.lower() == "all":
                queryset = queryset.filter(processing_status=filter_status)

            def get_date(filter_date):
                date = request.GET.get(filter_date)
                if date:
                    date = datetime.strptime(date, "%Y-%m-%d")
                return date

            filter_submitted_from_date = get_date("filter_submitted_from_date")
            filter_submitted_to_date = get_date("filter_submitted_to_date")
            if filter_submitted_to_date:
                filter_submitted_to_date = datetime.combine(
                    filter_submitted_to_date, time.max
                )

            if filter_submitted_from_date and not filter_submitted_to_date:
                queryset = queryset.filter(
                    reported_date__gte=filter_submitted_from_date
                )

            if filter_submitted_from_date and filter_submitted_to_date:
                queryset = queryset.filter(
                    reported_date__range=[
                        filter_submitted_from_date,
                        filter_submitted_to_date,
                    ]
                )

            if filter_submitted_to_date and not filter_submitted_from_date:
                queryset = queryset.filter(reported_date__lte=filter_submitted_to_date)

        if view.name and "external" in view.name:
            filter_group_type = request.GET.get("filter_group_type")
            if filter_group_type and not filter_group_type.lower() == "all":
                queryset = queryset.filter(group_type__name=filter_group_type)

            # filter_scientific_name is the species_id
            filter_scientific_name = request.GET.get("filter_scientific_name")
            if filter_scientific_name and not filter_scientific_name.lower() == "all":
                queryset = queryset.filter(species=filter_scientific_name)

            # filter_community_name is the community_id
            filter_community_name = request.GET.get("filter_community_name")
            if filter_community_name and not filter_community_name.lower() == "all":
                queryset = queryset.filter(community=filter_community_name)

            filter_application_status = request.GET.get("filter_application_status")
            if (
                filter_application_status
                and not filter_application_status.lower() == "all"
            ):
                queryset = queryset.filter(customer_status=filter_application_status)

        fields = self.get_fields(request)
        ordering = self.get_ordering(request, view, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        try:
            queryset = super(OccurrenceReportFilterBackend, self).filter_queryset(
                request, queryset, view
            )
        except Exception as e:
            print(e)
        setattr(view, "_datatables_total_count", total_count)
        return queryset


class OccurrencePaginatedViewSet(viewsets.ModelViewSet):
    pagination_class = DatatablesPageNumberPagination
    queryset = Occurrence.objects.none()
    serializer_class = OccurrenceSerializer
    page_size = 10
    filter_backends = (OccurrenceFilterBackend,)

    def get_serializer_class(self):
        if self.action == "list":
            return ListOccurrenceSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = Occurrence.objects.all()
        if is_customer(self.request):
            qs = qs.filter(submitter=self.request.user.id)
        return qs

    @list_route(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def occurrence_external(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = qs.filter(Q(internal_application=False))
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListOccurrenceSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)

    @list_route(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def occurrence_internal(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        self.paginator.page_size = qs.count()
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListOccurrenceSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)

    @list_route(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def occurrence_internal_export(self, request, *args, **kwargs):

        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        export_format = request.GET.get("export_format")
        allowed_fields = [
            "species",
            "scientific_name",
            "reported_date",
            "submitter",
            "processing_status",
            "occurrence_report_number",
        ]

        serializer = ListInternalOccurrenceReportSerializer(
            qs, context={"request": request}, many=True
        )
        serialized_data = serializer.data

        try:
            filtered_data = []
            for obj in serialized_data:
                filtered_obj = {
                    key: value for key, value in obj.items() if key in allowed_fields
                }
                filtered_data.append(filtered_obj)

            def flatten_dict(d, parent_key="", sep="_"):
                flattened_dict = {}
                for k, v in d.items():
                    new_key = parent_key + sep + k if parent_key else k
                    if isinstance(v, dict):
                        flattened_dict.update(flatten_dict(v, new_key, sep))
                    else:
                        flattened_dict[new_key] = v
                return flattened_dict

            flattened_data = [flatten_dict(item) for item in filtered_data]
            df = pd.DataFrame(flattened_data)
            new_headings = [
                "Number",
                "Occurrence",
                "Scientific Name",
                "Submission date/time",
                "Submitter",
                "Processing Status",
            ]
            df.columns = new_headings
            column_order = [
                "Number",
                "Occurrence",
                "Scientific Name",
                "Submission date/time",
                "Submitter",
                "Processing Status",
            ]
            df = df[column_order]

            if export_format is not None:
                if export_format == "excel":
                    buffer = BytesIO()
                    workbook = Workbook()
                    sheet_name = "Sheet1"
                    sheet = workbook.active
                    sheet.title = sheet_name

                    for row in dataframe_to_rows(df, index=False, header=True):
                        sheet.append(row)
                    for cell in sheet[1]:
                        cell.font = Font(bold=True)

                    workbook.save(buffer)
                    buffer.seek(0)
                    response = HttpResponse(
                        buffer.read(), content_type="application/vnd.ms-excel"
                    )
                    response["Content-Disposition"] = (
                        "attachment; filename=DBCA_OccurrenceReport_Species.xlsx"
                    )
                    final_response = response
                    buffer.close()
                    return final_response

                elif export_format == "csv":
                    csv_data = df.to_csv(index=False)
                    response = HttpResponse(content_type="text/csv")
                    response["Content-Disposition"] = (
                        "attachment; filename=DBCA_OccurrenceReport_Species.csv"
                    )
                    response.write(csv_data)
                    return response

                else:
                    return Response(status=400, data="Format not valid")
        except:
            return Response(status=500, data="Internal Server Error")

    @detail_route(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = OccurrenceUserActionSerializer(qs, many=True)
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

    @detail_route(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = OccurrenceLogEntrySerializer(qs, many=True)
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

    @detail_route(
        methods=[
            "POST",
        ],
        detail=True,
    )
    @renderer_classes((JSONRenderer,))
    def add_comms_log(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                mutable = request.data._mutable
                request.data._mutable = True
                request.data["conservation_status"] = "{}".format(instance.id)
                request.data["staff"] = "{}".format(request.user.id)
                request.data._mutable = mutable
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
