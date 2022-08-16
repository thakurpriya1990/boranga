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
    conservation_status = serializers.SerializerMethodField()
    conservation_list = serializers.SerializerMethodField()
    conservation_category = serializers.SerializerMethodField()
    #conservation_criteria = serializers.SerializerMethodField()
    effective_status_date = serializers.SerializerMethodField()

    class Meta:
        model = ConservationStatus
        fields = (
            'id',
            'conservation_status',
            'conservation_list',
            'conservation_category',
            #'conservation_criteria',
            'effective_status_date',
            )
        datatables_always_serialize = (
            'id',
            'conservation_status',
            'conservation_list',
            'conservation_category',
            #'conservation_criteria',
            'effective_status_date',
			)
        read_only_fields = ('id')

    def get_conservation_status(self,obj):
        if obj.conservation_list:
            return obj.conservation_list.code
        return None

    def get_conservation_list(self,obj):
    	if obj.conservation_list:
    		return obj.conservation_list.code
    	return None

    def get_conservation_category(self,obj):
    	if obj.conservation_category:
    		return obj.conservation_category.code
    	return None

    # def get_conservation_criteria(self,obj):
    # 	if obj.conservation_criteria:
    # 		return obj.conservation_criteria.code
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
            'conservation_status',
            'conservation_list',
            'conservation_category',
            #'conservation_criteria',
            'effective_status_date',
            )


class CommunityConservationStatusSerializer(ConservationStatusSerializer):
    class Meta:
        model = CommunityConservationStatus
        fields = (
            'id',
            'conservation_status_number',
            'community',
            'conservation_status',
            'conservation_list',
            'conservation_category',
            #'conservation_criteria',
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
    conservation_list = serializers.SerializerMethodField()
    conservation_category = serializers.SerializerMethodField()
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
                'conservation_list',
                'conservation_category',
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
                'conservation_list',
                'conservation_category',
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

    def get_conservation_list(self,obj):
        if obj.conservation_list:
            return obj.conservation_list.code
        return ''

    def get_conservation_category(self,obj):
        if obj.conservation_category:
            return obj.conservation_category.code
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
    conservation_list = serializers.SerializerMethodField()
    conservation_category = serializers.SerializerMethodField()
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
                'conservation_list',
                'conservation_category',
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
                'conservation_list',
                'conservation_category',
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

    def get_conservation_list(self,obj):
        if obj.conservation_list:
            return obj.conservation_list.code
        return ''

    def get_conservation_category(self,obj):
        if obj.conservation_category:
            return obj.conservation_category.code
        return ''

    def get_region(self,obj):
        if obj.community.region:
            return obj.community.region.name
        return ''

    def get_district(self,obj):
        if obj.community.district:
            return obj.community.district.name
        return ''