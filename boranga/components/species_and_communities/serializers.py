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
	SpeciesDocument,
	SpeciesDistribution,
	CommunityDistribution,
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


class TaxonomySerializer(serializers.ModelSerializer):
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
			'name_authority_id',
			)

class SaveTaxonomySerializer(serializers.ModelSerializer):
	name_authority_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
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
			'name_authority_id',
			)


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

class SpeciesDistributionSerializer(serializers.ModelSerializer):
	class Meta:
		model = SpeciesDistribution
		fields = (
			'department_file_numbers',
			'number_of_occurrences',
			'extent_of_occurrences',
			'area_of_occupancy',
			'number_of_iucn_locations',
			)


class BaseSpeciesSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    group_type = serializers.SerializerMethodField(read_only=True)
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
			    'region_id',
			    'district_id',
			    'conservation_status_id',
			    'conservation_status',
			    'processing_status',
			    'readonly',
			    'can_user_edit',
			    'taxonomy_details',
			    'conservation_attributes',
			    'distribution',
			    'last_data_curration_date',

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
    	#return [ConservationStatusSerializer(qs).data] # this array was used for dashboard on profile page
    	return ConservationStatusSerializer(qs).data

    def get_can_user_edit(self,obj):
    	return True

    def get_conservation_attributes(self,obj):
    	qs = ConservationAttributes.objects.get(species=obj)
    	return ConservationAttributesSerializer(qs).data

    def get_distribution(self,obj):
    	try:
    	    qs = SpeciesDistribution.objects.get(species=obj)
    	except:
            qs = None
    	return SpeciesDistributionSerializer(qs).data


class InternalSpeciesSerializer(BaseSpeciesSerializer):
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status


class CommunityDistributionSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommunityDistribution
		fields = (
			'community_original_area',
			'community_original_area_accuracy',
			'community_original_area_reference',
			)


class BaseCommunitySerializer(serializers.ModelSerializer):
	group_type = serializers.SerializerMethodField(read_only=True)
	conservation_status = serializers.SerializerMethodField()
	distribution = serializers.SerializerMethodField()
	readonly = serializers.SerializerMethodField(read_only=True)
	last_data_curration_date = serializers.DateField(required=False,allow_null=True)
	can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status

	class Meta:
		model = Community
		fields = (
        	    'id',
			    'group_type',
			    'community_id',
			    'community_name',
			    'community_description',
			    'community_status',
			    'region_id',
			    'district_id',
			    'conservation_status_id',
			    'conservation_status',
			    'distribution',
			    'readonly',
			    'can_user_edit',
			    'last_data_curration_date',

                # tab field models
                )

	def get_readonly(self,obj):
		return False

	def get_group_type(self,obj):
		return obj.group_type.name

	def get_conservation_status(self,obj):
		qs = ConservationStatus.objects.get(conservation_list=obj.conservation_status)
		#return [ConservationStatusSerializer(qs).data] # this array was used for dashboard on profile page
		return ConservationStatusSerializer(qs).data

	def get_distribution(self,obj):
		try:
			qs = CommunityDistribution.objects.get(community=obj)
		except:
			qs = None
		return CommunityDistributionSerializer(qs).data

	def get_can_user_edit(self,obj):
		return True


class InternalCommunitySerializer(BaseCommunitySerializer):
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status



class SaveSpeciesSerializer(BaseSpeciesSerializer):
    region_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
    district_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
    class Meta:
        model = Species
        fields = ('id',
			    'group_type',
			    'scientific_name',
			    'common_name',
			    'region_id',
			    'district_id',
			    'processing_status',
			    'last_data_curration_date',
			    'readonly',
			    'can_user_edit',
			    )
        read_only_fields=('id','group_type')


class SaveCommunitySerializer(BaseCommunitySerializer):
    region_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
    district_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
    class Meta:
        model = Community
        fields = ('id',
			    'group_type',
			    'community_id',
			    'community_name',
			    'community_status',
			    'region_id',
			    'district_id',
			    'last_data_curration_date',
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


class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = SpeciesDocument
		fields = ('id','name','_file')


class SpeciesDocumentSerializer(serializers.ModelSerializer):
	document_category_name = serializers.SerializerMethodField()
	class Meta:
		model = SpeciesDocument
		fields = (
			'id',
			'species',
			'name',
			'_file',
			'description',
			'input_name',
			'uploaded_date',
			'document_category',
			'document_category_name',
			'visible',
		)
		read_only_fields = ('id','document_category_name')

	def get_document_category_name(self,obj):
		if obj.document_category:
			return obj.document_category.name


class SaveSpeciesDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = SpeciesDocument
		fields = (
			'id',
			'species',
			'name',
			'description',
			'input_name',
			'uploaded_date',
			'document_category',
			)



