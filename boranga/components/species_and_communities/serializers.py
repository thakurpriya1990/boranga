import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.species_and_communities.models import(
	GroupType,
	Species,
	Community,
	ConservationList,
	ConservationStatus,
	ConservationCategory,
	ConservationCriteria,
	Taxonomy,
	NameAuthority,
	ConservationAttributes,
	Distribution,
	)

from boranga.components.users.serializers import UserSerializer
from boranga.components.users.serializers import UserAddressSerializer, DocumentSerializer
from rest_framework import serializers
from django.db.models import Q

logger = logging.getLogger('boranga')

class ListSpeciesSerializer(serializers.ModelSerializer):
	group_type = serializers.SerializerMethodField()
	family = serializers.SerializerMethodField()
	genus = serializers.SerializerMethodField()
	phylogenetic_group = serializers.SerializerMethodField()
	conservation_status = serializers.SerializerMethodField()
	conservation_list = serializers.SerializerMethodField()
	conservation_category = serializers.SerializerMethodField()
	region = serializers.SerializerMethodField()
	district = serializers.SerializerMethodField()
	class Meta:
		model = Species
		fields = (
			    'id',
			    'group_type',
			    'scientific_name',
			    'common_name',
			    'taxonomy',
			    'family',
			    'genus',
			    'phylogenetic_group',
			    'region',
			    'district',
			    'conservation_status',
			    'conservation_list',
			    'conservation_category',
			    'processing_status',
			)
		datatables_always_serialize = (
                'id',
                'group_type',
			    'scientific_name',
			    'common_name',
			    'taxonomy',
			    'family',
			    'genus',
			    'phylogenetic_group',
			    'region',
			    'district',
			    'conservation_status',
			    'conservation_list',
			    'conservation_category',
			    'processing_status',
			)	

	def get_group_type(self,obj):
		return obj.group_type.name

	def get_family(self,obj):
		if obj.taxonomy:
			return obj.taxonomy.family
		return None

	def get_genus(self,obj):
		if obj.taxonomy:
			return obj.taxonomy.genus
		return None

	def get_phylogenetic_group(self,obj):
		if obj.taxonomy:
			return obj.taxonomy.phylogenetic_group
		return None

	def get_conservation_status(self,obj):
		if obj.conservation_status:
			return obj.conservation_status.conservation_list.code
		return None

	def get_conservation_list(self,obj):
		if obj.conservation_status:
			return obj.conservation_status.conservation_list.code
		return None

	def get_conservation_category(self,obj):
		if obj.conservation_status:
			return obj.conservation_status.conservation_category.code
		return None

	def get_region(self,obj):
		if obj.region:
			return obj.region.name
		return None

	def get_district(self,obj):
		if obj.district:
			return obj.district.name
		return None

class ListCommunitiesSerializer(serializers.ModelSerializer):
	group_type = serializers.SerializerMethodField()
	conservation_status = serializers.SerializerMethodField()
	conservation_list = serializers.SerializerMethodField()
	conservation_category = serializers.SerializerMethodField()
	region = serializers.SerializerMethodField()
	district = serializers.SerializerMethodField()
	class Meta:
		model = Community
		fields = (
			    'id',
			    'group_type',
			    'community_id',
			    'community_name',
			    'community_status',
			    'conservation_status',
			    'conservation_list',
			    'conservation_category',
			    'region',
			    'district',
			)
		datatables_always_serialize = (
                'id',
                'group_type',
			    'community_id',
			    'community_name',
			    'community_status',
			    'conservation_status',
			    'conservation_list',
			    'conservation_category',
			    'region',
			    'district',
			)

	def get_group_type(self,obj):
		return obj.group_type.name

	def get_conservation_status(self,obj):
		if obj.conservation_status:
			return obj.conservation_status.conservation_list.code
		return None

	def get_conservation_list(self,obj):
		if obj.conservation_status:
			return obj.conservation_status.conservation_list.code
		return None

	def get_conservation_category(self,obj):
		if obj.conservation_status:
			return obj.conservation_status.conservation_category.code
		return None

	def get_region(self,obj):
		if obj.region:
			return obj.region.name
		return None

	def get_district(self,obj):
		if obj.district:
			return obj.district.name
		return None


class NameAuthoritySerializer(serializers.ModelSerializer):
	class Meta:
		model = NameAuthority
		fields = (
			'id',
			'name',
			)


class TaxonomySerializer(serializers.ModelSerializer):
	name_authority_details = serializers.SerializerMethodField()
	class Meta:
		model = Taxonomy
		fields = (
			'id',
			'taxon_id',
			'taxon',
			'previous_name',
			'family',
			'genus',
			'phylogenetic_group',
			'name_authority_details',
			)

	def get_name_authority_details(self,obj):
		if obj.name_authority:
			qs = NameAuthority.objects.get(id = obj.name_authority_id)
			return NameAuthoritySerializer(qs).data


class ConservationAttributesSerializer(serializers.ModelSerializer):
	class Meta:
		model = ConservationAttributes
		fields = (
			'species_id',
			'general_management_advice',
			'ecological_attributes',
			'biological_attributes',
			'specific_survey_advice',
			'comments',
			)

class DistributionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Distribution
		fields = (
			'species_id',
			'department_file_numbers',
			'community_original_area',
			'community_original_area_accuracy',
			'number_of_occurrences',
			'extent_of_occurrences',
			'area_of_occupancy',
			'number_of_iucn_locations',
			)


class BaseSpeciesSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    group_type = serializers.SerializerMethodField(read_only=True)
    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    conservation_status = serializers.SerializerMethodField()
    taxonomy_details = serializers.SerializerMethodField()
    conservation_attributes = serializers.SerializerMethodField()
    distribution = serializers.SerializerMethodField()
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status
	
    class Meta:
        model = Species
        fields = (
                'id',
			    'group_type',
			    'scientific_name',
			    'common_name',
			    'taxonomy_id',
			    'region',
			    'district',
			    'conservation_status_id',
			    'conservation_status',
			    'processing_status',
			    'readonly',
			    'can_user_edit',
			    'taxonomy_details',
			    'conservation_attributes',
			    'distribution',

                # tab field models
                )
    
    def get_readonly(self,obj):
        return False

    def get_group_type(self,obj):
        return obj.group_type.name

    def get_taxonomy_details(self,obj):
    	if obj.taxonomy:
    		qs=Taxonomy.objects.get(id=obj.taxonomy_id)
    		return TaxonomySerializer(qs).data

    def get_conservation_status(self,obj):
    	qs = ConservationStatus.objects.get(conservation_list=obj.conservation_status)
    	return [ConservationStatusSerializer(qs).data]

    def get_region(self,obj):
    	if obj.region:
    		return obj.region.name
    	return None

    def get_district(self,obj):
    	if obj.district:
    		return obj.district.name
    	return None

    def get_can_user_edit(self,obj):
    	return True

    def get_conservation_attributes(self,obj):
    	qs = ConservationAttributes.objects.get(species=obj)
    	return ConservationAttributesSerializer(qs).data

    def get_distribution(self,obj):
    	qs = Distribution.objects.get(species=obj)
    	return DistributionSerializer(qs).data


class InternalSpeciesSerializer(BaseSpeciesSerializer):
    region = serializers.CharField(source='region.name', read_only=True)
    district = serializers.CharField(source='district.name', read_only=True)
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status


class BaseCommunitySerializer(serializers.ModelSerializer):
	group_type = serializers.SerializerMethodField(read_only=True)
	region = serializers.SerializerMethodField()
	district = serializers.SerializerMethodField()
	conservation_status = serializers.SerializerMethodField()
	readonly = serializers.SerializerMethodField(read_only=True)
	can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status

	class Meta:
		model = Community
		fields = (
        	    'id',
			    'group_type',
			    'community_id',
			    'community_name',
			    'community_status',
			    'region',
			    'district',
			    'conservation_status_id',
			    'conservation_status',
			    'readonly',
			    'can_user_edit',

                # tab field models
                )

	def get_readonly(self,obj):
		return False

	def get_group_type(self,obj):
		return obj.group_type.name

	def get_conservation_status(self,obj):
		qs = ConservationStatus.objects.get(conservation_list=obj.conservation_status)
		return [ConservationStatusSerializer(qs).data]

	def get_region(self,obj):
		if obj.region:
			return obj.region.name
		return None

	def get_district(self,obj):
		if obj.district:
			return obj.district.name
		return None

	def get_can_user_edit(self,obj):
		return True


class InternalCommunitySerializer(BaseCommunitySerializer):
    region = serializers.CharField(source='region.name', read_only=True)
    district = serializers.CharField(source='district.name', read_only=True)
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status



class SaveSpeciesSerializer(BaseSpeciesSerializer):
    region = serializers.CharField(source='region.name', read_only=True)
    district = serializers.CharField(source='district.name', read_only=True)
    class Meta:
        model = Species
        fields = ('id',
			    'group_type',
			    'scientific_name',
			    'common_name',
			    'processing_status',
			    'readonly',
			    'can_user_edit',
			    )
        read_only_fields=('id','group_type')


class SaveCommunitySerializer(BaseCommunitySerializer):
    region = serializers.CharField(source='region.name', read_only=True)
    district = serializers.CharField(source='district.name', read_only=True)
    class Meta:
        model = Community
        fields = ('id',
			    'group_type',
			    'community_id',
			    'community_name',
			    'community_status',
			    'readonly',
			    'can_user_edit',
			    )
        read_only_fields=('id','group_type')


class ConservationStatusSerializer(serializers.ModelSerializer):
    conservation_status = serializers.SerializerMethodField()
    conservation_list = serializers.SerializerMethodField()
    conservation_category = serializers.SerializerMethodField()
    conservation_criteria = serializers.SerializerMethodField()
    effective_status_date = serializers.SerializerMethodField()

    class Meta:
        model = ConservationStatus
        fields = (
            'conservation_list_id',
            'conservation_status',
            'conservation_list',
            'conservation_category',
            'conservation_criteria',
            'effective_status_date',
            )
        datatables_always_serialize = (
            'conservation_list_id',
            'conservation_status',
            'conservation_list',
            'conservation_category',
            'conservation_criteria',
            'effective_status_date',
			)
        #read_only_fields = ('conservation_list')

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

    def get_conservation_criteria(self,obj):
    	if obj.conservation_criteria:
    		return obj.conservation_criteria.code
    	return None

    def get_effective_status_date(self,obj): #TODO add date in models 
    	return None

