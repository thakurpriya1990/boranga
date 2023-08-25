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
        self.fields['land_form'] = serializers.MultipleChoiceField(choices=[land_form_instance.id for land_form_instance in LandForm.objects.all()], allow_blank=False)


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


class BaseOccurrenceReportSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    group_type = serializers.SerializerMethodField(read_only=True)
    # group_type_id = serializers.SerializerMethodField(read_only=True)
    allowed_assessors = EmailUserSerializer(many=True)
    # list_approval_level = serializers.SerializerMethodField(read_only=True)
    habitat_composition = serializers.SerializerMethodField()
    habitat_condition = serializers.SerializerMethodField()

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
                'habitat_composition',
                'habitat_condition',
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
    land_form = serializers.MultipleChoiceField(choices=[land_form_instance.id for land_form_instance in LandForm.objects.all()], allow_null=True, allow_blank=True, required=False)
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
