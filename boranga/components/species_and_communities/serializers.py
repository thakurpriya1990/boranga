import logging

from django.conf import settings
from ledger_api_client.ledger_models import EmailUserRO as EmailUser, Address
from boranga.components.species_and_communities.models import(
	GroupType,
	Species,
	SpeciesLogEntry,
	Community,
	Taxonomy,
	NameAuthority,
	SpeciesConservationAttributes,
	CommunityConservationAttributes,
	SpeciesDocument,
	CommunityDocument,
	SpeciesDistribution,
	CommunityDistribution,
	ConservationThreat,
	)
from boranga.components.conservation_status.models import(
    SpeciesConservationStatus,
    CommunityConservationStatus,
    )
from boranga.components.conservation_status.serializers import(
    SpeciesConservationStatusSerializer,
    CommunityConservationStatusSerializer,
    )

from boranga.components.users.serializers import UserSerializer
from boranga.components.users.serializers import UserAddressSerializer, DocumentSerializer
from boranga.components.main.serializers import CommunicationLogEntrySerializer
from rest_framework import serializers
from django.db.models import Q

logger = logging.getLogger('boranga')

class ListSpeciesSerializer(serializers.ModelSerializer):
	group_type = serializers.SerializerMethodField()
	family = serializers.SerializerMethodField()
	genus = serializers.SerializerMethodField()
	phylogenetic_group = serializers.SerializerMethodField()
	#conservation_status = serializers.SerializerMethodField()
	conservation_list = serializers.SerializerMethodField()
	conservation_category = serializers.SerializerMethodField()
	region = serializers.SerializerMethodField()
	district = serializers.SerializerMethodField()
	class Meta:
		model = Species
		fields = (
			    'id',
			    'species_number',
			    'group_type',
			    'scientific_name',
			    'common_name',
			    'family',
			    'genus',
			    'phylogenetic_group',
			    'region',
			    'district',
			    #'conservation_status',
			    'conservation_list',
			    'conservation_category',
			    'processing_status',
			)
		datatables_always_serialize = (
                'id',
                'species_number',
                'group_type',
			    'scientific_name',
			    'common_name',
			    'family',
			    'genus',
			    'phylogenetic_group',
			    'region',
			    'district',
			    #'conservation_status',
			    'conservation_list',
			    'conservation_category',
			    'processing_status',
			)	

	def get_group_type(self,obj):
		return obj.group_type.name

	def get_family(self,obj):
		try:
			taxonomy = Taxonomy.objects.get(species=obj)
			if taxonomy.family:
				return taxonomy.family.name
		except Taxonomy.DoesNotExist:
			return ''

	def get_genus(self,obj):
		try:
			taxonomy = Taxonomy.objects.get(species=obj)
			if taxonomy.genus:
				return taxonomy.genus.name
		except Taxonomy.DoesNotExist:
			return ''

	def get_phylogenetic_group(self,obj):
		try:
			taxonomy = Taxonomy.objects.get(species=obj)
			if taxonomy.phylogenetic_group:
				return taxonomy.phylogenetic_group.name
		except Taxonomy.DoesNotExist:
			return ''

	# def get_conservation_status(self,obj):
	# 	try:
	# 		conservation_status = SpeciesConservationStatus.objects.get(species=obj)
	# 		return conservation_status.conservation_list.code
	# 	except SpeciesConservationStatus.DoesNotExist:
	# 		return None

	def get_conservation_list(self,obj):
		try:
			# need to show only WA_list species
			conservation_status = SpeciesConservationStatus.objects.get(species=obj ,conservation_list__applies_to_wa=True) # need to show only WA_list species
			return conservation_status.conservation_list.code
		except SpeciesConservationStatus.DoesNotExist:
			return ''

	def get_conservation_category(self,obj):
		try:
			# need to show only WA_list species
			conservation_status = SpeciesConservationStatus.objects.get(species=obj, conservation_list__applies_to_wa=True)
			return conservation_status.conservation_category.code
		except SpeciesConservationStatus.DoesNotExist:
			return ''

	def get_region(self,obj):
		if obj.region:
			return obj.region.name
		return ''

	def get_district(self,obj):
		if obj.district:
			return obj.district.name
		return ''

class ListCommunitiesSerializer(serializers.ModelSerializer):
	group_type = serializers.SerializerMethodField()
	#conservation_status = serializers.SerializerMethodField()
	conservation_list = serializers.SerializerMethodField()
	conservation_category = serializers.SerializerMethodField()
	region = serializers.SerializerMethodField()
	district = serializers.SerializerMethodField()
	class Meta:
		model = Community
		fields = (
			    'id',
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
		datatables_always_serialize = (
                'id',
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
		return obj.group_type.name

	# def get_conservation_status(self,obj):
	# 	try:
	# 		conservation_status = CommunityConservationStatus.objects.get(community=obj)
	# 		return conservation_status.conservation_list.code
	# 	except CommunityConservationStatus.DoesNotExist:
	# 		return None

	def get_conservation_list(self,obj):
		try:
			conservation_status = CommunityConservationStatus.objects.get(community=obj) # TODO need to show only WA_list species
			return conservation_status.conservation_list.code
		except CommunityConservationStatus.DoesNotExist:
			return ''

	def get_conservation_category(self,obj):
		try:
			conservation_status = CommunityConservationStatus.objects.get(community=obj)
			return conservation_status.conservation_category.code
		except CommunityConservationStatus.DoesNotExist:
			return ''

	def get_region(self,obj):
		if obj.region:
			return obj.region.name
		return ''

	def get_district(self,obj):
		if obj.district:
			return obj.district.name
		return ''


class TaxonomySerializer(serializers.ModelSerializer):
	class Meta:
		model = Taxonomy
		fields = (
			'id',
			'species_id',
			'taxon_id',
			'taxon',
			'previous_name',
			'family_id',
			'genus_id',
			'phylogenetic_group_id',
			'name_authority_id',
			'name_comments',
			)

class SaveTaxonomySerializer(serializers.ModelSerializer):
	species_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	name_authority_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	family_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	genus_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	phylogenetic_group_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	class Meta:
		model = Taxonomy
		fields = (
			'id',
			'species_id',
			'taxon_id',
			'taxon',
			'previous_name',
			'family_id',
			'genus_id',
			'phylogenetic_group_id',
			'name_authority_id',
			'name_comments',
			)
 

class SpeciesConservationAttributesSerializer(serializers.ModelSerializer):
	class Meta:
		model = SpeciesConservationAttributes
		fields = (
			'id',
			'species_id',
			#flora related attributes
			'flowering_period_id',
			'fruiting_period_id',
			'flora_recruitment_type_id',
			'seed_viability_germination_info_id',
			'root_morphology_id',
			'pollinator_information_id',
			'hydrology',
			'response_to_dieback',
			# fauna related attributes
			'breeding_period_id',
			'fauna_breeding_id',
			'fauna_reproductive_capacity',
			'diet_and_food_source',
			'home_range',
			# common attributes
			'habitat_growth_form',
			'time_to_maturity',
			'generation_length',
			'average_lifespan',
			'minimum_fire_interval',
			'response_to_fire',
			'post_fire_habitat_interaction_id',
			'response_to_disturbance',
			'habitat',
			'research_requirements',
			'other_relevant_diseases',
			)


class SaveSpeciesConservationAttributesSerializer(serializers.ModelSerializer):
	species_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	flowering_period_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	fruiting_period_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	flora_recruitment_type_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	seed_viability_germination_info_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	root_morphology_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	pollinator_information_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	breeding_period_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	fauna_breeding_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	post_fire_habitat_interaction_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	class Meta:
		model = SpeciesConservationAttributes
		fields = (
			'id',
			'species_id',
			#flora related attributes
			'flowering_period_id',
			'fruiting_period_id',
			'flora_recruitment_type_id',
			'seed_viability_germination_info_id',
			'root_morphology_id',
			'pollinator_information_id',
			'hydrology',
			'response_to_dieback',
			# fauna related attributes
			'breeding_period_id',
			'fauna_breeding_id',
			'fauna_reproductive_capacity',
			'diet_and_food_source',
			'home_range',
			# common attributes
			'habitat_growth_form',
			'time_to_maturity',
			'generation_length',
			'average_lifespan',
			'minimum_fire_interval',
			'response_to_fire',
			'post_fire_habitat_interaction_id',
			'response_to_disturbance',
			'habitat',
			'research_requirements',
			'other_relevant_diseases',
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


class SaveSpeciesDistributionSerializer(serializers.ModelSerializer):
	species_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	class Meta:
		model = SpeciesDistribution
		fields = (
			'species_id',
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
                'species_number',
			    'group_type',
			    'scientific_name',
			    'common_name',
			    'region_id',
			    'district_id',
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
    	try:
    		qs = Taxonomy.objects.get(species=obj)
    		return TaxonomySerializer(qs).data
    	except Taxonomy.DoesNotExist:
    		return TaxonomySerializer().data

    def get_conservation_status(self,obj):
        try:
        	qs = SpeciesConservationStatus.objects.get(species=obj , conservation_list__applies_to_wa=True)
        	return SpeciesConservationStatusSerializer(qs).data
        except SpeciesConservationStatus.DoesNotExist:
        	return SpeciesConservationStatusSerializer().data
        	#return [SpeciesConservationStatusSerializer(qs).data] # this array was used for dashboard on profile page

    def get_can_user_edit(self,obj):
    	return True

    def get_conservation_attributes(self,obj):
        try:
            qs = SpeciesConservationAttributes.objects.get(species=obj)
            return SpeciesConservationAttributesSerializer(qs).data
        except SpeciesConservationAttributes.DoesNotExist:
            return SpeciesConservationAttributesSerializer().data

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


class SaveCommunityDistributionSerializer(serializers.ModelSerializer): 
	community_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	class Meta:
		model = CommunityDistribution
		fields = (
			'community_id',
			'community_original_area',
			'community_original_area_accuracy',
			'community_original_area_reference',
			)


class SpeciesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Species
		fields = ('id','scientific_name',)


class CommunityConservationAttributesSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommunityConservationAttributes
		fields = (
			'id',
			'community_id',
			'habitat_growth_form',
			'pollinator_information_id',
			'minimum_fire_interval',
			'response_to_fire',
			'post_fire_habitat_interaction_id',
			'hydrology',
			'ecological_and_biological_information',
			'research_requirements',
			'response_to_dieback',
			'other_relevant_diseases',
			)


class SaveCommunityConservationAttributesSerializer(serializers.ModelSerializer):
	community_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	pollinator_information_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	post_fire_habitat_interaction_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
	class Meta:
		model = CommunityConservationAttributes
		fields = (
			'id',
			'community_id',
			'habitat_growth_form',
			'pollinator_information_id',
			'minimum_fire_interval',
			'response_to_fire',
			'post_fire_habitat_interaction_id',
			'hydrology',
			'ecological_and_biological_information',
			'research_requirements',
			'response_to_dieback',
			'other_relevant_diseases',
			)


class BaseCommunitySerializer(serializers.ModelSerializer):
	species = serializers.SerializerMethodField()
	group_type = serializers.SerializerMethodField(read_only=True)
	conservation_status = serializers.SerializerMethodField()
	distribution = serializers.SerializerMethodField()
	conservation_attributes = serializers.SerializerMethodField()
	readonly = serializers.SerializerMethodField(read_only=True)
	last_data_curration_date = serializers.DateField(required=False,allow_null=True)
	can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Species model depending on customer status

	class Meta:
		model = Community
		fields = (
        	    'id',
        	    'community_number',
        	    'species',
			    'group_type',
			    'community_migrated_id',
			    'community_name',
			    'community_description',
			    'previous_name',
			    'name_authority_id',
			    'name_comments',
			    'community_status',
			    'region_id',
			    'district_id',
			    'conservation_status',
			    'distribution',
			    'conservation_attributes',
			    'readonly',
			    'can_user_edit',
			    'last_data_curration_date',

                # tab field models
                )

	def get_species(self,obj):
		return [s.id for s in obj.species.all()]
	
	def get_readonly(self,obj):
		return False

	def get_group_type(self,obj):
		return obj.group_type.name

	def get_conservation_status(self,obj):
		try:
			qs = CommunityConservationStatus.objects.get(community=obj , conservation_list__applies_to_wa=True)
			return CommunityConservationStatusSerializer(qs).data
		except CommunityConservationStatus.DoesNotExist:
			return CommunityConservationStatusSerializer().data
			#return [CommunityConservationStatusSerializer(qs).data] # this array was used for dashboard on profile page

	def get_distribution(self,obj):
		try:
			qs = CommunityDistribution.objects.get(community=obj)
		except:
			qs = None
		return CommunityDistributionSerializer(qs).data

	def get_conservation_attributes(self,obj):
		try:
			qs = CommunityConservationAttributes.objects.get(community=obj)
			return CommunityConservationAttributesSerializer(qs).data
		except CommunityConservationAttributes.DoesNotExist:
			return CommunityConservationAttributesSerializer().data

	def get_can_user_edit(self,obj):
		return True


class InternalCommunitySerializer(BaseCommunitySerializer):
    can_user_edit = serializers.SerializerMethodField() #TODO need to add this property to Community model depending on customer status



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


class CreateSpeciesSerializer(BaseSpeciesSerializer):
    group_type_id = serializers.IntegerField(required=True, write_only= True);
    class Meta:
        model = Species
        fields = ('id',
			    'group_type_id',
			    )
        read_only_fields = (
            'id',
            )


class SaveCommunitySerializer(BaseCommunitySerializer):
    region_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
    district_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
    name_authority_id = serializers.IntegerField(required=False, allow_null=True, write_only= True);
    class Meta:
        model = Community
        fields = ('id',
			    'group_type',
			    'community_migrated_id',
			    'community_name',
			    'community_status',
			    'name_authority_id',
			    'region_id',
			    'district_id',
			    'last_data_curration_date',
			    'readonly',
			    'can_user_edit',
			    )
        read_only_fields=('id','group_type')


class CreateCommunitySerializer(BaseCommunitySerializer):
    group_type_id = serializers.IntegerField(required=True, write_only= True);
    class Meta:
        model = Community
        fields = ('id',
			    'group_type_id',
			    )
        read_only_fields = (
            'id',
            )


class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = SpeciesDocument
		fields = ('id','name','_file')


class SpeciesDocumentSerializer(serializers.ModelSerializer):
	document_category_name = serializers.SerializerMethodField()
	document_sub_category_name = serializers.SerializerMethodField()
	class Meta:
		model = SpeciesDocument
		fields = (
			'id',
			'document_number',
			'species',
			'name',
			'_file',
			'description',
			'input_name',
			'uploaded_date',
			'document_category',
			'document_category_name',
			'document_sub_category',
			'document_sub_category_name',
			'visible',
		)
		read_only_fields = ('id','document_number')

	def get_document_category_name(self,obj):
		if obj.document_category:
			return obj.document_category.document_category_name

	def get_document_sub_category_name(self,obj):
		if obj.document_sub_category:
			return obj.document_sub_category.document_sub_category_name


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
			'document_sub_category',
			)


class CommunityDocumentSerializer(serializers.ModelSerializer):
	document_category_name = serializers.SerializerMethodField()
	document_sub_category_name = serializers.SerializerMethodField()
	class Meta:
		model = CommunityDocument
		fields = (
			'id',
			'document_number',
			'community',
			'name',
			'_file',
			'description',
			'input_name',
			'uploaded_date',
			'document_category',
			'document_category_name',
			'document_sub_category',
			'document_sub_category_name',
			'visible',
		)
		read_only_fields = ('id','document_number')

	def get_document_category_name(self,obj):
		if obj.document_category:
			return obj.document_category.document_category_name

	def get_document_sub_category_name(self,obj):
		if obj.document_sub_category:
			return obj.document_sub_category.document_sub_category_name


class SaveCommunityDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommunityDocument
		fields = (
			'id',
			'community',
			'name',
			'description',
			'input_name',
			'uploaded_date',
			'document_category',
			'document_sub_category',
			)


class SpeciesLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()
    class Meta:
        model = SpeciesLogEntry
        fields = '__all__'
        read_only_fields = (
            'customer',
        )

    def get_documents(self,obj):
        return [[d.name,d._file.url] for d in obj.documents.all()]


class ConservationThreatSerializer(serializers.ModelSerializer):
	threat_category_name = serializers.SerializerMethodField()
	current_impact_name = serializers.SerializerMethodField()
	potential_impact_name = serializers.SerializerMethodField()
	potential_threat_onset_name = serializers.SerializerMethodField()
	class Meta:
		model = ConservationThreat
		fields = (
			'id',
			'threat_number',
			'threat_category',
			'threat_category_name',
			'threat_agent',
			'current_impact',
			'current_impact_name',
			'potential_impact',
			'potential_impact_name',
			'potential_threat_onset',
			'potential_threat_onset_name',
			'comment',
			'date_observed',
			'source',
			'species',
			'community',
			'visible',
		)
		read_only_fields = ('id','threat_number',)

	def get_threat_category_name(self,obj):
		if obj.threat_category:
			return obj.threat_category.name

	def get_current_impact_name(self,obj):
		if obj.current_impact:
			return obj.current_impact.name

	def get_potential_impact_name(self,obj):
		if obj.potential_impact:
			return obj.potential_impact.name

	def get_potential_threat_onset_name(self,obj):
		if obj.potential_threat_onset:
			return obj.potential_threat_onset.name


class SaveConservationThreatSerializer(serializers.ModelSerializer):
	class Meta:
		model = ConservationThreat
		fields = (
			'id',
			'species',
			'community',
			'threat_category',
			'threat_agent',
			'comment',
			'current_impact',
			'potential_impact',
			'potential_threat_onset',
			'date_observed',
			)
