import logging

from django.urls import reverse
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from boranga.components.conservation_status.models import ConservationStatus
from boranga.components.main.serializers import (
    CommunicationLogEntrySerializer,
    EmailUserSerializer,
)
from boranga.components.spatial.utils import wkb_to_geojson
from boranga.components.main.utils import get_geometry_source
from boranga.components.occurrence.models import (
    LandForm,
    GeometryType,
    OCCAnimalObservation,
    OCCAssociatedSpecies,
    OCCConservationThreat,
    OCCFireHistory,
    OCCHabitatComposition,
    OCCHabitatCondition,
    OCCIdentification,
    OCCLocation,
    OCCObservationDetail,
    OCCObserverDetail,
    OCCPlantCount,
    Occurrence,
    OccurrenceDocument,
    OccurrenceGeometry,
    OccurrenceLogEntry,
    OccurrenceReport,
    OccurrenceReportAmendmentRequest,
    OccurrenceReportAmendmentRequestDocument,
    OccurrenceReportApprovalDetails,
    OccurrenceReportDeclinedDetails,
    OccurrenceReportDocument,
    OccurrenceReportGeometry,
    OccurrenceReportLogEntry,
    OccurrenceReportReferral,
    OccurrenceReportUserAction,
    OccurrenceTenure,
    OccurrenceUserAction,
    OCCVegetationStructure,
    OCRAnimalObservation,
    OCRAssociatedSpecies,
    OCRConservationThreat,
    OCRFireHistory,
    OCRHabitatComposition,
    OCRHabitatCondition,
    OCRIdentification,
    OCRLocation,
    OCRObservationDetail,
    OCRObserverDetail,
    OCRPlantCount,
    OCRVegetationStructure,
    PrimaryDetectionMethod,
    ReproductiveMaturity,
    SecondarySign,
)
from boranga.components.species_and_communities.models import CommunityTaxonomy
from boranga.helpers import (
    is_internal,
    is_new_external_contributor,
    is_occurrence_approver,
    is_occurrence_assessor,
)
from boranga.ledger_api_utils import retrieve_email_user

logger = logging.getLogger("boranga")


class OccurrenceSerializer(serializers.ModelSerializer):
    processing_status = serializers.CharField(source="get_processing_status_display")
    scientific_name = serializers.CharField(
        source="species.taxonomy.scientific_name", allow_null=True
    )
    group_type = serializers.CharField(source="group_type.name", allow_null=True)
    group_type_id = serializers.CharField(source="group_type.id", allow_null=True)
    can_user_edit = serializers.SerializerMethodField()
    submitter = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    habitat_composition = serializers.SerializerMethodField()
    habitat_condition = serializers.SerializerMethodField()
    vegetation_structure = serializers.SerializerMethodField()
    fire_history = serializers.SerializerMethodField()
    associated_species = serializers.SerializerMethodField()
    observation_detail = serializers.SerializerMethodField()
    plant_count = serializers.SerializerMethodField()
    animal_observation = serializers.SerializerMethodField()
    identification = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()
    occurrence_reports = serializers.SerializerMethodField()

    class Meta:
        model = Occurrence
        fields = "__all__"

    def get_processing_status(self, obj):
        return obj.get_processing_status_display()

    def get_can_user_edit(self, obj):
        request = self.context["request"]
        return obj.can_user_edit(request)
    
    def get_submitter(self, obj):
        if obj.submitter:
            email_user = retrieve_email_user(obj.submitter)
            return EmailUserSerializer(email_user).data
        else:
            return None

    def get_location(self, obj):
        try:
            qs = OCCLocation.objects.get(occurrence=obj)
            return OCCLocationSerializer(qs).data
        except OCCLocation.DoesNotExist:
            return OCCLocationSerializer().data

    def get_habitat_composition(self, obj):
        try:
            qs = OCCHabitatComposition.objects.get(occurrence=obj)
            return OCCHabitatCompositionSerializer(qs).data
        except OCCHabitatComposition.DoesNotExist:
            return OCCHabitatCompositionSerializer().data

    def get_habitat_condition(self, obj):
        try:
            qs = OCCHabitatCondition.objects.get(occurrence=obj)
            return OCCHabitatConditionSerializer(qs).data
        except OCCHabitatCondition.DoesNotExist:
            return OCCHabitatConditionSerializer().data

    def get_vegetation_structure(self, obj):
        try:
            qs = OCCVegetationStructure.objects.get(occurrence=obj)
            return OCCVegetationStructureSerializer(qs).data
        except OCCVegetationStructure.DoesNotExist:
            return OCCVegetationStructureSerializer().data

    def get_fire_history(self, obj):
        try:
            qs = OCCFireHistory.objects.get(occurrence=obj)
            return OCCFireHistorySerializer(qs).data
        except OCCFireHistory.DoesNotExist:
            return OCCFireHistorySerializer().data

    def get_associated_species(self, obj):
        try:
            qs = OCCAssociatedSpecies.objects.get(occurrence=obj)
            return OCCAssociatedSpeciesSerializer(qs).data
        except OCCAssociatedSpecies.DoesNotExist:
            return OCCAssociatedSpeciesSerializer().data

    def get_observation_detail(self, obj):
        try:
            qs = OCCObservationDetail.objects.get(occurrence=obj)
            return OCCObservationDetailSerializer(qs).data
        except OCCObservationDetail.DoesNotExist:
            return OCCObservationDetailSerializer().data

    def get_plant_count(self, obj):
        try:
            qs = OCCPlantCount.objects.get(occurrence=obj)
            return OCCPlantCountSerializer(qs).data
        except OCCPlantCount.DoesNotExist:
            return OCCPlantCountSerializer().data

    def get_animal_observation(self, obj):
        try:
            qs = OCCAnimalObservation.objects.get(occurrence=obj)
            return OCCAnimalObservationSerializer(qs).data
        except OCCAnimalObservation.DoesNotExist:
            return OCCAnimalObservationSerializer().data

    def get_identification(self, obj):
        try:
            qs = OCCIdentification.objects.get(occurrence=obj)
            return OCCIdentificationSerializer(qs).data
        except OCCIdentification.DoesNotExist:
            return OCCIdentificationSerializer().data

    def get_label(self, obj):
        return "Occurrence"

    def get_model_name(self, obj):
        return "occurrence"

    def get_occurrence_reports(self, obj):
        serializer = ListOccurrenceReportSerializer(
            obj.occurrence_reports.all(), many=True, context=self.context
        )
        return serializer.data


class ListOccurrenceReportSerializer(serializers.ModelSerializer):
    group_type = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    customer_status = serializers.CharField(source="get_customer_status_display")

    class Meta:
        model = OccurrenceReport
        fields = (
            "id",
            "occurrence_report_number",
            "group_type",
            "scientific_name",
            "community_name",
            "processing_status",
            "customer_status",
            "can_user_view",
            "can_user_edit",
        )
        datatables_always_serialize = (
            "id",
            "occurrence_report_number",
            "group_type",
            "scientific_name",
            "community_name",
            "processing_status",
            "customer_status",
            "can_user_view",
            "can_user_edit",
        )

    def get_group_type(self, obj):
        if obj.group_type:
            return obj.group_type.get_name_display()
        return ""

    def get_scientific_name(self, obj):
        if obj.species:
            if obj.species.taxonomy:
                return obj.species.taxonomy.scientific_name
        return ""

    def get_community_name(self, obj):
        if obj.community:
            try:
                taxonomy = CommunityTaxonomy.objects.get(community=obj.community)
                return taxonomy.community_name
            except CommunityTaxonomy.DoesNotExist:
                return ""
        return ""


class ListInternalOccurrenceReportSerializer(serializers.ModelSerializer):
    scientific_name = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    submitter = serializers.SerializerMethodField()
    processing_status_display = serializers.CharField(
        source="get_processing_status_display"
    )
    reported_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    effective_from = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", allow_null=True
    )
    effective_to = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", allow_null=True
    )
    review_due_date = serializers.DateField(format="%Y-%m-%d", allow_null=True)
    reported_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    assessor_edit = serializers.SerializerMethodField(read_only=True)
    internal_user_edit = serializers.SerializerMethodField()
    can_user_approve = serializers.SerializerMethodField()
    can_user_assess = serializers.SerializerMethodField()
    occurrence = serializers.IntegerField(source="occurrence.id", allow_null=True)
    occurrence_name = serializers.CharField(
        source="occurrence.occurrence_number", allow_null=True
    )
    is_new_contributor = serializers.SerializerMethodField()
    observation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", allow_null=True)

    class Meta:
        model = OccurrenceReport
        fields = (
            "id",
            "occurrence_report_number",
            "species",
            "community",
            # 'group_type',
            "scientific_name",
            "community_name",
            "reported_date",
            "submitter",
            "processing_status",
            "processing_status_display",
            "can_user_edit",
            "can_user_view",
            "can_user_assess",
            "can_user_approve",
            "assessor_edit",
            "internal_user_edit",
            "occurrence",
            "occurrence_name",
            "effective_from",
            "effective_to",
            "review_due_date",
            "is_new_contributor",
            "observation_date",
        )
        datatables_always_serialize = (
            "id",
            "occurrence_report_number",
            "species",
            "scientific_name",
            "community",
            "community_name",
            "reported_date",
            "submitter",
            "processing_status",
            "processing_status_display",
            "can_user_edit",
            "can_user_view",
            "can_user_approve",
            "can_user_assess",
            "internal_user_edit",
            "is_new_contributor",
        )

    def get_scientific_name(self, obj):
        if obj.species and obj.species.taxonomy:
                return obj.species.taxonomy.scientific_name

    def get_community_name(self, obj):
        if obj.community:
            if obj.community.taxonomy:
                return obj.community.taxonomy.community_name
        return ""

    def get_submitter(self, obj):
        if obj.submitter:
            email_user = retrieve_email_user(obj.submitter)
            return email_user.get_full_name()
        else:
            return None

    def get_assessor_edit(self, obj):
        request = self.context["request"]
        user = request.user
        if obj.can_user_edit:
            if user in obj.allowed_assessors:
                return True
        return False

    def get_internal_user_edit(self, obj):
        request = self.context["request"]
        if obj.can_user_edit:
            if obj.internal_application is True and obj.submitter == request.user.id:
                return True
        else:
            return False

    def get_can_user_assess(self, obj):
        request = self.context["request"]
        return is_occurrence_assessor(request) and (
            obj.processing_status == OccurrenceReport.PROCESSING_STATUS_WITH_ASSESSOR
            or obj.processing_status == OccurrenceReport.PROCESSING_STATUS_WITH_REFERRAL
        )

    def get_can_user_approve(self, obj):
        request = self.context["request"]
        return (
            is_occurrence_assessor(request)
            and obj.processing_status
            == OccurrenceReport.PROCESSING_STATUS_WITH_APPROVER
        )

    def get_is_new_contributor(self, obj):
        return is_new_external_contributor(obj.submitter)


class OCRHabitatCompositionSerializer(serializers.ModelSerializer):

    land_form = serializers.MultipleChoiceField(
        choices=[],
        allow_null=True, allow_blank=True, required=False
    )

    class Meta:
        model = OCRHabitatComposition
        fields = (
            "id",
            "occurrence_report_id",
            "land_form",
            "rock_type_id",
            "loose_rock_percent",
            "soil_type_id",
            "soil_colour_id",
            "soil_condition_id",
            "drainage_id",
            "water_quality",
            "habitat_notes",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["land_form"].choices = OCRHabitatComposition._meta.get_field("land_form").choices

class OCRHabitatConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OCRHabitatCondition
        fields = (
            "id",
            "occurrence_report_id",
            "pristine",
            "excellent",
            "very_good",
            "good",
            "degraded",
            "completely_degraded",
        )


class OCRVegetationStructureSerializer(serializers.ModelSerializer):

    class Meta:
        model = OCRVegetationStructure
        fields = (
            "id",
            "occurrence_report_id",
            "free_text_field_one",
            "free_text_field_two",
            "free_text_field_three",
            "free_text_field_four",
        )


class OCRFireHistorySerializer(serializers.ModelSerializer):
    last_fire_estimate = serializers.DateField(format="%Y-%m")

    class Meta:
        model = OCRFireHistory
        fields = (
            "id",
            "occurrence_report_id",
            "last_fire_estimate",
            "intensity_id",
            "comment",
        )


class OCRAssociatedSpeciesSerializer(serializers.ModelSerializer):

    class Meta:
        model = OCRAssociatedSpecies
        fields = (
            "id",
            "occurrence_report_id",
            "comment",
            "related_species",
        )


class OCRObservationDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OCRObservationDetail
        fields = (
            "id",
            "occurrence_report_id",
            "observation_method_id",
            "area_surveyed",
            "survey_duration",
        )


class OCRPlantCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = OCRPlantCount
        fields = (
            "id",
            "occurrence_report_id",
            "plant_count_method_id",
            "plant_count_accuracy_id",
            "counted_subject_id",
            "plant_condition_id",
            "estimated_population_area",
            "quadrats_present",
            "quadrats_data_attached",
            "quadrats_surveyed",
            "individual_quadrat_area",
            "total_quadrat_area",
            "flowering_plants_per",
            "clonal_reproduction_present",
            "vegetative_state_present",
            "flower_bud_present",
            "flower_present",
            "immature_fruit_present",
            "ripe_fruit_present",
            "dehisced_fruit_present",
            "pollinator_observation",
            "comment",
            "simple_alive",
            "simple_dead",
            "detailed_alive_mature",
            "detailed_dead_mature",
            "detailed_alive_juvenile",
            "detailed_dead_juvenile",
            "detailed_alive_seedling",
            "detailed_dead_seedling",
            "detailed_alive_unknown",
            "detailed_dead_unknown",
        )


class OCRAnimalObservationSerializer(serializers.ModelSerializer):

    primary_detection_method = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    secondary_sign = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    reproductive_maturity = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )

    class Meta:
        model = OCRAnimalObservation
        fields = (
            "id",
            "occurrence_report_id",
            "primary_detection_method",
            "secondary_sign",
            "reproductive_maturity",
            "animal_health_id",
            "death_reason_id",
            "total_count",
            "distinctive_feature",
            "action_taken",
            "action_required",
            "observation_detail_comment",
            "alive_adult",
            "dead_adult",
            "alive_juvenile",
            "dead_juvenile",
            "alive_pouch_young",
            "dead_pouch_young",
            "alive_unsure",
            "dead_unsure",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["primary_detection_method"].choices = OCRAnimalObservation._meta.get_field("primary_detection_method").choices
        self.fields["secondary_sign"].choices = OCRAnimalObservation._meta.get_field("secondary_sign").choices
        self.fields["reproductive_maturity"].choices = OCRAnimalObservation._meta.get_field("reproductive_maturity").choices

class OCRIdentificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OCRIdentification
        fields = (
            "id",
            "occurrence_report_id",
            "id_confirmed_by",
            "identification_certainty_id",
            "sample_type_id",
            "sample_destination_id",
            "permit_type_id",
            "permit_id",
            "collector_number",
            "barcode_number",
            "identification_comment",
        )


class OCRLocationSerializer(serializers.ModelSerializer):
    # observation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # geojson_point = serializers.SerializerMethodField()
    # geojson_polygon = serializers.SerializerMethodField()
    has_boundary = serializers.SerializerMethodField()
    has_points = serializers.SerializerMethodField()

    class Meta:
        model = OCRLocation
        fields = (
            "id",
            "occurrence_report_id",
            # "observation_date",
            "location_description",
            "boundary_description",
            "new_occurrence",
            "boundary",
            "mapped_boundary",
            "buffer_radius",
            "datum_id",
            "epsg_code",
            "coordination_source_id",
            "location_accuracy_id",
            "region_id",
            "district_id",
            "locality",
            # 'geojson_point',
            # 'geojson_polygon',
            "has_boundary",
            "has_points",
        )

    def get_has_boundary(self, obj):
        return obj.occurrence_report.ocr_geometry.annotate(geom_type=GeometryType("geometry")).filter(geom_type="POLYGON").exists()

    def get_has_points(self, obj):
        return obj.occurrence_report.ocr_geometry.annotate(geom_type=GeometryType("geometry")).filter(geom_type="POINT").exists()

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
    geometry_source = serializers.SerializerMethodField()
    report_copied_from = serializers.SerializerMethodField(read_only=True)
    srid = serializers.SerializerMethodField(read_only=True)
    original_geometry = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OccurrenceReportGeometry
        geo_field = "geometry"
        fields = (
            "id",
            "occurrence_report_id",
            "geometry",
            "original_geometry",
            "srid",
            "area_sqm",
            "area_sqhm",
            "intersects",
            "geometry_source",
            "locked",
            "report_copied_from",
        )
        read_only_fields = ("id",)

    def get_srid(self, obj):
        if obj.geometry:
            return obj.geometry.srid
        else:
            return None

    def get_geometry_source(self, obj):
        return get_geometry_source(obj)

    def get_report_copied_from(self, obj):
        if obj.copied_from:
            return ListOCRReportMinimalSerializer(
                obj.copied_from.occurrence_report, context=self.context
            ).data

        return None

    def get_original_geometry(self, obj):
        if obj.original_geometry_ewkb:
            return wkb_to_geojson(obj.original_geometry_ewkb)
        else:
            return None


class ListOCRReportMinimalSerializer(serializers.ModelSerializer):
    ocr_geometry = OccurrenceReportGeometrySerializer(many=True, read_only=True)
    label = serializers.SerializerMethodField(read_only=True)
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
            "label",
            "occurrence_report_number",
            "processing_status",
            "processing_status_display",
            "ocr_geometry",
            "lodgement_date",
            "lodgement_date_display",
            "details_url",
        )

    def get_label(self, obj):
        return "Occurrence Report"

    def get_details_url(self, obj):
        request = self.context["request"]

        if request.user.is_authenticated:
            if is_internal(request):
                return reverse(
                    "internal-occurrence-report-detail",
                    kwargs={"occurrence_report_pk": obj.id},
                )
            else:
                return reverse(
                    "external-occurrence-report-detail",
                    kwargs={"occurrence_report_pk": obj.id},
                )

        return None


class OccurrenceUserActionSerializer(serializers.ModelSerializer):
    who = serializers.SerializerMethodField()

    class Meta:
        model = OccurrenceUserAction
        fields = "__all__"

    def get_who(self, obj):
        email_user = retrieve_email_user(obj.who)
        fullname = email_user.get_full_name()
        return fullname


class OccurrenceLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = OccurrenceLogEntry
        fields = "__all__"
        read_only_fields = ("customer",)

    def get_documents(self, obj):
        return [[d.name, d._file.url] for d in obj.documents.all()]


class ListOccurrenceSerializer(OccurrenceSerializer):
    processing_status = serializers.CharField()
    processing_status_display = serializers.CharField(
        source="get_processing_status_display"
    )
    effective_from = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", allow_null=True
    )
    effective_to = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", allow_null=True
    )
    review_due_date = serializers.DateField(format="%Y-%m-%d", allow_null=True)
    community_number = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    community_migrated_id = serializers.SerializerMethodField()
    wild_status = serializers.CharField(source="wild_status.name", allow_null=True)
    can_user_edit = serializers.SerializerMethodField()

    class Meta:
        model = Occurrence
        fields = (
            "id",
            "occurrence_number",
            "occurrence_name",
            "scientific_name",
            "community_number",
            "community_name",
            "community_migrated_id",
            "wild_status",
            "group_type",
            "group_type_id",
            "number_of_reports",
            "processing_status",
            "processing_status_display",
            "effective_from",
            "effective_to",
            "review_due_date",
            "can_user_edit",
        )
        datatables_always_serialize = (
            "id",
            "occurrence_number",
            "scientific_name",
            "group_type",
            "number_of_reports",
            "processing_status",
            "processing_status_display",
            "can_user_edit",
        )

    def get_community_number(self, obj):
        if not obj.community:
            return ""

        return obj.community.community_number

    def get_community_name(self, obj):
        if not obj.community:
            return ""

        if not obj.community.taxonomy:
            return ""

        return obj.community.taxonomy.community_name

    def get_community_migrated_id(self, obj):
        if not obj.community:
            return ""

        if not obj.community.taxonomy:
            return ""

        return obj.community.taxonomy.community_migrated_id

    def get_conservation_status(self, obj):
        if not obj.community:
            return None

        try:
            conservation_status = ConservationStatus.objects.get(
                community=obj.community,
                processing_status="approved",
            )
            return conservation_status
        except ConservationStatus.DoesNotExist:
            return None

    def get_can_user_edit(self, obj):
        request = self.context["request"]
        return obj.can_user_edit(request)


class BaseOccurrenceReportSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    group_type = serializers.SerializerMethodField(read_only=True)
    # group_type_id = serializers.SerializerMethodField(read_only=True)
    allowed_assessors = EmailUserSerializer(many=True)
    location = serializers.SerializerMethodField()
    habitat_composition = serializers.SerializerMethodField()
    habitat_condition = serializers.SerializerMethodField()
    vegetation_structure = serializers.SerializerMethodField()
    fire_history = serializers.SerializerMethodField()
    associated_species = serializers.SerializerMethodField()
    observation_detail = serializers.SerializerMethodField()
    plant_count = serializers.SerializerMethodField()
    animal_observation = serializers.SerializerMethodField()
    identification = serializers.SerializerMethodField()
    ocr_geometry = OccurrenceReportGeometrySerializer(many=True, read_only=True)
    # label used for new polygon featuretoast on map_component
    label = serializers.SerializerMethodField(read_only=True)
    model_name = serializers.SerializerMethodField(read_only=True)
    occurrence = OccurrenceSerializer(read_only=True, allow_null=True)
    lodgement_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True
    )
    observation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = OccurrenceReport
        fields = (
            "id",
            "group_type",
            "group_type_id",
            "species_id",
            "community_id",
            "occurrence_report_number",
            "reported_date",
            "lodgement_date",
            "reported_date",
            "applicant_type",
            "applicant",
            "submitter",
            # 'assigned_officer',
            "customer_status",
            "processing_status",
            "review_status",
            "readonly",
            "can_user_edit",
            "can_user_view",
            "reference",
            "applicant_details",
            # 'assigned_approver',
            "allowed_assessors",
            "deficiency_data",
            "assessor_data",
            "location",
            "habitat_composition",
            "habitat_condition",
            "vegetation_structure",
            "fire_history",
            "associated_species",
            "observation_detail",
            "plant_count",
            "animal_observation",
            "identification",
            "ocr_geometry",
            "label",
            "model_name",
            "occurrence",
            "observation_date",
            "site",
        )

    def get_readonly(self, obj):
        return False

    def get_group_type(self, obj):
        return obj.group_type.name

    def get_processing_status(self, obj):
        return obj.get_processing_status_display()

    def get_review_status(self, obj):
        return obj.get_review_status_display()

    def get_customer_status(self, obj):
        return obj.get_customer_status_display()

    def get_location(self, obj):
        try:
            qs = OCRLocation.objects.get(occurrence_report=obj)
            return OCRLocationSerializer(qs).data
        except OCRLocation.DoesNotExist:
            return OCRLocationSerializer().data

    def get_habitat_composition(self, obj):
        try:
            qs = OCRHabitatComposition.objects.get(occurrence_report=obj)
            return OCRHabitatCompositionSerializer(qs).data
        except OCRHabitatComposition.DoesNotExist:
            return OCRHabitatCompositionSerializer().data

    def get_habitat_condition(self, obj):
        try:
            qs = OCRHabitatCondition.objects.get(occurrence_report=obj)
            return OCRHabitatConditionSerializer(qs).data
        except OCRHabitatCondition.DoesNotExist:
            return OCRHabitatConditionSerializer().data

    def get_vegetation_structure(self, obj):
        try:
            qs = OCRVegetationStructure.objects.get(occurrence_report=obj)
            return OCRVegetationStructureSerializer(qs).data
        except OCRVegetationStructure.DoesNotExist:
            return OCRVegetationStructureSerializer().data

    def get_fire_history(self, obj):
        try:
            qs = OCRFireHistory.objects.get(occurrence_report=obj)
            return OCRFireHistorySerializer(qs).data
        except OCRFireHistory.DoesNotExist:
            return OCRFireHistorySerializer().data

    def get_associated_species(self, obj):
        try:
            qs = OCRAssociatedSpecies.objects.get(occurrence_report=obj)
            return OCRAssociatedSpeciesSerializer(qs).data
        except OCRAssociatedSpecies.DoesNotExist:
            return OCRAssociatedSpeciesSerializer().data

    def get_observation_detail(self, obj):
        try:
            qs = OCRObservationDetail.objects.get(occurrence_report=obj)
            return OCRObservationDetailSerializer(qs).data
        except OCRObservationDetail.DoesNotExist:
            return OCRObservationDetailSerializer().data

    def get_plant_count(self, obj):
        try:
            qs = OCRPlantCount.objects.get(occurrence_report=obj)
            return OCRPlantCountSerializer(qs).data
        except OCRPlantCount.DoesNotExist:
            return OCRPlantCountSerializer().data

    def get_animal_observation(self, obj):
        try:
            qs = OCRAnimalObservation.objects.get(occurrence_report=obj)
            return OCRAnimalObservationSerializer(qs).data
        except OCRAnimalObservation.DoesNotExist:
            return OCRAnimalObservationSerializer().data

    def get_identification(self, obj):
        try:
            qs = OCRIdentification.objects.get(occurrence_report=obj)
            return OCRIdentificationSerializer(qs).data
        except OCRIdentification.DoesNotExist:
            return OCRIdentificationSerializer().data

    def get_label(self, obj):
        return "Occurrence Report"

    def get_model_name(self, obj):
        return "occurrencereport"


class OccurrenceReportSerializer(BaseOccurrenceReportSerializer):
    submitter = serializers.SerializerMethodField(read_only=True)
    processing_status = serializers.SerializerMethodField(read_only=True)
    review_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)

    def get_readonly(self, obj):
        return obj.can_user_view

    # Priya updated as gives error for submitter when resubmit after amendment request
    def get_submitter(self, obj):
        if obj.submitter:
            email_user = retrieve_email_user(obj.submitter)
            return EmailUserSerializer(email_user).data
        else:
            return None


class CreateOccurrenceReportSerializer(BaseOccurrenceReportSerializer):
    class Meta:
        model = OccurrenceReport
        fields = (
            "id",
            "submitter",
        )
        read_only_fields = (
            "id",
            "submitter",
        )


class CreateOccurrenceSerializer(BaseOccurrenceReportSerializer):
    class Meta:
        model = Occurrence
        fields = (
            "id",
            "submitter",
        )
        read_only_fields = (
            "id",
            "submitter",
        )


class OccurrenceReportDeclinedDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccurrenceReportDeclinedDetails
        fields = "__all__"


class OccurrenceReportApprovalDetailsSerializer(serializers.ModelSerializer):
    occurrence_number = serializers.CharField(
        source="occurrence.occurrence_number", allow_null=True
    )
    occurrence_name = serializers.CharField(
        source="occurrence.occurrence_name", allow_null=True
    )
    officer_name = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = OccurrenceReportApprovalDetails
        fields = "__all__"


class OccurrenceReportReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccurrenceReportReferral
        fields = "__all__"


class InternalOccurrenceReportReferralSerializer(serializers.ModelSerializer):
    referral = serializers.SerializerMethodField()
    referral_comment = serializers.SerializerMethodField()
    referral_status = serializers.CharField(source="get_processing_status_display")

    class Meta:
        model = OccurrenceReportReferral
        fields = "__all__"

    def get_referral(self, obj):
        return EmailUserSerializer(retrieve_email_user(obj.referral)).data

    def get_referral_comment(self, obj):
        return obj.referral_comment if obj.referral_comment else ""


class InternalOccurrenceReportSerializer(OccurrenceReportSerializer):
    can_user_approve = serializers.SerializerMethodField()
    can_user_assess = serializers.SerializerMethodField()
    can_user_action = serializers.SerializerMethodField()
    current_assessor = serializers.SerializerMethodField(read_only=True)
    approval_details = OccurrenceReportApprovalDetailsSerializer(
        read_only=True, allow_null=True
    )
    declined_details = OccurrenceReportDeclinedDetailsSerializer(
        read_only=True, allow_null=True
    )
    assessor_mode = serializers.SerializerMethodField()
    latest_referrals = InternalOccurrenceReportReferralSerializer(
        many=True, read_only=True, allow_null=True
    )
    referrals = InternalOccurrenceReportReferralSerializer(
        many=True, read_only=True, allow_null=True
    )
    readonly = serializers.SerializerMethodField(read_only=True)
    is_new_contributor = serializers.SerializerMethodField()

    class Meta:
        model = OccurrenceReport
        fields = (
            "id",
            "group_type",
            "group_type_id",
            "species_id",
            "community_id",
            "occurrence_report_number",
            "reported_date",
            "lodgement_date",
            "reported_date",
            "applicant_type",
            "applicant",
            "submitter",
            "assigned_officer",
            "customer_status",
            "processing_status",
            "review_status",
            "readonly",
            "can_user_edit",
            "can_user_view",
            "can_user_assess",
            "can_user_approve",
            "can_user_action",
            "reference",
            "applicant_details",
            "allowed_assessors",
            "deficiency_data",
            "assessor_data",
            "location",
            "habitat_composition",
            "habitat_condition",
            "vegetation_structure",
            "fire_history",
            "associated_species",
            "observation_detail",
            "plant_count",
            "animal_observation",
            "identification",
            "ocr_geometry",
            "label",
            "model_name",
            "occurrence",
            "current_assessor",
            "assigned_approver",
            "proposed_decline_status",
            "declined_details",
            "approval_details",
            "internal_application",
            "assessor_mode",
            "latest_referrals",
            "referrals",
            "finalised",
            "is_new_contributor",
            "observation_date",
            "site",
        )

    def get_readonly(self, obj):
        # Assessor can edit the report in appropriate statuses
        if self.get_can_user_assess(obj):
            return False

        # The only other case where an internal user can edit is
        # if the application is internal, the user is the submitter and
        # the report is in draft status
        request = self.context["request"]
        if (
            obj.internal_application
            and request.user.id == obj.submitter
            and obj.processing_status == OccurrenceReport.PROCESSING_STATUS_DRAFT
        ):
            return False
        return True

    def get_can_user_assess(self, obj):
        request = self.context["request"]
        return (
            (is_occurrence_assessor(request) or is_occurrence_approver(request))
            and obj.processing_status
            in [
                OccurrenceReport.PROCESSING_STATUS_WITH_ASSESSOR,
                OccurrenceReport.PROCESSING_STATUS_WITH_REFERRAL,
                OccurrenceReport.PROCESSING_STATUS_UNLOCKED,
            ]
            and obj.assigned_officer == request.user.id
        )

    def get_can_user_approve(self, obj):
        request = self.context["request"]
        return (
            is_occurrence_approver(request)
            and obj.processing_status == OccurrenceReport.CUSTOMER_STATUS_WITH_APPROVER
            and obj.assigned_approver == request.user.id
        )

    def get_can_user_change_lock(self, obj):
        request = self.context["request"]
        return (
            is_occurrence_assessor(request) or is_occurrence_approver(request)
        ) and obj.processing_status in [
            OccurrenceReport.PROCESSING_STATUS_APPROVED,
            OccurrenceReport.PROCESSING_STATUS_UNLOCKED,
        ]

    def get_can_user_action(self, obj):
        return (
            self.get_can_user_assess(obj)
            or self.get_can_user_approve(obj)
            or self.get_can_user_change_lock(obj)
        )

    def get_current_assessor(self, obj):
        user = self.context["request"].user
        return {
            "id": user.id,
            "name": user.get_full_name(),
            "email": user.email,
        }

    def get_assessor_mode(self, obj):
        request = self.context["request"]
        return {
            "assessor_mode": True,
            "has_assessor_mode": obj.has_assessor_mode(request),
            "has_unlocked_mode": obj.has_unlocked_mode(request),
            "assessor_box_view": obj.assessor_comments_view(request),
            "assessor_can_assess": obj.can_assess(request),
            "assessor_level": "assessor",
        }

    def get_is_new_contributor(self, obj):
        return is_new_external_contributor(obj.submitter)


class SaveOCRHabitatCompositionSerializer(serializers.ModelSerializer):
    # write_only removed from below as the serializer will not return that field in serializer.data
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    land_form = serializers.MultipleChoiceField(
        choices=[],
        allow_null=True, allow_blank=True, required=False
    )
    rock_type_id = serializers.IntegerField(required=False, allow_null=True)
    soil_type_id = serializers.IntegerField(required=False, allow_null=True)
    soil_colour_id = serializers.IntegerField(required=False, allow_null=True)
    soil_condition_id = serializers.IntegerField(required=False, allow_null=True)
    drainage_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCRHabitatComposition
        fields = (
            "id",
            "occurrence_report_id",
            "land_form",
            "rock_type_id",
            "loose_rock_percent",
            "soil_type_id",
            "soil_colour_id",
            "soil_condition_id",
            "drainage_id",
            "water_quality",
            "habitat_notes",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["land_form"].choices = OCRHabitatComposition._meta.get_field("land_form").choices

class SaveOCRHabitatConditionSerializer(serializers.ModelSerializer):
    # occurrence_report_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    # write_only removed from below as the serializer will not return that field in serializer.data
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCRHabitatCondition
        fields = (
            "id",
            "occurrence_report_id",
            "pristine",
            "excellent",
            "very_good",
            "good",
            "degraded",
            "completely_degraded",
        )


class SaveOCRVegetationStructureSerializer(serializers.ModelSerializer):
    # write_only removed from below as the serializer will not return that field in serializer.data
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCRVegetationStructure
        fields = (
            "id",
            "occurrence_report_id",
            "free_text_field_one",
            "free_text_field_two",
            "free_text_field_three",
            "free_text_field_four",
        )


class SaveOCRFireHistorySerializer(serializers.ModelSerializer):
    # occurrence_report_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    # write_only removed from below as the serializer will not return that field in serializer.data
    last_fire_estimate = serializers.DateField(
        format="%Y-%m", input_formats=["%Y-%m"], required=False, allow_null=True
    )
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    intensity_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCRFireHistory
        fields = (
            "id",
            "occurrence_report_id",
            "last_fire_estimate",
            "intensity_id",
            "comment",
        )


class SaveOCRAssociatedSpeciesSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCRAssociatedSpecies
        fields = (
            "id",
            "occurrence_report_id",
            "comment",
            "related_species",
        )


class SaveOCRObservationDetailSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    observation_method_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCRObservationDetail
        fields = (
            "id",
            "occurrence_report_id",
            "observation_method_id",
            "area_surveyed",
            "survey_duration",
        )


class SaveOCRPlantCountSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    plant_count_method_id = serializers.IntegerField(required=False, allow_null=True)
    plant_count_accuracy_id = serializers.IntegerField(required=False, allow_null=True)
    counted_subject_id = serializers.IntegerField(required=False, allow_null=True)
    plant_condition_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCRPlantCount
        fields = (
            "id",
            "occurrence_report_id",
            "plant_count_method_id",
            "plant_count_accuracy_id",
            "counted_subject_id",
            "plant_condition_id",
            "estimated_population_area",
            "quadrats_present",
            "quadrats_data_attached",
            "quadrats_surveyed",
            "individual_quadrat_area",
            "total_quadrat_area",
            "flowering_plants_per",
            "clonal_reproduction_present",
            "vegetative_state_present",
            "flower_bud_present",
            "flower_present",
            "immature_fruit_present",
            "ripe_fruit_present",
            "dehisced_fruit_present",
            "pollinator_observation",
            "comment",
            "simple_alive",
            "simple_dead",
            "detailed_alive_mature",
            "detailed_dead_mature",
            "detailed_alive_juvenile",
            "detailed_dead_juvenile",
            "detailed_alive_seedling",
            "detailed_dead_seedling",
            "detailed_alive_unknown",
            "detailed_dead_unknown",
        )


class SaveOCRAnimalObservationSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    primary_detection_method = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    secondary_sign = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    reproductive_maturity = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    animal_health_id = serializers.IntegerField(required=False, allow_null=True)
    death_reason_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCRAnimalObservation
        fields = (
            "id",
            "occurrence_report_id",
            "primary_detection_method",
            "secondary_sign",
            "reproductive_maturity",
            "animal_health_id",
            "death_reason_id",
            "total_count",
            "distinctive_feature",
            "action_taken",
            "action_required",
            "observation_detail_comment",
            "alive_adult",
            "dead_adult",
            "alive_juvenile",
            "dead_juvenile",
            "alive_pouch_young",
            "dead_pouch_young",
            "alive_unsure",
            "dead_unsure",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["primary_detection_method"].choices = OCRAnimalObservation._meta.get_field("primary_detection_method").choices
        self.fields["secondary_sign"].choices = OCRAnimalObservation._meta.get_field("secondary_sign").choices
        self.fields["reproductive_maturity"].choices = OCRAnimalObservation._meta.get_field("reproductive_maturity").choices


class SaveOCRIdentificationSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    identification_certainty_id = serializers.IntegerField(
        required=False, allow_null=True
    )
    sample_type_id = serializers.IntegerField(required=False, allow_null=True)
    sample_destination_id = serializers.IntegerField(required=False, allow_null=True)
    permit_type_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCRIdentification
        fields = (
            "id",
            "occurrence_report_id",
            "id_confirmed_by",
            "identification_certainty_id",
            "sample_type_id",
            "sample_destination_id",
            "permit_type_id",
            "permit_id",
            "collector_number",
            "barcode_number",
            "identification_comment",
        )


class SaveOCRLocationSerializer(serializers.ModelSerializer):
    region_id = serializers.IntegerField(required=False, allow_null=True)
    district_id = serializers.IntegerField(required=False, allow_null=True)
    occurrence_report_id = serializers.IntegerField(required=True, allow_null=False)
    datum_id = serializers.IntegerField(required=False, allow_null=True)
    coordination_source_id = serializers.IntegerField(required=False, allow_null=True)
    location_accuracy_id = serializers.IntegerField(required=False, allow_null=True)
    # observation_date = serializers.DateTimeField(
    #    format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True
    # )
    has_boundary = serializers.SerializerMethodField()
    has_points = serializers.SerializerMethodField()


    class Meta:
        model = OCRLocation
        fields = (
            "id",
            "occurrence_report_id",
            # "observation_date",
            "location_description",
            "boundary_description",
            "new_occurrence",
            "boundary",
            "mapped_boundary",
            "buffer_radius",
            "datum_id",
            "epsg_code",
            "coordination_source_id",
            "location_accuracy_id",
            "region_id",
            "district_id",
            "locality",
            # 'geojson_polygon',
            "has_boundary",
            "has_points",
        )

    def get_has_boundary(self, obj):
        return obj.occurrence_report.ocr_geometry.annotate(geom_type=GeometryType("geometry")).filter(geom_type="POLYGON").exists()

    def get_has_points(self, obj):
        return obj.occurrence_report.ocr_geometry.annotate(geom_type=GeometryType("geometry")).filter(geom_type="POINT").exists()


class OCRObserverDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OCRObserverDetail
        fields = (
            "id",
            "occurrence_report",
            "observer_name",
            "role",
            "contact",
            "organisation",
            "main_observer",
            "visible",
        )


class OccurrenceReportGeometrySaveSerializer(GeoFeatureModelSerializer):
    occurrence_report_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = OccurrenceReportGeometry
        geo_field = "geometry"
        fields = (
            "id",
            "occurrence_report_id",
            "geometry",
            "original_geometry_ewkb",
            "intersects",
            "drawn_by",
            "locked",
        )
        read_only_fields = ("id",)


class SaveOccurrenceReportSerializer(BaseOccurrenceReportSerializer):
    species_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )
    community_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )
    observation_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True
    )

    class Meta:
        model = OccurrenceReport
        fields = (
            "id",
            "group_type",
            "species_id",
            "community_id",
            "lodgement_date",
            "reported_date",
            "applicant_type",
            "submitter",
            "readonly",
            "can_user_edit",
            "can_user_view",
            "reference",
            "deficiency_data",
            "assessor_data",
            "site",
            "observation_date",
        )
        read_only_fields = ("id",)


class OccurrenceReportUserActionSerializer(serializers.ModelSerializer):
    who = serializers.SerializerMethodField()

    class Meta:
        model = OccurrenceReportUserAction
        fields = "__all__"

    def get_who(self, occurrence_report_user_action):
        email_user = retrieve_email_user(occurrence_report_user_action.who)
        fullname = email_user.get_full_name()
        return fullname


class OccurrenceReportLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = OccurrenceReportLogEntry
        fields = "__all__"
        read_only_fields = ("customer",)

    def get_documents(self, obj):
        return [[d.name, d._file.url] for d in obj.documents.all()]


class OccurrenceReportDocumentSerializer(serializers.ModelSerializer):
    document_category_name = serializers.SerializerMethodField()
    document_sub_category_name = serializers.SerializerMethodField()

    class Meta:
        model = OccurrenceReportDocument
        fields = (
            "id",
            "document_number",
            "occurrence_report",
            "name",
            "_file",
            "description",
            "input_name",
            "uploaded_date",
            "document_category",
            "document_category_name",
            "document_sub_category",
            "document_sub_category_name",
            "visible",
        )
        read_only_fields = ("id", "document_number")

    def get_document_category_name(self, obj):
        if obj.document_category:
            return obj.document_category.document_category_name

    def get_document_sub_category_name(self, obj):
        if obj.document_sub_category:
            return obj.document_sub_category.document_sub_category_name


class SaveOccurrenceReportDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccurrenceReportDocument
        fields = (
            "id",
            "occurrence_report",
            "name",
            "description",
            "input_name",
            "uploaded_date",
            "document_category",
            "document_sub_category",
        )
        read_only_fields = ("id",)

    # override save so we can include our kwargs
    def save(self, *args, **kwargs):
        # if the instance already exists, carry on as normal
        if self.instance:
            return super().save(*args, **kwargs)
        else:
            instance = OccurrenceReportDocument()
            validated_data = self.run_validation(self.initial_data)
            for field_name in self.Meta.fields:
                if (
                    field_name in validated_data
                    and field_name not in self.Meta.read_only_fields
                ):
                    setattr(instance, field_name, validated_data[field_name])
            instance.save(*args, **kwargs)
            return instance


class OccurrenceDocumentSerializer(serializers.ModelSerializer):
    document_category_name = serializers.SerializerMethodField()
    document_sub_category_name = serializers.SerializerMethodField()

    class Meta:
        model = OccurrenceDocument
        fields = (
            "id",
            "document_number",
            "occurrence",
            "name",
            "_file",
            "description",
            "input_name",
            "uploaded_date",
            "document_category",
            "document_category_name",
            "document_sub_category",
            "document_sub_category_name",
            "visible",
        )
        read_only_fields = ("id", "document_number")

    def get_document_category_name(self, obj):
        if obj.document_category:
            return obj.document_category.document_category_name

    def get_document_sub_category_name(self, obj):
        if obj.document_sub_category:
            return obj.document_sub_category.document_sub_category_name


class SaveOccurrenceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccurrenceDocument
        fields = (
            "id",
            "occurrence",
            "name",
            "description",
            "input_name",
            "uploaded_date",
            "document_category",
            "document_sub_category",
        )
        read_only_fields = ("id",)

    # override save so we can include our kwargs
    def save(self, *args, **kwargs):
        # if the instance already exists, carry on as normal
        if self.instance:
            return super().save(*args, **kwargs)
        else:
            instance = OccurrenceDocument()
            validated_data = self.run_validation(self.initial_data)
            for field_name in self.Meta.fields:
                if (
                    field_name in validated_data
                    and field_name not in self.Meta.read_only_fields
                ):
                    setattr(instance, field_name, validated_data[field_name])
            instance.save(*args, **kwargs)
            return instance


class OCRConservationThreatSerializer(serializers.ModelSerializer):
    threat_category = serializers.SerializerMethodField()
    threat_agent = serializers.SerializerMethodField()
    current_impact_name = serializers.SerializerMethodField()
    potential_impact_name = serializers.SerializerMethodField()
    potential_threat_onset_name = serializers.SerializerMethodField()
    # occurrence_report = OccurrenceReportSerializer()

    class Meta:
        model = OCRConservationThreat
        fields = (
            "id",
            "threat_number",
            "threat_category_id",
            "threat_category",
            "threat_agent",
            "threat_agent_id",
            "current_impact",
            "current_impact_name",
            "potential_impact",
            "potential_impact_name",
            "potential_threat_onset",
            "potential_threat_onset_name",
            "comment",
            "date_observed",
            "source",
            "occurrence_report",
            "visible",
        )
        read_only_fields = (
            "id",
            "threat_number",
        )

    def get_threat_category(self, obj):
        if obj.threat_category:
            return obj.threat_category.name

    def get_threat_agent(self, obj):
        if obj.threat_agent:
            return obj.threat_agent.name

    def get_current_impact_name(self, obj):
        if obj.current_impact:
            return obj.current_impact.name

    def get_potential_impact_name(self, obj):
        if obj.potential_impact:
            return obj.potential_impact.name

    def get_potential_threat_onset_name(self, obj):
        if obj.potential_threat_onset:
            return obj.potential_threat_onset.name


class SaveOCRConservationThreatSerializer(serializers.ModelSerializer):

    threat_category_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )
    threat_agent_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )
    date_observed = serializers.DateField(
        format="%Y-%m-%d", required=False, allow_null=True
    )

    class Meta:
        model = OCRConservationThreat
        fields = (
            "id",
            "occurrence_report",
            "threat_category_id",
            "threat_agent_id",
            "comment",
            "current_impact",
            "potential_impact",
            "potential_threat_onset",
            "date_observed",
        )
        read_only_fields = ("id",)

    # override save so we can include our kwargs
    def save(self, *args, **kwargs):
        # if the instance already exists, carry on as normal
        if self.instance:
            return super().save(*args, **kwargs)
        else:
            instance = OCRConservationThreat()
            validated_data = self.run_validation(self.initial_data)
            for field_name in self.Meta.fields:
                if (
                    field_name in validated_data
                    and field_name not in self.Meta.read_only_fields
                ):
                    setattr(instance, field_name, validated_data[field_name])
            instance.save(*args, **kwargs)
            return instance


class OccurrenceReportAmendmentRequestDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccurrenceReportAmendmentRequestDocument
        fields = ("id", "name", "_file")


class OccurrenceReportAmendmentRequestSerializer(serializers.ModelSerializer):
    amendment_request_documents = OccurrenceReportAmendmentRequestDocumentSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = OccurrenceReportAmendmentRequest
        fields = "__all__"


class OCCConservationThreatSerializer(serializers.ModelSerializer):
    threat_category = serializers.SerializerMethodField()
    threat_agent = serializers.SerializerMethodField()
    current_impact_name = serializers.SerializerMethodField()
    potential_impact_name = serializers.SerializerMethodField()
    potential_threat_onset_name = serializers.SerializerMethodField()
    original_report = serializers.SerializerMethodField()
    original_threat = serializers.SerializerMethodField()

    class Meta:
        model = OCCConservationThreat
        fields = (
            "id",
            "threat_number",
            "threat_category_id",
            "threat_category",
            "threat_agent",
            "threat_agent_id",
            "current_impact",
            "current_impact_name",
            "potential_impact",
            "potential_impact_name",
            "potential_threat_onset",
            "potential_threat_onset_name",
            "comment",
            "date_observed",
            "source",
            "occurrence",
            "visible",
            "original_report",
            "original_threat",
        )
        read_only_fields = (
            "id",
            "threat_number",
        )

    def get_threat_category(self, obj):
        if obj.threat_category:
            return obj.threat_category.name

    def get_threat_agent(self, obj):
        if obj.threat_agent:
            return obj.threat_agent.name

    def get_current_impact_name(self, obj):
        if obj.current_impact:
            return obj.current_impact.name

    def get_potential_impact_name(self, obj):
        if obj.potential_impact:
            return obj.potential_impact.name

    def get_potential_threat_onset_name(self, obj):
        if obj.potential_threat_onset:
            return obj.potential_threat_onset.name

    def get_original_report(self, obj):
        if obj.occurrence_report_threat:
            return (
                obj.occurrence_report_threat.occurrence_report.occurrence_report_number
            )

    def get_original_threat(self, obj):
        if obj.occurrence_report_threat:
            return obj.occurrence_report_threat.threat_number


class SaveOCCConservationThreatSerializer(serializers.ModelSerializer):

    threat_category_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )
    threat_agent_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )
    date_observed = serializers.DateField(
        format="%Y-%m-%d", required=False, allow_null=True
    )
    occurrence_report_threat_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )

    class Meta:
        model = OCCConservationThreat
        fields = (
            "id",
            "occurrence",
            "threat_category_id",
            "threat_agent_id",
            "comment",
            "current_impact",
            "potential_impact",
            "potential_threat_onset",
            "date_observed",
            "occurrence_report_threat_id",
        )
        read_only_fields = ("id",)

    # override save so we can include our kwargs
    def save(self, *args, **kwargs):
        # if the instance already exists, carry on as normal
        if self.instance:
            return super().save(*args, **kwargs)
        else:
            instance = OCCConservationThreat()
            validated_data = self.run_validation(self.initial_data)
            for field_name in self.Meta.fields:
                if (
                    field_name in validated_data
                    and field_name not in self.Meta.read_only_fields
                ):
                    setattr(instance, field_name, validated_data[field_name])
            instance.save(*args, **kwargs)
            return instance


class ProposeDeclineSerializer(serializers.Serializer):
    reason = serializers.CharField()


class BackToAssessorSerializer(serializers.Serializer):
    reason = serializers.CharField()


class ProposeApproveSerializer(serializers.Serializer):
    occurrence_id = serializers.IntegerField(allow_null=True)
    new_occurrence_name = serializers.CharField(allow_blank=True)
    effective_from_date = serializers.DateField()
    effective_to_date = serializers.DateField()
    details = serializers.CharField()


class SaveOccurrenceSerializer(serializers.ModelSerializer):
    species_id = serializers.IntegerField(
       required=False, allow_null=True, write_only=True
    )
    community_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )

    class Meta:
        model = Occurrence
        fields = (
            "occurrence_name",
            "wild_status",
            "occurrence_source",
            "comment",
            "species_id",
            "community_id",
            "species",
            "community",
            "can_user_edit",
        )
        read_only_fields = ("id",)


class OCCHabitatCompositionSerializer(serializers.ModelSerializer):

    land_form = serializers.MultipleChoiceField(
        choices=[],
        allow_null=True, allow_blank=True, required=False
    )
    copied_ocr = serializers.SerializerMethodField()

    class Meta:
        model = OCCHabitatComposition
        fields = (
            "id",
            "occurrence_id",
            "copied_ocr",
            "land_form",
            "rock_type_id",
            "loose_rock_percent",
            "soil_type_id",
            "soil_colour_id",
            "soil_condition_id",
            "drainage_id",
            "water_quality",
            "habitat_notes",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["land_form"].choices = OCCHabitatComposition._meta.get_field("land_form").choices

    def get_copied_ocr(self, obj):
        if obj.copied_ocr_habitat_composition:
            return obj.copied_ocr_habitat_composition.occurrence_report.occurrence_report_number

class OCCHabitatConditionSerializer(serializers.ModelSerializer):

    copied_ocr = serializers.SerializerMethodField()

    class Meta:
        model = OCCHabitatCondition
        fields = (
            "id",
            "occurrence_id",
            "copied_ocr",
            "pristine",
            "excellent",
            "very_good",
            "good",
            "degraded",
            "completely_degraded",
        )

    def get_copied_ocr(self, obj):
        if obj.copied_ocr_habitat_condition:
            return obj.copied_ocr_habitat_condition.occurrence_report.occurrence_report_number


class OCCVegetationStructureSerializer(serializers.ModelSerializer):

    copied_ocr = serializers.SerializerMethodField()

    class Meta:
        model = OCCVegetationStructure
        fields = (
            "id",
            "occurrence_id",
            "copied_ocr",
            "free_text_field_one",
            "free_text_field_two",
            "free_text_field_three",
            "free_text_field_four",
        )

    def get_copied_ocr(self, obj):
        if obj.copied_ocr_vegetation_structure:
            return obj.copied_ocr_vegetation_structure.occurrence_report.occurrence_report_number

class SaveOCCVegetationStructureSerializer(serializers.ModelSerializer):
    # write_only removed from below as the serializer will not return that field in serializer.data
    occurrence_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCCVegetationStructure
        fields = (
            "id",
            "occurrence_id",
            "free_text_field_one",
            "free_text_field_two",
            "free_text_field_three",
            "free_text_field_four",
        )


class OCCFireHistorySerializer(serializers.ModelSerializer):
    last_fire_estimate = serializers.DateField(format="%Y-%m")
    copied_ocr = serializers.SerializerMethodField()

    class Meta:
        model = OCCFireHistory
        fields = (
            "id",
            "occurrence_id",
            "copied_ocr",
            "last_fire_estimate",
            "intensity_id",
            "comment",
        )

    def get_copied_ocr(self, obj):
        if obj.copied_ocr_fire_history:
            return obj.copied_ocr_fire_history.occurrence_report.occurrence_report_number

class OCCAssociatedSpeciesSerializer(serializers.ModelSerializer):

    copied_ocr = serializers.SerializerMethodField()

    class Meta:
        model = OCCAssociatedSpecies
        fields = (
            "id",
            "occurrence_id",
            "copied_ocr",
            "comment",
            "related_species",
        )

    def get_copied_ocr(self, obj):
        if obj.copied_ocr_associated_species:
            return obj.copied_ocr_associated_species.occurrence_report.occurrence_report_number

class OCCObservationDetailSerializer(serializers.ModelSerializer):

    copied_ocr = serializers.SerializerMethodField()

    class Meta:
        model = OCCObservationDetail
        fields = (
            "id",
            "occurrence_id",
            "copied_ocr",
            "observation_method_id",
            "area_surveyed",
            "survey_duration",
        )

    def get_copied_ocr(self, obj):
        if obj.copied_ocr_observation_detail:
            return obj.copied_ocr_observation_detail.occurrence_report.occurrence_report_number

class OCCPlantCountSerializer(serializers.ModelSerializer):

    copied_ocr = serializers.SerializerMethodField()

    class Meta:
        model = OCCPlantCount
        fields = (
            "id",
            "occurrence_id",
            "copied_ocr",
            "plant_count_method_id",
            "plant_count_accuracy_id",
            "counted_subject_id",
            "plant_condition_id",
            "estimated_population_area",
            "quadrats_present",
            "quadrats_data_attached",
            "quadrats_surveyed",
            "individual_quadrat_area",
            "total_quadrat_area",
            "flowering_plants_per",
            "clonal_reproduction_present",
            "vegetative_state_present",
            "flower_bud_present",
            "flower_present",
            "immature_fruit_present",
            "ripe_fruit_present",
            "dehisced_fruit_present",
            "pollinator_observation",
            "comment",
            "simple_alive",
            "simple_dead",
            "detailed_alive_mature",
            "detailed_dead_mature",
            "detailed_alive_juvenile",
            "detailed_dead_juvenile",
            "detailed_alive_seedling",
            "detailed_dead_seedling",
            "detailed_alive_unknown",
            "detailed_dead_unknown",
        )

    def get_copied_ocr(self, obj):
        if obj.copied_ocr_plant_count:
            return obj.copied_ocr_plant_count.occurrence_report.occurrence_report_number

class OCCAnimalObservationSerializer(serializers.ModelSerializer):

    primary_detection_method = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    secondary_sign = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    reproductive_maturity = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    copied_ocr = serializers.SerializerMethodField()

    class Meta:
        model = OCCAnimalObservation
        fields = (
            "id",
            "occurrence_id",
            "copied_ocr",
            "primary_detection_method",
            "secondary_sign",
            "reproductive_maturity",
            "animal_health_id",
            "death_reason_id",
            "total_count",
            "distinctive_feature",
            "action_taken",
            "action_required",
            "observation_detail_comment",
            "alive_adult",
            "dead_adult",
            "alive_juvenile",
            "dead_juvenile",
            "alive_pouch_young",
            "dead_pouch_young",
            "alive_unsure",
            "dead_unsure",
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["primary_detection_method"].choices = OCCAnimalObservation._meta.get_field("primary_detection_method").choices
        self.fields["secondary_sign"].choices = OCCAnimalObservation._meta.get_field("secondary_sign").choices
        self.fields["reproductive_maturity"].choices = OCCAnimalObservation._meta.get_field("reproductive_maturity").choices

    def get_copied_ocr(self, obj):
        if obj.copied_ocr_animal_observation:
            return obj.copied_ocr_animal_observation.occurrence_report.occurrence_report_number

class OCCIdentificationSerializer(serializers.ModelSerializer):

    copied_ocr = serializers.SerializerMethodField()

    class Meta:
        model = OCCIdentification
        fields = (
            "id",
            "occurrence_id",
            "copied_ocr",
            "id_confirmed_by",
            "identification_certainty_id",
            "sample_type_id",
            "sample_destination_id",
            "permit_type_id",
            "permit_id",
            "collector_number",
            "barcode_number",
            "identification_comment",
        )

    def get_copied_ocr(self, obj):
        if obj.copied_ocr_identification:
            return obj.copied_ocr_identification.occurrence_report.occurrence_report_number

class OCCObserverDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OCCObserverDetail
        fields = (
            "id",
            "occurrence",
            "observer_name",
            "role",
            "contact",
            "organisation",
            "main_observer",
        )


class SaveOCCHabitatCompositionSerializer(serializers.ModelSerializer):
    # write_only removed from below as the serializer will not return that field in serializer.data
    occurrence_id = serializers.IntegerField(required=False, allow_null=True)
    land_form = serializers.MultipleChoiceField(
        choices=[],
        allow_null=True, allow_blank=True, required=False
    )
    rock_type_id = serializers.IntegerField(required=False, allow_null=True)
    soil_type_id = serializers.IntegerField(required=False, allow_null=True)
    soil_colour_id = serializers.IntegerField(required=False, allow_null=True)
    soil_condition_id = serializers.IntegerField(required=False, allow_null=True)
    drainage_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCCHabitatComposition
        fields = (
            "id",
            "occurrence_id",
            "land_form",
            "rock_type_id",
            "loose_rock_percent",
            "soil_type_id",
            "soil_colour_id",
            "soil_condition_id",
            "drainage_id",
            "water_quality",
            "habitat_notes",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["land_form"].choices = OCCHabitatComposition._meta.get_field("land_form").choices

class SaveOCCHabitatConditionSerializer(serializers.ModelSerializer):
    # occurrence_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    # write_only removed from below as the serializer will not return that field in serializer.data
    occurrence_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCCHabitatCondition
        fields = (
            "id",
            "occurrence_id",
            "pristine",
            "excellent",
            "very_good",
            "good",
            "degraded",
            "completely_degraded",
        )


class SaveOCCFireHistorySerializer(serializers.ModelSerializer):
    # occurrence_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    # write_only removed from below as the serializer will not return that field in serializer.data
    last_fire_estimate = serializers.DateField(
        format="%Y-%m", input_formats=["%Y-%m"], required=False, allow_null=True
    )
    occurrence_id = serializers.IntegerField(required=False, allow_null=True)
    intensity_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCCFireHistory
        fields = (
            "id",
            "occurrence_id",
            "last_fire_estimate",
            "intensity_id",
            "comment",
        )


class SaveOCCAssociatedSpeciesSerializer(serializers.ModelSerializer):
    occurrence_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCCAssociatedSpecies
        fields = (
            "id",
            "occurrence_id",
            "comment",
            "related_species",
        )


class SaveOCCObservationDetailSerializer(serializers.ModelSerializer):
    occurrence_id = serializers.IntegerField(required=False, allow_null=True)
    observation_method_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCCObservationDetail
        fields = (
            "id",
            "occurrence_id",
            "observation_method_id",
            "area_surveyed",
            "survey_duration",
        )


class SaveOCCPlantCountSerializer(serializers.ModelSerializer):
    occurrence_id = serializers.IntegerField(required=False, allow_null=True)
    plant_count_method_id = serializers.IntegerField(required=False, allow_null=True)
    plant_count_accuracy_id = serializers.IntegerField(required=False, allow_null=True)
    counted_subject_id = serializers.IntegerField(required=False, allow_null=True)
    plant_condition_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCCPlantCount
        fields = (
            "id",
            "occurrence_id",
            "plant_count_method_id",
            "plant_count_accuracy_id",
            "counted_subject_id",
            "plant_condition_id",
            "estimated_population_area",
            "quadrats_present",
            "quadrats_data_attached",
            "quadrats_surveyed",
            "individual_quadrat_area",
            "total_quadrat_area",
            "flowering_plants_per",
            "clonal_reproduction_present",
            "vegetative_state_present",
            "flower_bud_present",
            "flower_present",
            "immature_fruit_present",
            "ripe_fruit_present",
            "dehisced_fruit_present",
            "pollinator_observation",
            "comment",
            "simple_alive",
            "simple_dead",
            "detailed_alive_mature",
            "detailed_dead_mature",
            "detailed_alive_juvenile",
            "detailed_dead_juvenile",
            "detailed_alive_seedling",
            "detailed_dead_seedling",
            "detailed_alive_unknown",
            "detailed_dead_unknown",
        )


class SaveOCCAnimalObservationSerializer(serializers.ModelSerializer):
    occurrence_id = serializers.IntegerField(required=False, allow_null=True)
    primary_detection_method = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    secondary_sign = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    reproductive_maturity = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    animal_health_id = serializers.IntegerField(required=False, allow_null=True)
    death_reason_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCCAnimalObservation
        fields = (
            "id",
            "occurrence_id",
            "primary_detection_method",
            "secondary_sign",
            "reproductive_maturity",
            "animal_health_id",
            "death_reason_id",
            "total_count",
            "distinctive_feature",
            "action_taken",
            "action_required",
            "observation_detail_comment",
            "alive_adult",
            "dead_adult",
            "alive_juvenile",
            "dead_juvenile",
            "alive_pouch_young",
            "dead_pouch_young",
            "alive_unsure",
            "dead_unsure",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["primary_detection_method"].choices = OCCAnimalObservation._meta.get_field("primary_detection_method").choices
        self.fields["secondary_sign"].choices = OCCAnimalObservation._meta.get_field("secondary_sign").choices
        self.fields["reproductive_maturity"].choices = OCCAnimalObservation._meta.get_field("reproductive_maturity").choices


class SaveOCCIdentificationSerializer(serializers.ModelSerializer):
    occurrence_id = serializers.IntegerField(required=False, allow_null=True)
    identification_certainty_id = serializers.IntegerField(
        required=False, allow_null=True
    )
    sample_type_id = serializers.IntegerField(required=False, allow_null=True)
    sample_destination_id = serializers.IntegerField(required=False, allow_null=True)
    permit_type_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OCCIdentification
        fields = (
            "id",
            "occurrence_id",
            "id_confirmed_by",
            "identification_certainty_id",
            "sample_type_id",
            "sample_destination_id",
            "permit_type_id",
            "permit_id",
            "collector_number",
            "barcode_number",
            "identification_comment",
        )


class OCCLocationSerializer(serializers.ModelSerializer):
    has_boundary = serializers.SerializerMethodField()
    has_points = serializers.SerializerMethodField()
    copied_ocr = serializers.SerializerMethodField()

    class Meta:
        model = OCCLocation
        fields = (
            "id",
            "occurrence_id",
            "copied_ocr",
            "location_description",
            "boundary_description",
            "boundary",
            "mapped_boundary",
            "buffer_radius",
            "datum_id",
            "epsg_code",
            "coordination_source_id",
            "location_accuracy_id",
            "region_id",
            "district_id",
            "locality",
            "has_boundary",
            "has_points",
        )

    def get_has_boundary(self, obj):
        return obj.occurrence.occ_geometry.annotate(geom_type=GeometryType("geometry")).filter(geom_type="POLYGON").exists()

    def get_has_points(self, obj):
        return obj.occurrence.occ_geometry.annotate(geom_type=GeometryType("geometry")).filter(geom_type="POINT").exists()
    
    def get_copied_ocr(self, obj):
        if obj.copied_ocr_location:
            return obj.copied_ocr_location.occurrence_report.occurrence_report_number

class OccurrenceGeometrySerializer(GeoFeatureModelSerializer):
    occurrence_id = serializers.IntegerField(write_only=True, required=False)
    geometry_source = serializers.SerializerMethodField()
    copied_from = serializers.SerializerMethodField(read_only=True)
    srid = serializers.SerializerMethodField(read_only=True)
    original_geometry = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OccurrenceGeometry
        geo_field = "geometry"
        fields = (
            "id",
            "occurrence_id",
            "geometry",
            "original_geometry",
            "srid",
            "area_sqm",
            "area_sqhm",
            "intersects",
            "geometry_source",
            "locked",
            "copied_from",
        )
        read_only_fields = ("id",)

    def get_srid(self, obj):
        if obj.geometry:
            return obj.geometry.srid
        else:
            return None

    def get_geometry_source(self, obj):
        return get_geometry_source(obj)

    def get_copied_from(self, obj):
        if obj.copied_from:
            return ListOCCMinimalSerializer(
                obj.copied_from.occurrence, context=self.context
            ).data

        return None

    def get_original_geometry(self, obj):
        if obj.original_geometry_ewkb:
            return wkb_to_geojson(obj.original_geometry_ewkb)
        else:
            return None


class ListOCCMinimalSerializer(serializers.ModelSerializer):
    occ_geometry = OccurrenceGeometrySerializer(many=True, read_only=True)
    label = serializers.SerializerMethodField(read_only=True)
    processing_status_display = serializers.CharField(
        read_only=True, source="get_processing_status_display"
    )
    # lodgement_date_display = serializers.DateTimeField(
    #     read_only=True, format="%d/%m/%Y", source="lodgement_date"
    # )
    details_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Occurrence
        fields = (
            "id",
            "label",
            "occurrence_number",
            "processing_status",
            "processing_status_display",
            "occ_geometry",
            # "lodgement_date",
            # "lodgement_date_display",
            "details_url",
        )

    def get_label(self, obj):
        return "Occurrence"

    def get_details_url(self, obj):
        request = self.context["request"]

        if request.user.is_authenticated:
            # TODO: Don't have these url names yet
            if is_internal(request):
                return f"{obj.id}"
                # return reverse(
                #     "internal-occurrence-detail",
                #     kwargs={"occurrence_pk": obj.id},
                # )
            else:
                return None
                # return reverse(
                #     "external-occurrence-detail",
                #     kwargs={"occurrence_pk": obj.id},
                # )

        return None


class SaveOCCLocationSerializer(serializers.ModelSerializer):
    region_id = serializers.IntegerField(required=False, allow_null=True)
    district_id = serializers.IntegerField(required=False, allow_null=True)
    occurrence_id = serializers.IntegerField(required=False, allow_null=True)
    datum_id = serializers.IntegerField(required=False, allow_null=True)
    coordination_source_id = serializers.IntegerField(required=False, allow_null=True)
    location_accuracy_id = serializers.IntegerField(required=False, allow_null=True)
    has_boundary = serializers.SerializerMethodField()
    has_points = serializers.SerializerMethodField()

    class Meta:
        model = OCCLocation
        fields = (
            "id",
            "occurrence_id",
            "location_description",
            "boundary_description",
            "boundary",
            "mapped_boundary",
            "buffer_radius",
            "datum_id",
            "epsg_code",
            "coordination_source_id",
            "location_accuracy_id",
            "region_id",
            "district_id",
            "locality",
            "has_boundary",
            "has_points",
        )

    def get_has_boundary(self, obj):
        return obj.occurrence.occ_geometry.annotate(geom_type=GeometryType("geometry")).filter(geom_type="POLYGON").exists()

    def get_has_points(self, obj):
        return obj.occurrence.occ_geometry.annotate(geom_type=GeometryType("geometry")).filter(geom_type="POINT").exists()

class OccurrenceGeometrySaveSerializer(GeoFeatureModelSerializer):
    occurrence_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = OccurrenceGeometry
        geo_field = "geometry"
        fields = (
            "id",
            "occurrence_id",
            "geometry",
            "original_geometry_ewkb",
            "intersects",
            "drawn_by",
            "locked",
        )
        read_only_fields = ("id",)

class BaseOccurrenceTenureSerializer(serializers.ModelSerializer):
    vesting = serializers.SerializerMethodField()

    class Meta:
        model = OccurrenceTenure
        fields = (
            "__all__"
        )

    def get_vesting(self, obj):
        if obj.vesting:
            return obj.vesting
        return None

class OccurrenceTenureSerializer(BaseOccurrenceTenureSerializer):
    pass

class ListOccurrenceTenureSerializer(BaseOccurrenceTenureSerializer):
    class Meta:
        model = OccurrenceTenure
        fields = (
            "id",
            "status",
            "tenure_area_id",
            "owner_name",
            "owner_count",
            "vesting",
            "purpose",
            "comments",
            "significant_to_occurrence",
        )
        datatables_always_serialize = (
            "id",
            "status",
            "tenure_area_id",
            "owner_name",
            "owner_count",
            "vesting",
            "purpose",
            "comments",
            "significant_to_occurrence",
        )
