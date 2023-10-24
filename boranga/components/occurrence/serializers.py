import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.species_and_communities.models import(
    GroupType,
    Species,
    Community,
    Taxonomy,
    CommunityTaxonomy
    )
from boranga.components.occurrence.models import(
    OccurrenceReport,
    HabitatComposition,
    HabitatCondition,
    LandForm,
    FireHistory,
    AssociatedSpecies,
    ObservationDetail,
    PlantCount,
    PrimaryDetectionMethod,
    AnimalObservation,
    SecondarySign,
    ReproductiveMaturity,
    Identification,
    Location,
    ObserverDetail,
    OccurrenceReportGeometry,
    )

from boranga.components.users.serializers import UserSerializer
from boranga.components.users.serializers import UserAddressSerializer, DocumentSerializer
from boranga.components.main.serializers import(
    CommunicationLogEntrySerializer,
    EmailUserSerializer,
    )
from boranga.ledger_api_utils import retrieve_email_user
from rest_framework import serializers
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from rest_framework_gis.serializers import GeoFeatureModelSerializer

logger = logging.getLogger('boranga')

class ListOccurrenceReportSerializer(serializers.ModelSerializer):
    group_type = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    customer_status = serializers.CharField(source='get_customer_status_display')
    class Meta:
        model = OccurrenceReport
        fields = (
                'id',
                'occurrence_report_number',
                'group_type',
                'scientific_name',
                'community_name',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )
        datatables_always_serialize = (
                'id',
                'occurrence_report_number',
                'group_type',
                'scientific_name',
                'community_name',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )   

    def get_group_type(self,obj):
        if obj.group_type:
            return obj.group_type.get_name_display()
        return ''

    def get_scientific_name(self,obj):
        if obj.species:
            if obj.species.taxonomy:
                return obj.species.taxonomy.scientific_name
        return ''

    def get_community_name(self,obj):
        if obj.community:
            try:
                taxonomy = CommunityTaxonomy.objects.get(community = obj.community)
                return taxonomy.community_name
            except CommunityTaxonomy.DoesNotExist:
                return ''
        return ''


class HabitatCompositionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HabitatComposition
        fields = (
			'id',
			'occurrence_report_id',
            'land_form',
			'rock_type_id',
			'loose_rock_percent',
			'soil_type_id',
			'soil_colour_id',
            'soil_condition_id',
            'drainage_id',
            'water_quality',
            'habitat_notes',
			)
    
    def __init__(self, *args, **kwargs):
        super(HabitatCompositionSerializer, self).__init__(*args, **kwargs)
        self.fields['land_form'] = serializers.MultipleChoiceField(choices=[(land_form_instance.id, land_form_instance.name) for land_form_instance in LandForm.objects.all()], allow_blank=False)


class HabitatConditionSerializer(serializers.ModelSerializer):

	class Meta:
		model = HabitatCondition
		fields = (
			'id',
			'occurrence_report_id',
            'pristine',
            'excellent',
            'very_good',
            'good',
            'degraded',
            'completely_degraded',
			)

class FireHistorySerializer(serializers.ModelSerializer):
    last_fire_estimate = serializers.DateField(format="%Y-%m")
    
    class Meta:
        model = FireHistory
        fields = (
			'id',
			'occurrence_report_id',
            'last_fire_estimate',
            'intensity_id',
            'comment',
            )

class AssociatedSpeciesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AssociatedSpecies
        fields = (
			'id',
			'occurrence_report_id',
            'related_species',
            )

class ObservationDetailSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = ObservationDetail
        fields = (
            'id',
			'occurrence_report_id',
            'observation_method_id',
            'area_surveyed',
            'survey_duration',
            )


class PlantCountSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = PlantCount
        fields = (
            'id',
			'occurrence_report_id',
            'plant_count_method_id',
            'plant_count_accuracy_id',
            'counted_subject_id',
            'plant_condition_id',
            'estimated_population_area',
            'quadrats_present',
            'quadrats_data_attached',
            'quadrats_surveyed',
            'individual_quadrat_area',
            'total_quadrat_area',
            'flowering_plants_per',
            'clonal_reproduction_present',
            'vegetative_state_present',
            'flower_bud_present',
            'flower_present',
            'immature_fruit_present',
            'ripe_fruit_present',
            'dehisced_fruit_present',
            'pollinator_observation',
            'comment',
            'simple_alive',
            'simple_dead',
            'detailed_alive_mature',
            'detailed_dead_mature',
            'detailed_alive_juvenile',
            'detailed_dead_juvenile',
            'detailed_alive_seedling',
            'detailed_dead_seedling',
            'detailed_alive_unknown',
            'detailed_dead_unknown',
            )


class AnimalObservationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AnimalObservation
        fields = (
            'id',
            'occurrence_report_id',
            'primary_detection_method',
            'secondary_sign',
            'reproductive_maturity',
            'animal_health_id',
            'death_reason_id',
            'total_count',
            'distinctive_feature',
            'action_taken',
            'action_required',
            'observation_detail_comment',
            'alive_adult',
            'dead_adult',
            'alive_juvenile',
            'dead_juvenile',
            'alive_pouch_young',
            'dead_pouch_young',
            'alive_unsure',
            'dead_unsure',
            )

    def __init__(self, *args, **kwargs):
        super(AnimalObservationSerializer, self).__init__(*args, **kwargs)
        self.fields['primary_detection_method'] = serializers.MultipleChoiceField(choices=[(primary_det_instance.id, primary_det_instance.name) for primary_det_instance in PrimaryDetectionMethod.objects.all()], allow_blank=False)
        self.fields['secondary_sign'] = serializers.MultipleChoiceField(choices=[(sec_sign_instance.id, sec_sign_instance.name) for sec_sign_instance in SecondarySign.objects.all()], allow_blank=False)
        self.fields['reproductive_maturity'] = serializers.MultipleChoiceField(choices=[(rep_maturity_instance.id, rep_maturity_instance.name) for rep_maturity_instance in ReproductiveMaturity.objects.all()], allow_blank=False)
    

class IdentificationSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = Identification
        fields = (
            'id',
			'occurrence_report_id',
            'id_confirmed_by',
            'identification_certainty_id',
            'sample_type_id',
            'sample_destination_id',
            'permit_type_id',
            'permit_id',
            'collector_number',
            'barcode_number',
            'identification_comment',
            )

class LocationSerializer(serializers.ModelSerializer):
    observation_date= serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # geojson_point = serializers.SerializerMethodField()
    # geojson_polygon = serializers.SerializerMethodField()
	
    class Meta:
        model = Location
        fields = (
            'id',
			'occurrence_report_id',
            'observation_date',
            'location_description',
            'boundary_description',
            'new_occurrence',
            'boundary',
            'mapped_boundary',
            'buffer_radius',
            'datum_id',
            'coordination_source_id',
            'location_accuracy_id',
            # 'geojson_point',
            # 'geojson_polygon',
            )
    
    # def get_geojson_point(self,obj):
    #     if(obj.geojson_point):
    #         coordinates = GEOSGeometry(obj.geojson_point).coords
    #         return coordinates
    #     else:
    #         return None
        
    # def get_geojson_polygon(self,obj):
    #     if(obj.geojson_polygon):
    #         coordinates = GEOSGeometry(obj.geojson_polygon).coords
    #         return coordinates
    #     else:
    #         return None

class OccurrenceReportGeometrySerializer(GeoFeatureModelSerializer):
    occurrence_report_id = serializers.IntegerField(write_only=True, required=False)
    polygon_source = serializers.SerializerMethodField()
    report_copied_from = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OccurrenceReportGeometry
        geo_field = "polygon"
        fields = (
            "id",
            "occurrence_report_id",
            "polygon",
            # "area_sqm",
            # "area_sqhm",
            "intersects",
            "polygon_source",
            "locked",
            "report_copied_from",
        )
        read_only_fields = ("id",)

    def get_polygon_source(self, obj):
        # return get_polygon_source(obj)
        return ''

    def get_report_copied_from(self, obj):
        if obj.copied_from:
            return ListOCRReportMinimalSerializer(
                obj.copied_from.occurrence_report, context=self.context
            ).data

        return None


class ListOCRReportMinimalSerializer(serializers.ModelSerializer):
    ocr_geometry = OccurrenceReportGeometrySerializer(many=True, read_only=True)
    processing_status_display = serializers.CharField(
        read_only=True, source="get_processing_status_display"
    )
    lodgement_date_display = serializers.DateTimeField(
        read_only=True, format="%d/%m/%Y", source="lodgement_date"
    )
    details_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OccurrenceReport
        fields = (
            "id",
            "processing_status",
            "processing_status_display",
            "ocr_geometry",
            "lodgement_date",
            "lodgement_date_display",
            "details_url",
        )

    def get_details_url(self, obj):
        # request = self.context["request"]
        # if request.user.is_authenticated:
        #     if is_internal(request):
        #         return reverse("internal-proposal-detail", kwargs={"pk": obj.id})
        #     else:
        #         return reverse(
        #             "external-proposal-detail", kwargs={"proposal_pk": obj.id}
        #         )
        return ''


class BaseOccurrenceReportSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    group_type = serializers.SerializerMethodField(read_only=True)
    # group_type_id = serializers.SerializerMethodField(read_only=True)
    allowed_assessors = EmailUserSerializer(many=True)
    # list_approval_level = serializers.SerializerMethodField(read_only=True)
    location = serializers.SerializerMethodField()
    habitat_composition = serializers.SerializerMethodField()
    habitat_condition = serializers.SerializerMethodField()
    fire_history = serializers.SerializerMethodField()
    associated_species = serializers.SerializerMethodField()
    observation_detail = serializers.SerializerMethodField()
    plant_count = serializers.SerializerMethodField()
    animal_observation = serializers.SerializerMethodField()
    identification = serializers.SerializerMethodField()
    ocr_geometry = OccurrenceReportGeometrySerializer(many=True, read_only=True)

    class Meta:
        model = OccurrenceReport
        fields = (
                'id',
                'group_type',
                'group_type_id',
                'species_id',
                'community_id',
                'occurrence_report_number',
                'reported_date',
                'lodgement_date',
                'applicant_type',
                'applicant',
                'submitter',
                # 'assigned_officer',
                'customer_status',
                'processing_status',
                'review_status',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'reference',
                'applicant_details',
                # 'assigned_approver',
                'allowed_assessors',
                'deficiency_data',
                'assessor_data',
                # 'list_approval_level',
                'location',
                'habitat_composition',
                'habitat_condition',
                'fire_history',
                'associated_species',
                'observation_detail',
                'plant_count',
                'animal_observation',
                'identification',
                'ocr_geometry',
                )

    def get_readonly(self,obj):
        return False
    
    def get_group_type(self,obj):
        return obj.group_type.name
    
    def get_processing_status(self,obj):
        return obj.get_processing_status_display()

    def get_review_status(self,obj):
        return obj.get_review_status_display()

    def get_customer_status(self,obj):
        return obj.get_customer_status_display()
    
    # def get_list_approval_level(self,obj):
    #     if obj.conservation_list:
    #         return obj.conservation_list.approval_level
    #     else:
    #         return None

    def get_location(self,obj):
        try:
            qs = Location.objects.get(occurrence_report=obj)
            return LocationSerializer(qs).data
        except Location.DoesNotExist:
            return LocationSerializer().data

    def get_habitat_composition(self,obj):
        try:
            qs = HabitatComposition.objects.get(occurrence_report=obj)
            return HabitatCompositionSerializer(qs).data
        except HabitatComposition.DoesNotExist:
            return HabitatCompositionSerializer().data
    
    def get_habitat_condition(self,obj):
        try:
            qs = HabitatCondition.objects.get(occurrence_report=obj)
            return HabitatConditionSerializer(qs).data
        except HabitatCondition.DoesNotExist:
            return HabitatConditionSerializer().data
    
    def get_fire_history(self,obj):
        try:
            qs = FireHistory.objects.get(occurrence_report=obj)
            return FireHistorySerializer(qs).data
        except FireHistory.DoesNotExist:
            return FireHistorySerializer().data
    
    def get_associated_species(self,obj):
        try:
            qs = AssociatedSpecies.objects.get(occurrence_report=obj)
            return AssociatedSpeciesSerializer(qs).data
        except AssociatedSpecies.DoesNotExist:
            return AssociatedSpeciesSerializer().data
    
    def get_observation_detail(self,obj):
        try:
            qs = ObservationDetail.objects.get(occurrence_report=obj)
            return ObservationDetailSerializer(qs).data
        except ObservationDetail.DoesNotExist:
            return ObservationDetailSerializer().data
    
    def get_plant_count(self,obj):
        try:
            qs = PlantCount.objects.get(occurrence_report=obj)
            return PlantCountSerializer(qs).data
        except PlantCount.DoesNotExist:
            return PlantCountSerializer().data
    
    def get_animal_observation(self,obj):
        try:
            qs = AnimalObservation.objects.get(occurrence_report=obj)
            return AnimalObservationSerializer(qs).data
        except AnimalObservation.DoesNotExist:
            return AnimalObservationSerializer().data
    
    def get_identification(self,obj):
        try:
            qs = Identification.objects.get(occurrence_report=obj)
            return IdentificationSerializer(qs).data
        except Identification.DoesNotExist:
            return IdentificationSerializer().data


class OccurrenceReportSerializer(BaseOccurrenceReportSerializer):
    submitter = serializers.SerializerMethodField(read_only=True)
    processing_status = serializers.SerializerMethodField(read_only=True)
    review_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)

    def get_readonly(self,obj):
        return obj.can_user_view

    # Priya updated as gives error for submitter when resubmit after amendment request
    def get_submitter(self,obj):
        if obj.submitter:
            email_user = retrieve_email_user(obj.submitter)
            return EmailUserSerializer(email_user).data
        else:
            return None

class SaveHabitatCompositionSerializer(serializers.ModelSerializer):
    # write_only removed from below as the serializer will not return that field in serializer.data
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    land_form = serializers.MultipleChoiceField(choices=[], allow_null=True, allow_blank=True, required=False)
    rock_type_id = serializers.IntegerField(required=False, allow_null=True)
    soil_type_id = serializers.IntegerField(required=False, allow_null=True)
    soil_colour_id = serializers.IntegerField(required=False, allow_null=True)
    soil_condition_id = serializers.IntegerField(required=False, allow_null=True)
    drainage_id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = HabitatComposition
        fields = (
            'id',
			'occurrence_report_id',
			'land_form',
			'rock_type_id',
			'loose_rock_percent',
			'soil_type_id',
			'soil_colour_id',
            'soil_condition_id',
            'drainage_id',
            'water_quality',
            'habitat_notes',
			)
    
    def __init__(self, *args, **kwargs):
        super(SaveHabitatCompositionSerializer, self).__init__(*args, **kwargs)
        self.fields['land_form'].choices = [(land_form_instance.id, land_form_instance.name) for land_form_instance in LandForm.objects.all()]


class SaveHabitatConditionSerializer(serializers.ModelSerializer):
	# occurrence_report_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    # write_only removed from below as the serializer will not return that field in serializer.data
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = HabitatCondition
        fields = (
            'id',
			'occurrence_report_id',
            'pristine',
            'excellent',
            'very_good',
            'good',
            'degraded',
            'completely_degraded',
			)

class SaveFireHistorySerializer(serializers.ModelSerializer):
	# occurrence_report_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    # write_only removed from below as the serializer will not return that field in serializer.data
    last_fire_estimate = serializers.DateField(format="%Y-%m",input_formats=['%Y-%m'], required=False,  allow_null=True)
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    intensity_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = FireHistory
        fields = (
            'id',
			'occurrence_report_id',
            'last_fire_estimate',
            'intensity_id',
            'comment',
            )

class SaveAssociatedSpeciesSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
	
    class Meta:
        model = AssociatedSpecies
        fields = (
            'id',
			'occurrence_report_id',
            'related_species',
            )


class SaveObservationDetailSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    observation_method_id = serializers.IntegerField(required=False, allow_null=True)
	
    class Meta:
        model = ObservationDetail
        fields = (
            'id',
			'occurrence_report_id',
            'observation_method_id',
            'area_surveyed',
            'survey_duration',
            )

class SavePlantCountSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    plant_count_method_id = serializers.IntegerField(required=False, allow_null=True)
    plant_count_accuracy_id = serializers.IntegerField(required=False, allow_null=True)
    counted_subject_id = serializers.IntegerField(required=False, allow_null=True)
    plant_condition_id = serializers.IntegerField(required=False, allow_null=True)
	
    class Meta:
        model = PlantCount
        fields = (
            'id',
			'occurrence_report_id',
            'plant_count_method_id',
            'plant_count_accuracy_id',
            'counted_subject_id',
            'plant_condition_id',
            'estimated_population_area',
            'quadrats_present',
            'quadrats_data_attached',
            'quadrats_surveyed',
            'individual_quadrat_area',
            'total_quadrat_area',
            'flowering_plants_per',
            'clonal_reproduction_present',
            'vegetative_state_present',
            'flower_bud_present',
            'flower_present',
            'immature_fruit_present',
            'ripe_fruit_present',
            'dehisced_fruit_present',
            'pollinator_observation',
            'comment',
            'simple_alive',
            'simple_dead',
            'detailed_alive_mature',
            'detailed_dead_mature',
            'detailed_alive_juvenile',
            'detailed_dead_juvenile',
            'detailed_alive_seedling',
            'detailed_dead_seedling',
            'detailed_alive_unknown',
            'detailed_dead_unknown',
            )


class SaveAnimalObservationSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    primary_detection_method = serializers.MultipleChoiceField(choices=[], allow_null=True, allow_blank=True, required=False)
    secondary_sign = serializers.MultipleChoiceField(choices=[], allow_null=True, allow_blank=True, required=False)
    reproductive_maturity = serializers.MultipleChoiceField(choices=[], allow_null=True, allow_blank=True, required=False)
    animal_health_id = serializers.IntegerField(required=False, allow_null=True)
    death_reason_id = serializers.IntegerField(required=False, allow_null=True)
	
    class Meta:
        model = AnimalObservation
        fields = (
            'id',
            'occurrence_report_id',
            'primary_detection_method',
            'secondary_sign',
            'reproductive_maturity',
            'animal_health_id',
            'death_reason_id',
            'total_count',
            'distinctive_feature',
            'action_taken',
            'action_required',
            'observation_detail_comment',
            'alive_adult',
            'dead_adult',
            'alive_juvenile',
            'dead_juvenile',
            'alive_pouch_young',
            'dead_pouch_young',
            'alive_unsure',
            'dead_unsure',
        )

    def __init__(self, *args, **kwargs):
        super(SaveAnimalObservationSerializer, self).__init__(*args, **kwargs)
        self.fields['primary_detection_method'].choices = [(primary_det_instance.id, primary_det_instance.name) for primary_det_instance in PrimaryDetectionMethod.objects.all()]
        self.fields['secondary_sign'].choices = [(sec_sign_instance.id, sec_sign_instance.name) for sec_sign_instance in SecondarySign.objects.all()]
        self.fields['reproductive_maturity'].choices = [(rep_maturity_instance.id, rep_maturity_instance.name) for rep_maturity_instance in ReproductiveMaturity.objects.all()]

class SaveIdentificationSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    identification_certainty_id = serializers.IntegerField(required=False, allow_null=True)
    sample_type_id = serializers.IntegerField(required=False, allow_null=True)
    sample_destination_id = serializers.IntegerField(required=False, allow_null=True)
    permit_type_id = serializers.IntegerField(required=False, allow_null=True)
	
    class Meta:
        model = Identification
        fields = (
            'id',
			'occurrence_report_id',
            'id_confirmed_by',
            'identification_certainty_id',
            'sample_type_id',
            'sample_destination_id',
            'permit_type_id',
            'permit_id',
            'collector_number',
            'barcode_number',
            'identification_comment',
            )

class SaveLocationSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=True, allow_null=False)
    datum_id = serializers.IntegerField(required=False, allow_null=True)
    coordination_source_id = serializers.IntegerField(required=False, allow_null=True)
    location_accuracy_id = serializers.IntegerField(required=False, allow_null=True)
    observation_date= serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False,allow_null=True)
	
    class Meta:
        model = Location
        fields = (
            'id',
			'occurrence_report_id',
            'observation_date',
            'location_description',
            'boundary_description',
            'new_occurrence',
            'boundary',
            'mapped_boundary',
            'buffer_radius',
            'datum_id',
            'coordination_source_id',
            'location_accuracy_id',
            # 'geojson_polygon',
            )

class ObserverDetailSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = ObserverDetail
        fields = (
			'id',
            'occurrence_report',
			'observer_name',
			'role',
			'contact',
			'organisation',
			'main_observer',
		)


class OccurrenceReportGeometrySaveSerializer(GeoFeatureModelSerializer):
    occurrence_report_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = OccurrenceReportGeometry
        geo_field = "polygon"
        fields = (
            "id",
            "occurrence_report_id",
            "polygon",
            "intersects",
            "drawn_by",
            "locked",
        )
        read_only_fields = ("id",)

