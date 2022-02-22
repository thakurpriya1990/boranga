import datetime
from django.db import models
from django.db.models.deletion import CASCADE


class RegionDistrict(models.Model):

    DISTRICT_PERTH_HILLS = 'PHD'
    DISTRICT_SWAN_COASTAL = 'SCD'
    DISTRICT_SWAN_REGION = 'SWAN'
    DISTRICT_BLACKWOOD = 'BWD'
    DISTRICT_WELLINGTON = 'WTN'
    DISTRICT_SOUTH_WEST_REGION = 'SWR'
    DISTRICT_DONNELLY = 'DON'
    DISTRICT_FRANKLAND = 'FRK'
    DISTRICT_WARREN_REGION = 'WR'
    DISTRICT_ALBANY = 'ALB'
    DISTRICT_ESPERANCE = 'ESP'
    DISTRICT_SOUTH_COAST_REGION = 'SCR'
    DISTRICT_EAST_KIMBERLEY = 'EKD'
    DISTRICT_WEST_KIMBERLEY = 'WKD'
    DISTRICT_KIMBERLEY_REGION = 'KIMB'
    DISTRICT_PILBARA_REGION = 'PIL'
    DISTRICT_EXMOUTH = 'EXM'
    DISTRICT_GOLDFIELDS_REGION = 'GLD'
    DISTRICT_GERALDTON = 'GER'
    DISTRICT_KALBARRI = 'KLB'
    DISTRICT_MOORA = 'MOR'
    DISTRICT_SHARK_BAY = 'SHB'
    DISTRICT_MIDWEST_REGION = 'MWR'
    DISTRICT_CENTRAL_WHEATBELT = 'CWB'
    DISTRICT_SOUTHERN_WHEATBELT = 'SWB'
    DISTRICT_WHEATBELT_REGION = 'WBR'
    DISTRICT_AVIATION = 'AV'
    DISTRICT_OTHER = 'OTH'
    DISTRICT_KENSINGTON = 'KENSINGTON'
    
    DISTRICT_CHOICES = (
        (DISTRICT_SWAN_REGION, "Swan Region"),
        (DISTRICT_PERTH_HILLS, "Perth Hills"),
        (DISTRICT_SWAN_COASTAL, "Swan Coastal"),
        (DISTRICT_SOUTH_WEST_REGION, "South West Region"),
        (DISTRICT_BLACKWOOD, "Blackwood"),
        (DISTRICT_WELLINGTON, "Wellington"),
        (DISTRICT_WARREN_REGION, "Warren Region"),
        (DISTRICT_DONNELLY, "Donnelly"),
        (DISTRICT_FRANKLAND, "Frankland"),
        (DISTRICT_SOUTH_COAST_REGION, "South Coast Region"),
        (DISTRICT_ALBANY, "Albany"),
        (DISTRICT_ESPERANCE, "Esperance"),
        (DISTRICT_KIMBERLEY_REGION, "Kimberley Region"),
        (DISTRICT_EAST_KIMBERLEY, "East Kimberley"),
        (DISTRICT_WEST_KIMBERLEY, "West Kimberley"),
        (DISTRICT_PILBARA_REGION, "Pilbara Region"),
        (DISTRICT_EXMOUTH, "Exmouth"),
        (DISTRICT_GOLDFIELDS_REGION, "Goldfields Region"),
        (DISTRICT_MIDWEST_REGION, "Midwest Region"),
        (DISTRICT_GERALDTON, "Geraldton"),
        (DISTRICT_KALBARRI, "Kalbarri"),
        (DISTRICT_MOORA, "Moora"),
        (DISTRICT_SHARK_BAY, "Shark Bay"),
        (DISTRICT_WHEATBELT_REGION, "Wheatbelt Region"),
        (DISTRICT_CENTRAL_WHEATBELT, "Central Wheatbelt"),
        (DISTRICT_SOUTHERN_WHEATBELT, "Southern Wheatbelt"),
        (DISTRICT_AVIATION, "Aviation"),
        (DISTRICT_OTHER, "Other"),
        (DISTRICT_KENSINGTON, "Kensington"),
    )

    district = models.CharField(max_length=32, 
        choices=DISTRICT_CHOICES, 
        default=DISTRICT_OTHER)

    region = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='districts',
        on_delete=CASCADE)

    class Meta:
        app_label = 'boranga'
        verbose_name = 'boranga_Region District'
        verbose_name_plural = 'boranga_Region Districts'

    def __str__(self):
        return self.get_district_display()

    @property
    def display_name(self):
        return self.__str__


class GroupType(models.Model):
    """
    The three types of group managed by Boranga: fauna, flora and communities. These are the basis
    for all other models in Species and Communities.

    Has a:
    - N/A
    Used by:
    - Species
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


class ConservationList(models.Model):
    """

    NB: Can have multiple lists per species
    WAPEC	    WA Priority Ecological Community List
    DBCA_RLE	Pre-BCA DBCA precursor to IUCN RLE
    WAPS	    WA Priority Species List
    SPFN	    Wildlife Conservation (Specially Protected Fauna) Notice, Schedules
    IUCN_RLE	IUCN Red List of Ecosystems
    IUCN2012	IUCN Red List Categories and Criteria v3.1(2001) 2nd edition (2012)
    IUCN2001	IUCN Red List Categories and Criteria v3.1(2001)
    EPBC	    Environment Protection and Biodiversity Conservation Act 1999
    IUCN1994	IUCN Red List Categories v2.3 (1994)
    WAWCA	    Wildlife Conservation Act 1950, Gazettal notice listing

    Has a:
    - N/A
    Used by:
    - ConservationStatus
    Is:
    - TBD
    """
    code = models.CharField(max_length=64,
                            default="None")
    label = models.CharField(max_length=1024,
                            default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.code)


class ConservationCategory(models.Model):
    """
    CR	Critically endangered fauna (S1)
    P1	Priority 1
    PD	Presumed Totally Destroyed
    P1	Priority 1
    EN	Endangered fauna (S2)
    P2	Priority 2
    P2	Priority 2
    CR	Critically Endangered
    VU	Vulnerable fauna (S3)
    P3	Priority 3
    P3	Priority 3
    EN	Endangered
    EX	Presumed extinct fauna (S4)
    P4	Priority 4
    P4	Priority 4
    VU	Vulnerable
    P5	Priority 5
    LR	Lower Risk
    IA	Migratory birds under international agreement (S5)
    CD	Conservation dependent fauna (S6)
    DD	Data Deficient
    NE	Not Evaluated
    OS	Other specially protected fauna (S7)
    P5	Priority 5
    SP	Rare or otherwise in need of special protection
    P	Priority
    T	(Threatened) Rare or is likely to become extinct (S1)
    X	Presumed extinct (S2)
    I	Migratory birds under international agreement (S3)
    S	Other specially protected fauna (S4)
    CO	Collapsed
    CR	Critically Endangered
    EN	Endangered
    VU	Vulnerable
    NT	Near Threatened
    LC	Least Concern
    DD	Data Deficient
    NE	Not Evaluated
    EX	Extinct
    EW	Extinct in the Wild
    CR	Critically Endangered
    EN	Endangered
    VU	Vulnerable
    NT	Near Threatened
    LC	Least Concern
    DD	Data Deficient
    NE	Not Evaluated
    EX	Extinct
    EW	Extinct in the Wild
    CR	Critically Endangered
    EN	Endangered
    VU	Vulnerable
    EX	Extinct
    CR	Critically Endangered
    EN	Endangered
    VU	Vulnerable
    MA	Marine
    MI	Migratory
    CT	Cetacean
    EX	Extinct
    EW	Extinct in the Wild
    CR	Critically Endangered
    EN	Endangered
    VU	Vulnerable
    CD	Conservation Dependent
    SP	Specially Protected
    E	Extant (S1)
    X	Presumed extinct (S2)

    Has a:
    - N/A
    Used by:
    - ConservationStatus
    Is:
    - TBD
    """
    code = models.CharField(max_length=64,
                            default="None")
    label = models.CharField(max_length=1024,
                            default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.code)


class ConservationCriteria(models.Model):
    """
    Justification for listing as threatened (IUCN-how everything is defined)
    A
    Ai
    Aii
    B
    Bi
    Bii
    Biii
    C
    A1
    A2a
    A2b
    A3
    B1ai
    B1aii
    B1aiii
    B1b
    B1c
    B2ai
    B2aii
    B2aiii
    B2b
    B2c
    B3
    C1
    C2a
    C2b
    C3
    D1
    D2a
    D2b
    D3
    E
    A1a
    A1b
    A1c
    A1d
    A1e
    A2c
    A2d
    A2e
    A3b
    A3c
    A3d
    A3e
    A4a
    A4b
    A4c
    A4d
    A4e
    B1a
    B1b(i)
    B1b(ii)
    B1b(iii)
    B1b(iv)
    B1b(v)
    B1c(i)
    B1c(ii)
    B1c(iii)
    B1c(iv)
    B2a
    B2b(i)
    B2b(ii)
    B2b(iii)
    B2b(iv)
    B2b(v)
    B2c(i)
    B2c(ii)
    B2c(iii)
    B2c(iv)
    C2a(i)
    C2a(ii)
    D
    D2
    Criterion 1
    Criterion 2
    Criterion 3
    Criterion 4
    Criterion 5
    B1
    B2d
    B2e
    B3a
    B3b
    B3c
    B3d
    NB: may have multiple of these per species
    Has a:
    - N/A
    Used by:
    - ConservationStatus
    Is:
    - TBD
    """
    code = models.CharField(max_length=64)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.code)


class ConservationStatus(models.Model):
    """
    Several lists with different attributes

    NB: Different lists has different different entries
    mainly interest in wa but must accomodte comm as well
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
    conservation_list = models.OneToOneField(ConservationList,
                                             on_delete=models.CASCADE,
                                             primary_key=True,)
    conservation_category = models.ForeignKey(ConservationCategory, on_delete=CASCADE)
    conservation_criteria = models.ForeignKey(ConservationCriteria, on_delete=CASCADE)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.conservation_list)  # TODO: is the most appropriate?


class NameAuthority(models.Model):
    """

    """
    name = models.CharField(max_length=128,
                            default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name)


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
                             default="None")  # flora and fauna, name
    taxon_id = models.IntegerField(default=-1)  # flora and fauna, name

    previous_name = models.CharField(max_length=512,
                                     default="None")
    family = models.CharField(max_length=512,
                              default="None")
    genus = models.CharField(max_length=512,
                             default="None")
    phylogenetic_group = models.CharField(max_length=512,
                                          default="None")
    name_authority = models.ForeignKey(NameAuthority,
                                       on_delete=models.CASCADE)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.taxon)  # TODO: is the most appropriate?


class Species(models.Model):
    """
    Forms the basis for a Species and Communities record.

    Has a:
    - ConservationStatus
    - Community
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
    group_type = models.ForeignKey(GroupType,
                                   on_delete=models.CASCADE)
    scientific_name = models.CharField(max_length=128,
                                       default="None")
    common_name = models.CharField(max_length=128,
                                   default="None")
    name_currency = models.CharField(max_length=512,
                                     default="None") # is it the current name? yes or no
    conservation_status = models.OneToOneField(ConservationStatus,
                                               on_delete=models.CASCADE)
    # community many to many
    district = models.ForeignKey(RegionDistrict, 
                                 related_name='species_district', 
                                 null=True,
                                 on_delete=models.CASCADE)
    region = models.ForeignKey(RegionDistrict, 
                               related_name='species_region', 
                               null=True,
                               on_delete=models.CASCADE)
    image = models.CharField(max_length=512,
                             default="None")
    processing_status = models.CharField(max_length=512,
                                         default="None")
    # species_document foreign key
    # conservation_threats foreign key
    # conservation_plans many to many
    taxonomy = models.OneToOneField(Taxonomy, on_delete=models.CASCADE,)
    # distribution one to one
    # conservation_attributes one to one

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.taxonomy.taxon)  # TODO: is the most appropriate?


class Source(models.Model):
    """

    """
    name = models.CharField(max_length=128,
                            default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name)


class Community(models.Model):
    """
    A collection of 2 or more Species within a specific location.

    Has a:
    - ConservationStatus
    - Species
    Used by:
    - N/A
    Is:
    - Table
    """
    group_type = models.ForeignKey(GroupType,
                                   on_delete=models.CASCADE)
    community_name = models.CharField(max_length=2048,
                                      default="None")
    community_id = models.IntegerField(default=-1) # this will be the display name and will appear in filter list
    community_status = models.CharField(max_length=128,
                                        default="None")
    district = models.ForeignKey(RegionDistrict, 
                                 related_name='community_district', 
                                 null=True,
                                 on_delete=models.CASCADE)
    region = models.ForeignKey(RegionDistrict, 
                               related_name='community_region', 
                               null=True,
                               on_delete=models.CASCADE)

    species = models.ManyToManyField(Species, blank=False)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str("{}: {}".format(self.community_id, self.community_name))


class SpeciesDocument(models.Model):
    """
    Meta-data associated with a document relevant to a Species.

    Has a:
    - DocumentCategory
    Used by:
    - Species
    - Communities:
    Is:
    - Table
    """
    document = models.CharField(max_length=512,                 
                                default="None") # document file name without path
    document_description = models.CharField(max_length=1024,
                                            default="None")
    date_time = models.DateField(default=datetime.date.today)

    species = models.ManyToManyField(Species, blank=False)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.document)


class DocumentCategory(models.Model):
    """
    This is particularly useful for organisation of documents e.g. preventing inappropriate documents being added
    to certain tables.

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
    name = models.CharField(max_length=128,
                            default="None")
    species_document = models.ForeignKey(to=SpeciesDocument, 
                                         on_delete=CASCADE)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name)


class ThreatCategory(models.Model):
    """
    # e.g. mechnical disturbance
    """
    name = models.CharField(max_length=128,
                            default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.name)


class ConservationThreat(models.Model):
    """
    Threat for a species in a particular location.

    NB: Maybe make many to many

    Has a:
    - N/A
    Used by:
    - Species
    Is:
    - Table
    """
    threat_category = models.ForeignKey(ThreatCategory, on_delete=CASCADE)
    threat_description = models.CharField(max_length=512,
                                          default="None")
    comment = models.CharField(max_length=512,
                               default="None")
    document = models.CharField(max_length=1024,
                                default="None")
    source = models.CharField(max_length=1024,
                              default="None") # from species or occurrence_threat -> species level
    species = models.ForeignKey(Species, on_delete=CASCADE)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.threat_category)  # TODO: is the most appropriate?


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
    district = models.ForeignKey(RegionDistrict, 
                                 related_name='conservation_plan_district', 
                                 null=True,
                                 on_delete=models.CASCADE)

    region = models.ForeignKey(RegionDistrict, 
                               related_name='conservation_plan_region', 
                               null=True,
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
    general_management_advice = models.CharField(max_length=512,
                                                 default="None")
    ecological_attributes = models.CharField(max_length=512,
                                             default="None")
    biological_attributes = models.CharField(max_length=512,
                                             default="None")
    specific_survey_advice = models.CharField(max_length=512,
                                              default="None")

    species = models.OneToOneField(Species,
                                   on_delete=models.CASCADE,
                                   primary_key=True,)
    comments = models.CharField(max_length=2048,
                                default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.species.taxonomy.taxon)  # TODO: is the most appropriate?


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
    community_original_area = models.IntegerField(default=-1)
    community_original_area_accuracy = models.IntegerField(default=-1)
    number_of_occurrences = models.IntegerField(default=-1)
    extent_of_occurrences = models.IntegerField(default=-1)
    area_of_occupancy = models.IntegerField(default=-1)
    number_of_iucn_locations = models.IntegerField(default=-1)
    community_original_area_reference = models.CharField(max_length=512,
                                                         default="None")
    species = models.OneToOneField(Species,
                                   on_delete=models.CASCADE,
                                   primary_key=True,)

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.community_original_area_reference)  # TODO: is the most appropriate?
