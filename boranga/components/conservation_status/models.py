import datetime
from django.db import models
from boranga.components.main.models import (
    CommunicationsLogEntry, 
    UserAction,
    Document
)
from boranga.components.species_and_communities.models import(
    Species,
    Community,
)
import json
from django.db import models,transaction
from django.conf import settings


class ConservationList(models.Model):
    """

    NB: Can have multiple lists per species
    WAPEC       WA Priority Ecological Community List
    DBCA_RLE    Pre-BCA DBCA precursor to IUCN RLE
    WAPS        WA Priority Species List
    SPFN        Wildlife Conservation (Specially Protected Fauna) Notice, Schedules
    IUCN_RLE    IUCN Red List of Ecosystems
    IUCN2012    IUCN Red List Categories and Criteria v3.1(2001) 2nd edition (2012)
    IUCN2001    IUCN Red List Categories and Criteria v3.1(2001)
    EPBC        Environment Protection and Biodiversity Conservation Act 1999
    IUCN1994    IUCN Red List Categories v2.3 (1994)
    WAWCA       Wildlife Conservation Act 1950, Gazettal notice listing

    Has a:
    - N/A
    Used by:
    - SpeciesConservationStatus
    - CommunityConservationStatus
    - ConservationCategory
    - ConservationCriteria
    Is:
    - TBD
    """
    APPROVAL_LEVEL_CHOICES = (
        ('intermediate', 'Intermediate'),
        ('minister', 'Minister'),
    )

    code = models.CharField(max_length=64,
                            default="None")
    label = models.CharField(max_length=512,
                            default="None")
    applies_to_wa = models.BooleanField(default=False)
    applies_to_commonwealth = models.BooleanField(default=False)
    applies_to_international = models.BooleanField(default=False)
    applies_to_species = models.BooleanField(default=False)
    applies_to_communities = models.BooleanField(default=False)
    approval_level = models.CharField('Approval level', max_length=20, choices=APPROVAL_LEVEL_CHOICES,
                                        default=APPROVAL_LEVEL_CHOICES[0][0])

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.code)


class ConservationCategory(models.Model):
    """
    Dependent on Conservation List (FK)
    eg.:
    CR  Critically endangered fauna (S1)
    P1  Priority 1
    PD  Presumed Totally Destroyed
    P1  Priority 1
    EN  Endangered fauna (S2)
    P2  Priority 2
    

    Has a:
    - ConservationList
    Used by:
    - SpeciesConservationStatus
    - CommunityConservationStatus
    Is:
    - TBD
    """
    conservation_list = models.ForeignKey(ConservationList, on_delete=models.CASCADE, related_name="conservation_categories", null=True)
    code = models.CharField(max_length=64,
                            default="None")
    label = models.CharField(max_length=512,
                            default="None")

    class Meta:
        app_label = 'boranga'
        verbose_name = "Conservation Category"
        verbose_name_plural = "Conservation Categories"

    def __str__(self):
        return str(self.code)


class ConservationCriteria(models.Model):
    """
    Dependent on Conservation List (FK)

    Justification for listing as threatened (IUCN-how everything is defined)
    eg:
    A
    Ai
    Aii
    B
    Bi
    Bii
    NB: may have multiple of these per species
    Has a:
    - N/A
    Used by:
    - SpeciesConservationStatus
    - CommunityConservationStatus
    Is:
    - TBD
    """
    conservation_list = models.ForeignKey(ConservationList, on_delete=models.CASCADE, related_name="conservation_criterias", null=True)
    code = models.CharField(max_length=64)
    label = models.CharField(max_length=512,
                            default="None")

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return str(self.code)


class ConservationChangeCode(models.Model):
    """
    When the conservation status of a species/community is changed, it can be for a number of reasons. 
    These reasons are represented by change codes.
    """
    code = models.CharField(max_length=32,
                            default="None")
    label = models.CharField(max_length=512,
                            default="None")

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
    - ConservationChangeCode
    - ConservationList
    - ConservationCategory
    - ConservationCriteria
    Used by:
    - SpeciesConservationStatus
    - CommunityConservationStatus
    Is:
    - Abstract class
    """
    change_code = models.ForeignKey(ConservationChangeCode, 
                                    on_delete=models.SET_NULL , blank=True, null=True)
    conservation_list = models.ForeignKey(ConservationList,
                                             on_delete=models.CASCADE, blank=True, null=True)
    conservation_category = models.ForeignKey(ConservationCategory, 
                                              on_delete=models.SET_NULL, blank=True, null=True)
    conservation_criteria = models.ManyToManyField(ConservationCriteria, blank=True, null=True)
    comment = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        abstract = True
        app_label = 'boranga'

    def __str__(self):
        return str(self.conservation_list)  # TODO: is the most appropriate?


class SpeciesConservationStatus(ConservationStatus):
    """
    Species Conservation Status
    """
    species = models.ForeignKey(Species, on_delete=models.CASCADE , related_name="conservation_status")
    conservation_status_number = models.CharField(max_length=9, blank=True, default='')

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return(self.conservation_status_number)

    def save(self, *args, **kwargs):
        super(SpeciesConservationStatus, self).save(*args,**kwargs)
        if self.conservation_status_number == '':
            new_conservation_status_id = 'CS{}'.format(str(self.pk))
            self.conservation_status_number = new_conservation_status_id
            self.save()


class CommunityConservationStatus(ConservationStatus):
    """
    Community Conservation Status
    """
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="conservation_status")
    conservation_status_number = models.CharField(max_length=9, blank=True, default='')

    class Meta:
        app_label = 'boranga'

    def __str__(self):
        return(self.conservation_status_number)

    def save(self, *args, **kwargs):
        super(CommunityConservationStatus, self).save(*args,**kwargs)
        if self.conservation_status_number == '':
            new_conservation_status_id = 'CS{}'.format(str(self.pk))
            self.conservation_status_number = new_conservation_status_id
            self.save()
