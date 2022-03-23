import logging
from boranga.components.species_and_communities.models import Source, Species, SpeciesAttributes, SpeciesDocument
from rest_framework import serializers

logger = logging.getLogger('boranga')

class SpeciesDocumentsSerializer(serializers.ModelSerializer):
	document_category = serializers.SerializerMethodField()
	number = serializers.SerializerMethodField()
	name_reference = serializers.SerializerMethodField()
	genetic = serializers.SerializerMethodField()
	biology = serializers.SerializerMethodField()
	ecology = serializers.SerializerMethodField()
	fire = serializers.SerializerMethodField()
	disease = serializers.SerializerMethodField()

	class Meta:
		model = SpeciesDocument
		fields = (
				"id",
				"document_category",
				"document",
				"document_description",
				"date_time",
				"number",
				"name_reference",
				"genetic",
				"biology",
				"ecology",
				"fire",
				"disease",
			)
		datatables_always_serialize = (
				"id",
				"document",
				"document_category",
				"document_description",
				"date_time",
				"number",
				"name_reference",
				"genetic",
				"biology",
				"ecology",
				"fire",
				"disease",
			)	

	def get_document_category(self, species_document_obj):
		if species_document_obj.document_category:
			return species_document_obj.document_category.name
		return None

	def get_document(self, species_document_obj):
		if species_document_obj.document:
			return species_document_obj.document
		return None

	def get_document_description(self, species_document_obj):
		if species_document_obj.document_description:
			return species_document_obj.document_description
		return None

	def get_number(self, species_document_obj):
		if species_document_obj.id:
			return species_document_obj.id
		return None

	def get_name_reference(self, species_document_obj):
		return species_document_obj.species_name_reference

	def get_genetic(self, species_document_obj):
		species = species_document_obj.species
		species_attributes = SpeciesAttributes.objects.get(species=species)
		return species_attributes.genetic

	def get_biology(self, species_document_obj):
		species = species_document_obj.species
		species_attributes = SpeciesAttributes.objects.get(species=species)
		return species_attributes.biology
		
	def get_ecology(self, species_document_obj):
		species = species_document_obj.species
		species_attributes = SpeciesAttributes.objects.get(species=species)
		return species_attributes.ecology
		
	def get_fire(self, species_document_obj):
		species = species_document_obj.species
		species_attributes = SpeciesAttributes.objects.get(species=species)
		return species_attributes.fire
		
	def get_disease(self, species_document_obj):
		species = species_document_obj.species
		species_attributes = SpeciesAttributes.objects.get(species=species)
		return species_attributes.disease
		