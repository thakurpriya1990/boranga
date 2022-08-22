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
    SpeciesConservationStatus,
    CommunityConservationStatus,
    )

from boranga.components.users.serializers import UserSerializer
from boranga.components.users.serializers import UserAddressSerializer, DocumentSerializer
from boranga.components.main.serializers import CommunicationLogEntrySerializer
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
        model = SpeciesConservationStatus
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
        model = CommunityConservationStatus
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
        model = SpeciesConservationStatus
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
        model = CommunityConservationStatus
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
            )

    def get_group_type(self,obj):
        if obj.community:
            return obj.community.group_type.name
        return ''

    # def get_conservation_status(self,obj):
    #   try:
    #       conservation_status = CommunityConservationStatus.objects.get(community=obj)
    #       return conservation_status.conservation_list.code
    #   except CommunityConservationStatus.DoesNotExist:
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


class BaseSpeciesConservationStatusSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    group_type = serializers.SerializerMethodField(read_only=True)
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status
    class Meta:
        model = SpeciesConservationStatus
        fields = (
                'id',
                'group_type',
                'species_id',
                'conservation_status_number',
                'current_conservation_list',
                'current_conservation_category',
                'proposed_conservation_list',
                'proposed_conservation_category',
                'comment',
                'proposed_date',
                'readonly',
                'can_user_edit',
                )

    def get_readonly(self,obj):
        return False
    
    def get_group_type(self,obj):
        return obj.species.group_type.name

    def get_can_user_edit(self,obj):
        return True


class InternalSpeciesConservationStatusSerializer(BaseSpeciesConservationStatusSerializer):
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status


class BaseCommunityConservationStatusSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    group_type = serializers.SerializerMethodField(read_only=True)
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status
    class Meta:
        model = CommunityConservationStatus
        fields = (
                'id',
                'group_type',
                'community_id',
                'conservation_status_number',
                'current_conservation_list',
                'current_conservation_category',
                'proposed_conservation_list',
                'proposed_conservation_category',
                'comment',
                'proposed_date',
                'readonly',
                'can_user_edit',
                )

    def get_readonly(self,obj):
        return False
    
    def get_group_type(self,obj):
        return obj.community.group_type.name

    def get_can_user_edit(self,obj):
        return True


class InternalCommunityConservationStatusSerializer(BaseCommunityConservationStatusSerializer):
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status
