import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.species_and_communities.models import(
    GroupType,
    Species,
    Community,
    Taxonomy
    )
from boranga.components.conservation_status.models import(
    ConservationStatus,
    ConservationStatus,
    ConservationStatusLogEntry,
    ConservationStatusUserAction,
    ConservationCriteria,
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

class ConservationStatusSerializer(serializers.ModelSerializer):
    current_conservation_status = serializers.SerializerMethodField()
    current_conservation_list = serializers.SerializerMethodField()
    current_conservation_category = serializers.SerializerMethodField()
    #current_conservation_criteria = serializers.SerializerMethodField()
    effective_status_date = serializers.SerializerMethodField()

    class Meta:
        model = ConservationStatus
        fields = (
            'id',
            'current_conservation_status',
            'current_conservation_list',
            'current_conservation_category',
            #'current_conservation_criteria',
            'effective_status_date',
            )
        datatables_always_serialize = (
            'id',
            'current_conservation_status',
            'current_conservation_list',
            'current_conservation_category',
            #'current_conservation_criteria',
            'effective_status_date',
			)
        read_only_fields = ('id')

    def get_current_conservation_status(self,obj):
        if obj.current_conservation_list:
            return obj.current_conservation_list.code
        return None

    def get_current_conservation_list(self,obj):
    	if obj.current_conservation_list:
    		return obj.current_conservation_list.code
    	return None

    def get_current_conservation_category(self,obj):
    	if obj.current_conservation_category:
    		return obj.current_conservation_category.code
    	return None

    # def get_current_conservation_criteria(self,obj):
    # 	if obj.current_conservation_criteria:
    # 		return obj.current_conservation_criteria.code
    # 	return None

    def get_effective_status_date(self,obj): #TODO add date in models 
    	return None

class SpeciesConservationStatusSerializer(ConservationStatusSerializer):
    class Meta:
        model = ConservationStatus
        fields = (
            'id',
            'conservation_status_number',
            'species',
            'current_conservation_status',
            'current_conservation_list',
            'current_conservation_category',
            #'current_conservation_criteria',
            'effective_status_date',
            )


class CommunityConservationStatusSerializer(ConservationStatusSerializer):
    class Meta:
        model = ConservationStatus
        fields = (
            'id',
            'conservation_status_number',
            'community',
            'current_conservation_status',
            'current_conservation_list',
            'current_conservation_category',
            #'current_conservation_criteria',
            'effective_status_date',
            )


class ConservationCriteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConservationCriteria
        fields = ('id',
            'code',
            'label'
            )
        read_only_fields = ('id',)


class ListConservationStatusSerializer(serializers.ModelSerializer):
    scientific_name = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    current_conservation_list = serializers.SerializerMethodField()
    current_conservation_category = serializers.SerializerMethodField()
    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'conservation_status_number',
                'group_type',
                'scientific_name',
                'community_name',
                'current_conservation_list',
                'current_conservation_category',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )
        datatables_always_serialize = (
                'id',
                'conservation_status_number',
                'group_type',
                'scientific_name',
                'community_name',
                'current_conservation_list',
                'current_conservation_category',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )   

    def get_scientific_name(self,obj):
        if obj.species:
            return obj.species.scientific_name.name
        return ''

    def get_community_name(self,obj):
        if obj.community:
            if obj.community.community_name:
                return obj.community.community_name.name
            else:
                return ''
        return ''

    def get_current_conservation_list(self,obj):
        if obj.current_conservation_list:
            return obj.current_conservation_list.code
        return ''

    def get_current_conservation_category(self,obj):
        if obj.current_conservation_category:
            return obj.current_conservation_category.code
        return ''


class ListSpeciesConservationStatusSerializer(serializers.ModelSerializer):
    group_type = serializers.SerializerMethodField()
    species_number = serializers.SerializerMethodField()
    scientific_name = serializers.SerializerMethodField()
    common_name = serializers.SerializerMethodField()
    family = serializers.SerializerMethodField()
    genus = serializers.SerializerMethodField()
    phylogenetic_group = serializers.SerializerMethodField()
    current_conservation_list = serializers.SerializerMethodField()
    current_conservation_category = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'conservation_status_number',
                'group_type',
                'species_number',
                'scientific_name',
                'common_name',
                'family',
                'genus',
                'phylogenetic_group',
                'region',
                'district',
                'current_conservation_list',
                'current_conservation_category',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )
        datatables_always_serialize = (
                'id',
                'conservation_status_number',
                'group_type',
                'species_number',
                'scientific_name',
                'common_name',
                'family',
                'genus',
                'phylogenetic_group',
                'region',
                'district',
                'current_conservation_list',
                'current_conservation_category',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )   

    def get_group_type(self,obj):
        return obj.species.group_type.name

    def get_species_number(self,obj):
        if obj.species.species_number:
            return obj.species.species_number
        return ''

    def get_scientific_name(self,obj):
        if obj.species.scientific_name:
            return obj.species.scientific_name.name
        return ''

    def get_common_name(self,obj):
        if obj.species.common_name:
            return obj.species.common_name
        return ''

    def get_family(self,obj):
        try:
            taxonomy = Taxonomy.objects.get(species=obj.species)
            if taxonomy.family:
                return taxonomy.family.name
        except Taxonomy.DoesNotExist:
            return ''

    def get_genus(self,obj):
        try:
            taxonomy = Taxonomy.objects.get(species=obj.species)
            if taxonomy.genus:
                return taxonomy.genus.name
        except Taxonomy.DoesNotExist:
            return ''

    def get_phylogenetic_group(self,obj):
        try:
            taxonomy = Taxonomy.objects.get(species=obj.species)
            if taxonomy.phylogenetic_group:
                return taxonomy.phylogenetic_group.name
        except Taxonomy.DoesNotExist:
            return ''

    def get_current_conservation_list(self,obj):
        if obj.current_conservation_list:
            return obj.current_conservation_list.code
        return ''

    def get_current_conservation_category(self,obj):
        if obj.current_conservation_category:
            return obj.current_conservation_category.code
        return ''

    def get_region(self,obj):
        if obj.species.region:
            return obj.species.region.name
        return ''

    def get_district(self,obj):
        if obj.species.district:
            return obj.species.district.name
        return ''


class ListCommunityConservationStatusSerializer(serializers.ModelSerializer):
    group_type = serializers.SerializerMethodField()
    community_number = serializers.SerializerMethodField()
    community_migrated_id = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()
    community_status = serializers.SerializerMethodField()
    #conservation_status = serializers.SerializerMethodField()
    current_conservation_list = serializers.SerializerMethodField()
    current_conservation_category = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'conservation_status_number',
                'group_type',
                'community_number',
                'community_migrated_id',
                'community_name',
                'community_status',
                #'conservation_status',
                'current_conservation_list',
                'current_conservation_category',
                'region',
                'district',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )
        datatables_always_serialize = (
                'id',
                'conservation_status_number',
                'community_number',
                'group_type',
                'community_migrated_id',
                'community_name',
                'community_status',
                #'conservation_status',
                'current_conservation_list',
                'current_conservation_category',
                'region',
                'district',
                'processing_status',
                'customer_status',
                'can_user_edit',
                'can_user_view',
            )

    def get_group_type(self,obj):
        if obj.community:
            return obj.community.group_type.name
        return ''

    # def get_conservation_status(self,obj):
    #   try:
    #       conservation_status = ConservationStatus.objects.get(community=obj)
    #       return conservation_status.conservation_list.code
    #   except ConservationStatus.DoesNotExist:
    #       return None

    def get_community_number(self,obj):
        if obj.community.community_number:
            return obj.community.community_number
        return ''

    def get_community_migrated_id(self,obj):
        if obj.community.community_migrated_id:
            return obj.community.community_migrated_id
        return ''

    def get_community_name(self,obj):
        if obj.community.community_name:
            return obj.community.community_name.name
        return ''

    def get_community_status(self,obj):
        if obj.community.community_status:
            return obj.community.community_status
        return ''

    def get_current_conservation_list(self,obj):
        if obj.current_conservation_list:
            return obj.current_conservation_list.code
        return ''

    def get_current_conservation_category(self,obj):
        if obj.current_conservation_category:
            return obj.current_conservation_category.code
        return ''

    def get_region(self,obj):
        if obj.community.region:
            return obj.community.region.name
        return ''

    def get_district(self,obj):
        if obj.community.district:
            return obj.community.district.name
        return ''


class BaseConservationStatusSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    group_type = serializers.SerializerMethodField(read_only=True)
    current_conservation_criteria = serializers.SerializerMethodField()
    proposed_conservation_criteria = serializers.SerializerMethodField()
    previous_name = serializers.SerializerMethodField()
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status
    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'group_type',
                'species_id',
                'previous_name',
                'community_id',
                'conservation_status_number',
                'current_conservation_list_id',
                'current_conservation_category_id',
                'current_conservation_criteria',
                'proposed_conservation_list_id',
                'proposed_conservation_category_id',
                'proposed_conservation_criteria',
                'comment',
                'proposed_date',
                'readonly',
                'can_user_edit',
                'lodgement_date',
                )

    def get_readonly(self,obj):
        return False
    
    def get_group_type(self,obj):
        if obj.species:
            return obj.species.group_type.name
        elif obj.community:
            return obj.community.group_type.name
        else:
            return ''

    def get_current_conservation_criteria(self,obj):
        return [c.id for c in obj.current_conservation_criteria.all()]

    def get_proposed_conservation_criteria(self,obj):
        return [p.id for p in obj.proposed_conservation_criteria.all()]

    def get_previous_name(self,obj):
        try:
            taxonomy = Taxonomy.objects.get(species=obj.species)
            if taxonomy.previous_name:
                return taxonomy.previous_name
        except Taxonomy.DoesNotExist:
            return ''
    
    def get_can_user_edit(self,obj):
        return True


class InternalSpeciesConservationStatusSerializer(BaseConservationStatusSerializer):
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status
    submitter = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'group_type',
                'species_id',
                'previous_name',
                'conservation_status_number',
                'current_conservation_list_id',
                'current_conservation_category_id',
                'current_conservation_criteria',
                'proposed_conservation_list_id',
                'proposed_conservation_category_id',
                'proposed_conservation_criteria',
                'comment',
                'proposed_date',
                'readonly',
                'can_user_edit',
                'lodgement_date',
                'submitter',
                )

    def get_submitter(self, obj):
        if obj.submitter:
            email_user = retrieve_email_user(obj.submitter)
            return EmailUserSerializer(email_user).data
        else:
            return None


class SaveSpeciesConservationStatusSerializer(BaseConservationStatusSerializer):
    species_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    current_conservation_list_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    current_conservation_category_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    proposed_conservation_list_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    proposed_conservation_category_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    #current_conservation_criteria = ConservationCriteriaSerializer(read_only = True)

    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'species_id',
                'current_conservation_list_id',
                'current_conservation_category_id',
                'proposed_conservation_list_id',
                'proposed_conservation_category_id',
                'comment',
                'lodgement_date',
                'submitter',
                )
        read_only_fields=('id',)


class CreateSpeciesConservationStatusSerializer(BaseConservationStatusSerializer):
    class Meta:
        model = ConservationStatus
        fields = ('id',
                )
        read_only_fields = (
            'id',
            )


# class BaseCommunityConservationStatusSerializer(serializers.ModelSerializer):
#     readonly = serializers.SerializerMethodField(read_only=True)
#     group_type = serializers.SerializerMethodField(read_only=True)
#     can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status
#     class Meta:
#         model = ConservationStatus
#         fields = (
#                 'id',
#                 'group_type',
#                 'community_id',
#                 'conservation_status_number',
#                 'current_conservation_list_id',
#                 'current_conservation_category_id',
#                 'proposed_conservation_list_id',
#                 'proposed_conservation_category_id',
#                 'comment',
#                 'proposed_date',
#                 'readonly',
#                 'can_user_edit',
#                 )

#     def get_readonly(self,obj):
#         return False
    
#     def get_group_type(self,obj):
#         return obj.community.group_type.name

#     def get_can_user_edit(self,obj):
#         return True


class InternalCommunityConservationStatusSerializer(BaseConservationStatusSerializer):
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status
    submitter = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'group_type',
                'community_id',
                'conservation_status_number',
                'current_conservation_list_id',
                'current_conservation_category_id',
                'current_conservation_criteria',
                'proposed_conservation_list_id',
                'proposed_conservation_category_id',
                'proposed_conservation_criteria',
                'comment',
                'proposed_date',
                'readonly',
                'can_user_edit',
                'lodgement_date',
                'submitter',
                )

    def get_submitter(self, obj):
        if obj.submitter:
            email_user = retrieve_email_user(obj.submitter)
            return EmailUserSerializer(email_user).data
        else:
            return None


class SaveCommunityConservationStatusSerializer(BaseConservationStatusSerializer):
    community_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    current_conservation_list_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    current_conservation_category_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    proposed_conservation_list_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    proposed_conservation_category_id = serializers.IntegerField(required=False, allow_null=True, write_only= True)
    #current_conservation_criteria = ConservationCriteriaSerializer(read_only = True)

    class Meta:
        model = ConservationStatus
        fields = (
                'id',
                'community_id',
                'current_conservation_list_id',
                'current_conservation_category_id',
                'proposed_conservation_list_id',
                'proposed_conservation_category_id',
                'comment',
                'lodgement_date',
                'submitter',
                )
        read_only_fields=('id',)


class ConservationStatusUserActionSerializer(serializers.ModelSerializer):
    who = serializers.CharField(source='who.get_full_name')
    class Meta:
        model = ConservationStatusUserAction
        fields = '__all__'


class ConservationStatusLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = ConservationStatusLogEntry
        fields = "__all__"
        read_only_fields = ("customer",)

    def get_documents(self, obj):
        return [[d.name, d._file.url] for d in obj.documents.all()]
