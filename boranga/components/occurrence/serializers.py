import json
import logging

from django.urls import reverse
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from boranga.components.conservation_status.models import ConservationStatus
from boranga.components.main.serializers import (
    CommunicationLogEntrySerializer,
    EmailUserSerializer,
)
from boranga.components.main.utils import get_geometry_source
from boranga.components.occurrence.models import (
    AnimalObservation,
    AssociatedSpecies,
    FireHistory,
    HabitatComposition,
    HabitatCondition,
    Identification,
    LandForm,
    Location,
    ObservationDetail,
    ObserverDetail,
    Occurrence,
    OccurrenceDocument,
    OCCConservationThreat,
    OccurrenceLogEntry,
    OccurrenceReport,
    OccurrenceReportAmendmentRequest,
    OccurrenceReportAmendmentRequestDocument,
    OccurrenceReportDocument,
    OccurrenceReportGeometry,
    OccurrenceReportLogEntry,
    OccurrenceReportUserAction,
    OccurrenceUserAction,
    OCRConservationThreat,
    PlantCount,
    PrimaryDetectionMethod,
    ReproductiveMaturity,
    SecondarySign,
)
from boranga.components.species_and_communities.models import CommunityTaxonomy
from boranga.helpers import is_approver, is_assessor, is_internal
from boranga.ledger_api_utils import retrieve_email_user

logger = logging.getLogger("boranga")


class OccurrenceSerializer(serializers.ModelSerializer):
    processing_status_display = serializers.CharField(
        source="get_processing_status_display"
    )
    scientific_name = serializers.CharField(
        source="species.taxonomy.scientific_name", allow_null=True
    )
    group_type = serializers.CharField(source="group_type.name", allow_null=True)

    class Meta:
        model = Occurrence
        fields = "__all__"


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
    internal_user_edit = serializers.SerializerMethodField()
    can_user_assess = serializers.SerializerMethodField()
    occurrence = serializers.IntegerField(source="occurrence.id", allow_null=True)
    occurrence_name = serializers.CharField(
        source="occurrence.occurrence_number", allow_null=True
    )

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
            "internal_user_edit",
            "occurrence",
            "occurrence_name",
            "effective_from",
            "effective_to",
            "review_due_date",
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
            "can_user_assess",
            "internal_user_edit",
        )

    def get_scientific_name(self, obj):
        if obj.species:
            if obj.species.taxonomy:
                return obj.species.taxonomy.scientific_name
        return ""

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

    def get_internal_user_edit(self, obj):
        if obj.can_user_edit:
            if obj.internal_application is True:
                return True
        else:
            return False

    def get_can_user_assess(self, obj):
        request = self.context["request"]
        return (
            is_assessor(request.user)
            and obj.processing_status
            == OccurrenceReport.PROCESSING_STATUS_WITH_ASSESSOR
        )


class HabitatCompositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = HabitatComposition
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
        self.fields["land_form"] = serializers.MultipleChoiceField(
            choices=[
                (land_form_instance.id, land_form_instance.name)
                for land_form_instance in LandForm.objects.all()
            ],
            allow_blank=False,
        )


class HabitatConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = HabitatCondition
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


class FireHistorySerializer(serializers.ModelSerializer):
    last_fire_estimate = serializers.DateField(format="%Y-%m")

    class Meta:
        model = FireHistory
        fields = (
            "id",
            "occurrence_report_id",
            "last_fire_estimate",
            "intensity_id",
            "comment",
        )


class AssociatedSpeciesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssociatedSpecies
        fields = (
            "id",
            "occurrence_report_id",
            "related_species",
        )


class ObservationDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObservationDetail
        fields = (
            "id",
            "occurrence_report_id",
            "observation_method_id",
            "area_surveyed",
            "survey_duration",
        )


class PlantCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlantCount
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


class AnimalObservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnimalObservation
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
        self.fields["primary_detection_method"] = serializers.MultipleChoiceField(
            choices=[
                (primary_det_instance.id, primary_det_instance.name)
                for primary_det_instance in PrimaryDetectionMethod.objects.all()
            ],
            allow_blank=False,
        )
        self.fields["secondary_sign"] = serializers.MultipleChoiceField(
            choices=[
                (sec_sign_instance.id, sec_sign_instance.name)
                for sec_sign_instance in SecondarySign.objects.all()
            ],
            allow_blank=False,
        )
        self.fields["reproductive_maturity"] = serializers.MultipleChoiceField(
            choices=[
                (rep_maturity_instance.id, rep_maturity_instance.name)
                for rep_maturity_instance in ReproductiveMaturity.objects.all()
            ],
            allow_blank=False,
        )


class IdentificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Identification
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


class LocationSerializer(serializers.ModelSerializer):
    observation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # geojson_point = serializers.SerializerMethodField()
    # geojson_polygon = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = (
            "id",
            "occurrence_report_id",
            "observation_date",
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
    geometry_source = serializers.SerializerMethodField()
    report_copied_from = serializers.SerializerMethodField(read_only=True)
    srid = serializers.SerializerMethodField(read_only=True)

    def get_srid(self, obj):
        if obj.geometry:
            return obj.geometry.srid
        else:
            return None

    class Meta:
        model = OccurrenceReportGeometry
        geo_field = "geometry"
        fields = (
            "id",
            "occurrence_report_id",
            "geometry",
            "srid",
            "area_sqm",
            "area_sqhm",
            "intersects",
            "geometry_source",
            "locked",
            "report_copied_from",
        )
        read_only_fields = ("id",)

    def get_geometry_source(self, obj):
        return get_geometry_source(obj)

    def get_report_copied_from(self, obj):
        if obj.copied_from:
            return ListOCRReportMinimalSerializer(
                obj.copied_from.occurrence_report, context=self.context
            ).data

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
    effective_from = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", allow_null=True
    )
    effective_to = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", allow_null=True
    )
    review_due_date = serializers.DateField(format="%Y-%m-%d", allow_null=True)
    can_user_assess = serializers.SerializerMethodField()
    community_number = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    community_migrated_id = serializers.SerializerMethodField()
    conservation_list = serializers.SerializerMethodField()
    conservation_category = serializers.SerializerMethodField()
    wild_status = serializers.CharField(source="wild_status.name", allow_null=True)

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
            "conservation_list",
            "conservation_category",
            "wild_status",
            "group_type",
            "number_of_reports",
            "processing_status",
            "processing_status_display",
            "effective_from",
            "effective_to",
            "review_due_date",
            "can_user_assess",
        )
        datatables_always_serialize = (
            "id",
            "occurrence_number",
            "scientific_name",
            "group_type",
            "number_of_reports",
            "processing_status",
            "processing_status_display",
            "can_user_assess",
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
                conservation_list__applies_to_wa=True,
                processing_status="approved",
            )
            return conservation_status
        except ConservationStatus.DoesNotExist:
            return None

    def get_conservation_list(self, obj):
        if not obj.community:
            return ""

        conservation_status = self.get_conservation_status(obj)

        if not conservation_status:
            return ""

        return conservation_status.conservation_list.code

    def get_conservation_category(self, obj):
        if not obj.community:
            return ""

        conservation_status = self.get_conservation_status(obj)

        if not conservation_status:
            return ""

        return conservation_status.conservation_category.code

    def get_can_user_assess(self, obj):
        request = self.context["request"]
        return (
            is_assessor(request.user)
            and obj.processing_status
            == OccurrenceReport.PROCESSING_STATUS_WITH_ASSESSOR
        )


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
    # label used for new polygon featuretoast on map_component
    label = serializers.SerializerMethodField(read_only=True)
    model_name = serializers.SerializerMethodField(read_only=True)
    occurrence = OccurrenceSerializer(read_only=True, allow_null=True)
    lodgement_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True
    )

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
            # 'list_approval_level',
            "location",
            "habitat_composition",
            "habitat_condition",
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

    # def get_list_approval_level(self,obj):
    #     if obj.conservation_list:
    #         return obj.conservation_list.approval_level
    #     else:
    #         return None

    def get_location(self, obj):
        try:
            qs = Location.objects.get(occurrence_report=obj)
            return LocationSerializer(qs).data
        except Location.DoesNotExist:
            return LocationSerializer().data

    def get_habitat_composition(self, obj):
        try:
            qs = HabitatComposition.objects.get(occurrence_report=obj)
            return HabitatCompositionSerializer(qs).data
        except HabitatComposition.DoesNotExist:
            return HabitatCompositionSerializer().data

    def get_habitat_condition(self, obj):
        try:
            qs = HabitatCondition.objects.get(occurrence_report=obj)
            return HabitatConditionSerializer(qs).data
        except HabitatCondition.DoesNotExist:
            return HabitatConditionSerializer().data

    def get_fire_history(self, obj):
        try:
            qs = FireHistory.objects.get(occurrence_report=obj)
            return FireHistorySerializer(qs).data
        except FireHistory.DoesNotExist:
            return FireHistorySerializer().data

    def get_associated_species(self, obj):
        try:
            qs = AssociatedSpecies.objects.get(occurrence_report=obj)
            return AssociatedSpeciesSerializer(qs).data
        except AssociatedSpecies.DoesNotExist:
            return AssociatedSpeciesSerializer().data

    def get_observation_detail(self, obj):
        try:
            qs = ObservationDetail.objects.get(occurrence_report=obj)
            return ObservationDetailSerializer(qs).data
        except ObservationDetail.DoesNotExist:
            return ObservationDetailSerializer().data

    def get_plant_count(self, obj):
        try:
            qs = PlantCount.objects.get(occurrence_report=obj)
            return PlantCountSerializer(qs).data
        except PlantCount.DoesNotExist:
            return PlantCountSerializer().data

    def get_animal_observation(self, obj):
        try:
            qs = AnimalObservation.objects.get(occurrence_report=obj)
            return AnimalObservationSerializer(qs).data
        except AnimalObservation.DoesNotExist:
            return AnimalObservationSerializer().data

    def get_identification(self, obj):
        try:
            qs = Identification.objects.get(occurrence_report=obj)
            return IdentificationSerializer(qs).data
        except Identification.DoesNotExist:
            return IdentificationSerializer().data

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


class InternalOccurrenceReportSerializer(OccurrenceReportSerializer):
    can_user_approve = serializers.SerializerMethodField()
    can_user_assess = serializers.SerializerMethodField()
    can_user_action = serializers.SerializerMethodField()
    current_assessor = serializers.SerializerMethodField(read_only=True)

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
            "assigned_officer",
        )

    def get_can_user_assess(self, obj):
        request = self.context["request"]
        return (
            is_assessor(request.user)
            and obj.processing_status
            == OccurrenceReport.PROCESSING_STATUS_WITH_ASSESSOR
            and obj.assigned_officer == request.user.id
        )

    def get_can_user_approve(self, obj):
        request = self.context["request"]
        return (
            is_approver(request.user)
            and obj.processing_status == OccurrenceReport.CUSTOMER_STATUS_WITH_APPROVER
            and obj.assigned_approver == request.user.id
        )

    def get_can_user_action(self, obj):
        return self.get_can_user_assess(obj) or self.get_can_user_approve(obj)

    def get_current_assessor(self, obj):
        user = self.context["request"].user
        return {
            "id": user.id,
            "name": user.get_full_name(),
            "email": user.email,
        }


class SaveHabitatCompositionSerializer(serializers.ModelSerializer):
    # write_only removed from below as the serializer will not return that field in serializer.data
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    land_form = serializers.MultipleChoiceField(
        choices=[], allow_null=True, allow_blank=True, required=False
    )
    rock_type_id = serializers.IntegerField(required=False, allow_null=True)
    soil_type_id = serializers.IntegerField(required=False, allow_null=True)
    soil_colour_id = serializers.IntegerField(required=False, allow_null=True)
    soil_condition_id = serializers.IntegerField(required=False, allow_null=True)
    drainage_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = HabitatComposition
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
        self.fields["land_form"].choices = [
            (land_form_instance.id, land_form_instance.name)
            for land_form_instance in LandForm.objects.all()
        ]


class SaveHabitatConditionSerializer(serializers.ModelSerializer):
    # occurrence_report_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    # write_only removed from below as the serializer will not return that field in serializer.data
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = HabitatCondition
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


class SaveFireHistorySerializer(serializers.ModelSerializer):
    # occurrence_report_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    # write_only removed from below as the serializer will not return that field in serializer.data
    last_fire_estimate = serializers.DateField(
        format="%Y-%m", input_formats=["%Y-%m"], required=False, allow_null=True
    )
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    intensity_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = FireHistory
        fields = (
            "id",
            "occurrence_report_id",
            "last_fire_estimate",
            "intensity_id",
            "comment",
        )


class SaveAssociatedSpeciesSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = AssociatedSpecies
        fields = (
            "id",
            "occurrence_report_id",
            "related_species",
        )


class SaveObservationDetailSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    observation_method_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = ObservationDetail
        fields = (
            "id",
            "occurrence_report_id",
            "observation_method_id",
            "area_surveyed",
            "survey_duration",
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


class SaveAnimalObservationSerializer(serializers.ModelSerializer):
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
        model = AnimalObservation
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
        self.fields["primary_detection_method"].choices = [
            (primary_det_instance.id, primary_det_instance.name)
            for primary_det_instance in PrimaryDetectionMethod.objects.all()
        ]
        self.fields["secondary_sign"].choices = [
            (sec_sign_instance.id, sec_sign_instance.name)
            for sec_sign_instance in SecondarySign.objects.all()
        ]
        self.fields["reproductive_maturity"].choices = [
            (rep_maturity_instance.id, rep_maturity_instance.name)
            for rep_maturity_instance in ReproductiveMaturity.objects.all()
        ]


class SaveIdentificationSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=False, allow_null=True)
    identification_certainty_id = serializers.IntegerField(
        required=False, allow_null=True
    )
    sample_type_id = serializers.IntegerField(required=False, allow_null=True)
    sample_destination_id = serializers.IntegerField(required=False, allow_null=True)
    permit_type_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Identification
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


class SaveLocationSerializer(serializers.ModelSerializer):
    occurrence_report_id = serializers.IntegerField(required=True, allow_null=False)
    datum_id = serializers.IntegerField(required=False, allow_null=True)
    coordination_source_id = serializers.IntegerField(required=False, allow_null=True)
    location_accuracy_id = serializers.IntegerField(required=False, allow_null=True)
    observation_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True
    )

    class Meta:
        model = Location
        fields = (
            "id",
            "occurrence_report_id",
            "observation_date",
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
            # 'geojson_polygon',
        )


class ObserverDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObserverDetail
        fields = (
            "id",
            "occurrence_report",
            "observer_name",
            "role",
            "contact",
            "organisation",
            "main_observer",
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
            "intersects",
            "drawn_by",
            "locked",
        )
        read_only_fields = ("id",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.geometry:
            ret["geometry"] = instance.geometry.geojson
        return ret


class SaveOccurrenceReportSerializer(BaseOccurrenceReportSerializer):
    species_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )
    community_id = serializers.IntegerField(
        required=False, allow_null=True, write_only=True
    )
    # conservation_criteria = ConservationCriteriaSerializer(read_only = True)

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

    #override save so we can include our kwargs
    def save(self, *args, **kwargs):
        #if the instance already exists, carry on as normal
        if self.instance:
            return super(SaveOccurrenceReportDocumentSerializer,self).save(*args, **kwargs)
        else:
            instance = OccurrenceReportDocument()
            validated_data = self.run_validation(self.initial_data)
            for field_name in self.Meta.fields:
                if field_name in validated_data and not field_name in self.Meta.read_only_fields:
                    setattr(instance,field_name,validated_data[field_name])            
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

    #override save so we can include our kwargs
    def save(self, *args, **kwargs):
        #if the instance already exists, carry on as normal
        if self.instance:
            return super(SaveOccurrenceDocumentSerializer,self).save(*args, **kwargs)
        else:
            instance = OccurrenceDocument()
            validated_data = self.run_validation(self.initial_data)
            for field_name in self.Meta.fields:
                if field_name in validated_data and not field_name in self.Meta.read_only_fields:
                    setattr(instance,field_name,validated_data[field_name])            
            instance.save(*args, **kwargs)
            return instance


class OCRConservationThreatSerializer(serializers.ModelSerializer):
    threat_category = serializers.SerializerMethodField()
    threat_agent = serializers.SerializerMethodField()
    current_impact_name = serializers.SerializerMethodField()
    potential_impact_name = serializers.SerializerMethodField()
    potential_threat_onset_name = serializers.SerializerMethodField()

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

    #override save so we can include our kwargs
    def save(self, *args, **kwargs):
        #if the instance already exists, carry on as normal
        if self.instance:
            return super(SaveOCRConservationThreatSerializer,self).save(*args, **kwargs)
        else:
            instance = OCRConservationThreat()
            validated_data = self.run_validation(self.initial_data)
            for field_name in self.Meta.fields:
                if field_name in validated_data and not field_name in self.Meta.read_only_fields:
                    setattr(instance,field_name,validated_data[field_name])            
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
        )
        read_only_fields = ("id",)

    #override save so we can include our kwargs
    def save(self, *args, **kwargs):
        #if the instance already exists, carry on as normal
        if self.instance:
            return super(SaveOCCConservationThreatSerializer,self).save(*args, **kwargs)
        else:
            instance = OCCConservationThreat()
            validated_data = self.run_validation(self.initial_data)
            for field_name in self.Meta.fields:
                if field_name in validated_data and not field_name in self.Meta.read_only_fields:
                    setattr(instance,field_name,validated_data[field_name])            
            instance.save(*args, **kwargs)
            return instance

