import datetime
from django.db import models
from boranga.components.main.models import (
    CommunicationsLogEntry, 
    UserAction,
    Document
    )
import json
from django.db import models,transaction
from django.conf import settings


DISTRICT_PERTH_HILLS = 'PHS'
DISTRICT_SWAN_COASTAL = 'SWC'
DISTRICT_BLACKWOOD = 'BWD'
DISTRICT_WELLINGTON = 'WTN'
DISTRICT_DONNELLY = 'DON'
DISTRICT_FRANKLAND = 'FRK'
DISTRICT_ALBANY = 'ALB'
DISTRICT_ESPERANCE = 'ESP'
DISTRICT_EAST_KIMBERLEY = 'EKM'
DISTRICT_WEST_KIMBERLEY = 'WKM'
DISTRICT_EXMOUTH = 'EXM'
DISTRICT_PILBARA = 'PIL'
DISTRICT_KALGOORLIE = 'KAL'
DISTRICT_GERALDTON = 'GER'
DISTRICT_MOORA = 'MOR'
DISTRICT_SHARK_BAY = 'SHB'
DISTRICT_GREAT_SOUTHERN = 'GSN'
DISTRICT_CENTRAL_WHEATBELT = 'CWB'
DISTRICT_SOUTHERN_WHEATBELT = 'SWB'

DISTRICT_CHOICES = (
    (DISTRICT_PERTH_HILLS, "Perth Hills"),
    (DISTRICT_SWAN_COASTAL, "Swan Coastal"),
    (DISTRICT_BLACKWOOD, "Blackwood"),
    (DISTRICT_WELLINGTON, "Wellington"),
    (DISTRICT_DONNELLY, "Donnelly"),
    (DISTRICT_FRANKLAND, "Frankland"),
    (DISTRICT_ALBANY, "Albany"),
    (DISTRICT_ESPERANCE, "Esperance"),
    (DISTRICT_EAST_KIMBERLEY, "East Kimberley"),
    (DISTRICT_WEST_KIMBERLEY, "West Kimberley"),
    (DISTRICT_EXMOUTH, "Exmouth"),
    (DISTRICT_PILBARA, "Pilbara"),
    (DISTRICT_KALGOORLIE, "Kalgoorlie"),
    (DISTRICT_GERALDTON, "Geraldton"),
    (DISTRICT_MOORA, "Moora"),
    (DISTRICT_SHARK_BAY, "Shark Bay"),
    (DISTRICT_GREAT_SOUTHERN, "Great Southern"),
    (DISTRICT_CENTRAL_WHEATBELT, "Central Wheatbelt"),
    (DISTRICT_SOUTHERN_WHEATBELT, "Southern Wheatbelt")
)

REGION_KIMBERLEY = 'kimberley'
REGION_PILBARA = 'pilbara'
REGION_MIDWEST = 'midwest'
REGION_GOLDFIELDS = 'goldfields'
REGION_SWAN = 'swan'
REGION_WHEATBELT = 'wheatbelt'
REGION_SOUTH_WEST = 'southwest'
REGION_WARREN = 'warren'
REGION_SOUTH_COAST = 'southcoast'

REGION_CHOICES = (
    (REGION_KIMBERLEY,'Kimberley'),
    (REGION_PILBARA,'Pilbara'),
    (REGION_MIDWEST,'Midwest'),
    (REGION_GOLDFIELDS,'Goldfields'),
    (REGION_SWAN,'Swan'),
    (REGION_WHEATBELT,'Wheatbelt'),
    (REGION_SOUTH_WEST,'South West'),
    (REGION_WARREN,'Warren'),
    (REGION_SOUTH_COAST,'South Coast')
)

def update_species_doc_filename(instance, filename):
    return '{}/species/{}/species_documents/{}'.format(settings.MEDIA_APP_DIR, instance.species.id,filename)

def update_community_doc_filename(instance, filename):
    return '{}/community/{}/community_documents/{}'.format(settings.MEDIA_APP_DIR, instance.community.id,filename)

def update_species_comms_log_filename(instance, filename):
    return '{}/species/{}/communications/{}'.format(settings.MEDIA_APP_DIR, instance.log_entry.species.id,filename)

def update_community_comms_log_filename(instance, filename):
    return '{}/community/{}/communications/{}'.format(settings.MEDIA_APP_DIR, instance.log_entry.community.id,filename)


class Region(models.Model):
    name = models.CharField(choices=REGION_CHOICES, 
                            unique=True,
                            default=None,
                            max_length=64)

    class Meta:
        app_label = 'boranga'
        
    def __str__(self):
        return self.get_name_display()


class District(models.Model):
    name = models.CharField(choices=DISTRICT_CHOICES, 
                            unique=True,
                            max_length=64)
    region = models.ForeignKey(Region, 
                               on_delete=models.CASCADE )

    class Meta:
        app_label = 'boranga'
    def __str__(self):
        return self.get_name_display()


class GroupType(models.Model):
    """
    The three types of group managed by Boranga: fauna, flora and communities. These are the basis
    for all other models in Species and Communities.

    Has a:
    - N/A
    Used by:
    - Species
    - Community
    Is:
    - Enumeration (GroupTypes)
    """
    GROUP_TYPES = [('flora', 'Flora'), ('fauna', 'Fauna'), ('community', 'Community')]
    name = models.CharField(max_length=64,
                            choices=GROUP_TYPES,
                            default=GROUP_TYPES[1],)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return self.get_name_display()


class Contact(models.Model):
    """
    Hold the contact details for a person.
    """
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    role = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    email = models.EmailField()

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return '{}, {}'.format(self.last_name, self.first_name)


class NameAuthority(models.Model):
    """

    """
    name = models.CharField(max_length=128,
                            default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name)


class Species(models.Model):
    """
    Forms the basis for a Species and Communities record.

    Has a:
    - ConservationStatus
    - GroupType
    - SpeciesDocument
    - ConservationThreat
    - ConservationPlan
    - Taxonomy
    - Distribution
    - ConservationAttributes
    Used by:
    - Communities
    Is:
    - Table
    """
    species_number = models.CharField(max_length=9, blank=True, default='')
    group_type = models.ForeignKey(GroupType,
                                   on_delete=models.CASCADE)
    image = models.CharField(max_length=512,
                             default="None", null=True, blank=True)
    scientific_name = models.CharField(max_length=128,
                                       default="None", null=True, blank=True)
    common_name = models.CharField(max_length=128,
                                   default="None", null=True, blank=True)
    name_currency = models.CharField(max_length=16,
                                     default="None", null=True, blank=True) # is it the current name? yes or no
    #taxonomy = models.OneToOneField(Taxonomy, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, 
                               default=None,
                               on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, 
                                 default=None,
                                 on_delete=models.CASCADE, null=True, blank=True)
    last_data_curration_date = models.DateField(blank =True, null=True)
    processing_status = models.CharField(max_length=512,
                                         default="None", null=True, blank=True)
    
    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return '{}-{}'.format(self.species_number,self.scientific_name)

    def save(self, *args, **kwargs):
        # Prefix "S" char to species_number.
        super(Species, self).save(*args,**kwargs)
        if self.species_number == '':
            new_species_id = 'S{0:06d}'.format(self.pk)
            self.species_number = new_species_id
            self.save()

    @property
    def reference(self):
        return '{}-{}'.format(self.species_number,self.species_number) #TODO : the second parameter is lodgement.sequence no. don't know yet what for species it should be


class Taxonomy(models.Model):
    """
    Description from wacensus, to get the main name then fill in everything else

    Has a:
    - ConservationList
    - ConservationCategory
    - ConservationCriteria
    Used by:
    - Species
    - Communities
    Is:
    - Table
    """
    taxon = models.CharField(max_length=512,
                             default="None", null=True, blank=True)  # flora and fauna, name
    taxon_id = models.IntegerField(default=-1, null=True, blank=True)  # flora and fauna, name

    previous_name = models.CharField(max_length=512,
                                     default="None", null=True, blank=True)
    family = models.CharField(max_length=512,
                              default="None", null=True, blank=True)
    genus = models.CharField(max_length=512,
                             default="None", null=True, blank=True)
    phylogenetic_group = models.CharField(max_length=512,
                                          default="None", null=True, blank=True)
    name_authority = models.ForeignKey(NameAuthority,
                                       on_delete=models.CASCADE,null=True,blank=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, unique=True, null=True, related_name="species_taxonomy")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.taxon)  # TODO: is the most appropriate?


class SpeciesLogDocument(Document):
    log_entry = models.ForeignKey('SpeciesLogEntry',related_name='documents', on_delete=models.CASCADE)
    _file = models.FileField(upload_to=update_species_comms_log_filename, max_length=512)

    class Meta:
        app_label = 'boranga'


class SpeciesLogEntry(CommunicationsLogEntry):
    species = models.ForeignKey(Species, related_name='comms_logs', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.reference, self.subject)

    class Meta:
        app_label = 'boranga'

    def save(self, **kwargs):
        # save the application reference if the reference not provided
        if not self.reference:
            self.reference = self.species.reference
        super(SpeciesLogEntry, self).save(**kwargs)


class SpeciesDistribution(models.Model):
    """
    All the different locations where this species can be found.

    Used by:
    - Species
    Is:
    - Table
    """
    department_file_numbers = models.CharField(max_length=512,
                                               default="None", null=True, blank=True)  # objective, legacy, list of things
    number_of_occurrences = models.IntegerField(default=-1, null=True)
    extent_of_occurrences = models.IntegerField(default=-1, null = True)
    area_of_occupancy = models.IntegerField(default=-1, null=True)
    number_of_iucn_locations = models.IntegerField(default=-1, null=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, unique=True, null=True, related_name="species_distribution")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.id)  # TODO: is the most appropriate?


class Community(models.Model):
    """
    A collection of 2 or more Species within a specific location.

    Has a:
    - GroupType
    - Species
    Used by:
    - N/A
    Is:
    - Table
    """
    community_number = models.CharField(max_length=9, blank=True, default='')
    group_type = models.ForeignKey(GroupType,
                                   on_delete=models.CASCADE)
    species = models.ManyToManyField(Species, null=True, blank=True)
    community_id = models.CharField(max_length=200, null=True, blank=True)
    community_name = models.CharField(max_length=2048, null=True, blank=True)
    community_status = models.CharField(max_length=128, null=True, blank=True)
    community_description = models.CharField(max_length=2048, null=True, blank=True)
    region = models.ForeignKey(Region, 
                               default=None,
                               on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, 
                                 default=None,
                                 on_delete=models.CASCADE, null=True, blank=True)
    #conservation_status = models.OneToOneField(ConservationStatus,
    #                                       on_delete=models.CASCADE, null=True, blank=True)
    last_data_curration_date = models.DateField(blank =True, null=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.community_id)

    def save(self, *args, **kwargs):
        # Prefix "C" char to community_number.
        super(Community, self).save(*args,**kwargs)
        if self.community_number == '':
            new_community_id = 'C{0:06d}'.format(self.pk)
            self.community_number = new_community_id
            self.save()

    @property
    def reference(self):
        return '{}-{}'.format(self.community_number)


class CommunityLogDocument(Document):
    log_entry = models.ForeignKey('CommunityLogEntry',related_name='documents', on_delete=models.CASCADE)
    _file = models.FileField(upload_to=update_community_comms_log_filename, max_length=512)

    class Meta:
        app_label = 'boranga'


class CommunityLogEntry(CommunicationsLogEntry):
    community = models.ForeignKey(Community, related_name='comms_logs', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.reference, self.subject)

    class Meta:
        app_label = 'boranga'

    def save(self, **kwargs):
        # save the application reference if the reference not provided
        if not self.reference:
            self.reference = self.species.reference
        super(CommunityLogEntry, self).save(**kwargs)


class CommunityDistribution(models.Model):
    """
    All the different locations where this community can be found.

    Used by:
    - Communities
    Is:
    - Table
    """
    # Community Ecological Attributes
    community_original_area = models.IntegerField(default=-1, null=True, blank=True)
    community_original_area_accuracy = models.IntegerField(default=-1, null=True, blank=True)
    community_original_area_reference = models.CharField(max_length=512,
                                                         default="None", null=True, blank=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, unique=True, null=True, related_name="community_distribution")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.id)  # TODO: is the most appropriate?


class CommitteeMeeting(models.Model):
    """
    A change in conservation status for a species is executed during Committee Meetings. 
    It is necessary to capture these changes and the meetings that caused the change. 

    Has a:
    - Contact
    """
    attendees = models.ManyToManyField(Contact,
                                       blank=False)
    date = models.DateField()
    location = models.CharField(max_length=128)
    species = models.ManyToManyField(Species,
                                     blank=False)
                                
    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.date)


class SpeciesAttributes(models.Model):
    """
    Do no know what this is but is required for SpeciesDocuments
    """
    name_reference = models.CharField(max_length=128,
                                      default="None")
    genetic = models.CharField(max_length=128,
                               default="None")
    biology = models.CharField(max_length=128,
                               default="None")
    ecology = models.CharField(max_length=128,
                               default="None")
    fire = models.CharField(max_length=128,
                            default="None")
    disease = models.CharField(max_length=128,
                               default="None")

    species = models.ForeignKey(Species, blank=False, 
                                on_delete=models.CASCADE)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name_reference)  # TODO: is the most appropriate?


class Source(models.Model):
    """

    """
    name = models.CharField(max_length=128,
                            default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name)


class DocumentCategory(models.Model):
    """
    This is particularly useful for organisation of documents e.g. preventing inappropriate documents being added
    to certain tables.

    Used by:
    - DocumentSubCategory
    - SpeciesDocument
    - CommunityDocument
    Is:
    - Table
    """
    document_category_name = models.CharField(max_length=128, unique=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.document_category_name)


class DocumentSubCategory(models.Model):
    """
    This is particularly useful for organisation of sub documents e.g. preventing inappropriate documents being added
    to certain tables.

    Used by:
    - SpeciesDocument
    - CommunityDocument
    Is:
    - Table
    """
    document_category = models.ForeignKey(DocumentCategory, 
                                          on_delete=models.CASCADE,
                                          related_name='document_sub_categories')
    document_sub_category_name = models.CharField(max_length=128, unique=True,)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.document_sub_category_name)
                                    

class SpeciesDocument(Document):
    """
    Meta-data associated with a document relevant to a Species.

    Has a:
    - Species
    - DocumentCategory
    - DocumentSubCategoty
    Used for:
    - Species
    Is:
    - Table
    """
    document_number = models.CharField(max_length=9, blank=True, default='')
    _file = models.FileField(upload_to=update_species_doc_filename, max_length=512, default="None")
    input_name = models.CharField(max_length=255,null=True,blank=True)
    can_delete = models.BooleanField(default=True) # after initial submit prevent document from being deleted
    visible = models.BooleanField(default=True) # to prevent deletion on file system, hidden and still be available in history 
    document_category = models.ForeignKey(DocumentCategory, 
                                          null=True,
                                          blank=True,
                                          on_delete=models.CASCADE)
    document_sub_category = models.ForeignKey(DocumentSubCategory, 
                                          null=True,
                                          blank=True,
                                          on_delete=models.CASCADE)
    species = models.ForeignKey(Species, 
                                blank=False, 
                                default=None,
                                on_delete=models.CASCADE,
                                related_name='species_documents')

    class Meta:
        app_label = 'boranga'
        verbose_name = "Species Document"

    def save(self, *args, **kwargs):
        # Prefix "D" char to document_number.
        super(SpeciesDocument, self).save(*args,**kwargs)
        if self.document_number == '':
            new_document_id = 'D{0:06d}'.format(self.pk)
            self.document_number = new_document_id
            self.save()

    def add_documents(self, request):
        with transaction.atomic():
            try:
                # save the files
                data = json.loads(request.data.get('data'))
                # if not data.get('update'):
                #     documents_qs = self.filter(input_name='species_doc', visible=True)
                #     documents_qs.delete()
                for idx in range(data['num_files']):
                    _file = request.data.get('file-'+str(idx))
                    self._file=_file
                    self.name=_file.name
                    self.input_name = data['input_name']
                    self.can_delete = True
                    self.save()
                # end save documents
                self.save()
            except:
                raise
        return


class CommunityDocument(Document):
    """
    Meta-data associated with a document relevant to a Community.

    Has a:
    - Community
    - DocumentCategory
    - DocumentSubCategory
    Used for:
    - Community:
    Is:
    - Table
    """
    document_number = models.CharField(max_length=9, blank=True, default='')
    _file = models.FileField(upload_to=update_community_doc_filename, max_length=512, default="None")
    input_name = models.CharField(max_length=255,null=True,blank=True)
    can_delete = models.BooleanField(default=True) # after initial submit prevent document from being deleted
    visible = models.BooleanField(default=True) # to prevent deletion on file system, hidden and still be available in history 
    document_category = models.ForeignKey(DocumentCategory, 
                                          null=True,
                                          blank=True,
                                          on_delete=models.CASCADE)
    document_sub_category = models.ForeignKey(DocumentSubCategory, 
                                          null=True,
                                          blank=True,
                                          on_delete=models.CASCADE)
    community = models.ForeignKey(Community, 
                                blank=False, 
                                default=None,
                                on_delete=models.CASCADE,
                                related_name='community_documents')

    class Meta:
        app_label = 'boranga'
        verbose_name = "Community Document"

    def save(self, *args, **kwargs):
        # Prefix "D" char to document_number.
        super(CommunityDocument, self).save(*args,**kwargs)
        if self.document_number == '':
            new_document_id = 'D{0:06d}'.format(self.pk)
            self.document_number = new_document_id
            self.save()
    
    def add_documents(self, request):
        with transaction.atomic():
            try:
                # save the files
                data = json.loads(request.data.get('data'))
                # if not data.get('update'):
                #     documents_qs = self.filter(input_name='species_doc', visible=True)
                #     documents_qs.delete()
                for idx in range(data['num_files']):
                    _file = request.data.get('file-'+str(idx))
                    self._file=_file
                    self.name=_file.name
                    self.input_name = data['input_name']
                    self.can_delete = True
                    self.save()
                # end save documents
                self.save()
            except:
                raise
        return


class ThreatCategory(models.Model):
    """
    # e.g. mechnical disturbance
    """
    name = models.CharField(max_length=128, blank=False, unique=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name)


class CurrentImpact(models.Model):
    """
    # don't know the data yet

    Used by:
    - ConservationThreat

    """
    name = models.CharField(max_length=100, blank=False, unique=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name)


class PotentialImpact(models.Model):
    """
    # don't know the data yet
    
    Used by:
    - ConservationThreat

    """
    name = models.CharField(max_length=100, blank=False, unique=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name)


class PotentialThreatOnset(models.Model):
    """
    # don't know the data yet
    
    Used by:
    - ConservationThreat

    """
    name = models.CharField(max_length=100, blank=False, unique=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name)


class ConservationThreat(models.Model):
    """
    Threat for a species and community in a particular location.

    NB: Maybe make many to many

    Has a:
    - species
    - community
    Used for:
    - Species
    - Community
    Is:
    - Table
    """
    species = models.ForeignKey(Species, on_delete=models.CASCADE, null=True, blank=True , related_name="species_threats")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True, related_name="community_threats")
    threat_number = models.CharField(max_length=9, blank=True, default='')
    threat_category = models.ForeignKey(ThreatCategory, on_delete=models.CASCADE)
    threat_agent = models.CharField(max_length=512,
                                          default="None")
    current_impact = models.ForeignKey(CurrentImpact, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    potential_impact = models.ForeignKey(PotentialImpact, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    potential_threat_onset = models.ForeignKey(PotentialThreatOnset, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    comment = models.CharField(max_length=512,
                               default="None")
    date_observed = models.DateField(blank =True, null=True)
    visible = models.BooleanField(default=True) # to prevent deletion, hidden and still be available in history


    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.id)  # TODO: is the most appropriate?

    def save(self, *args, **kwargs):
        super(ConservationThreat, self).save(*args,**kwargs)
        if self.threat_number == '':
            new_threat_id = 'T{0:06d}'.format(self.pk)
            self.threat_number = new_threat_id
            self.save()

    @property
    def source(self):
        if self.species:
            return self.species.id
        elif self.community:
            return self.community.id


class ConservationPlan(models.Model):
    """
    Each occurrence of each species can have one or more plan to protect it.

    Has a:
    - N/A
    Used by:
    - Species
    Is:
    - Table
    """
    region = models.ForeignKey(Region, 
                               default=None,
                               on_delete=models.CASCADE)
    district = models.ForeignKey(District, 
                                 default=None,
                                 on_delete=models.CASCADE)
    type = models.CharField(max_length=512,
                            default="None")
    comment = models.CharField(max_length=512,
                               default="None")
    source = models.CharField(max_length=1024,
                              default="None")

    species = models.ManyToManyField(Species, blank=False)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.threat_category)  # TODO: is the most appropriate?


class ConservationAttributes(models.Model):
    """
    Additional meta-data particularly of use to administration.

    Used by:
    - Species
    Is:
    - Table
    """
    general_management_advice = models.CharField(max_length=512,
                                                 default="None", null=True, blank=True)
    ecological_attributes = models.CharField(max_length=512,
                                             default="None", null=True, blank=True)
    biological_attributes = models.CharField(max_length=512,
                                             default="None", null=True, blank=True)
    specific_survey_advice = models.CharField(max_length=512,
                                              default="None", null=True, blank=True)

    species = models.ForeignKey(Species, on_delete=models.CASCADE, unique=True, null=True, related_name="species_conservation_attributes")
    comments = models.CharField(max_length=2048,
                                default="None", null=True, blank=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.id)  # TODO: is the most appropriate?


# TODO Should delete this model as not required 
class Distribution(models.Model):
    """
    All the different locations where this species can be found.

    Has a:
    - ConservationList
    - ConservationCategory
    - ConservationCriteria
    Used by:
    - Species
    - Communities
    Is:
    - Table
    """
    department_file_numbers = models.CharField(max_length=512,
                                               default="None")  # objective, legacy, list of things
    number_of_occurrences = models.IntegerField(default=-1)
    extent_of_occurrences = models.IntegerField(default=-1)
    area_of_occupancy = models.IntegerField(default=-1)
    number_of_iucn_locations = models.IntegerField(default=-1)
    # Community Ecological Attributes
    community_original_area = models.IntegerField(default=-1)
    community_original_area_accuracy = models.IntegerField(default=-1)
    community_original_area_reference = models.CharField(max_length=512,
                                                         default="None")
    species = models.OneToOneField(Species, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.community_original_area_reference)  # TODO: is the most appropriate?
