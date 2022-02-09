
import csv
from random import randrange
from django.db.models import DateField
from django.test import TestCase

# Create your tests here.
from boranga.components.species_and_communities.models import Species, GroupType, ConservationStatus, ConservationList, \
    ConservationCategory, ConservationCriteria, Taxonomy, Community, SpeciesDocument, ConservationThreat, \
    ConservationPlan, Distribution, ConservationAttributes

def create_test_data():
    # print('----------------------------------------------------')
    # print('--------------ADDING TEST DATA----------------------')
    # print('----------------------------------------------------')
    # create_group_types()
    # create_species_fauna()
    # create_species_flora()
    # create_community()
    pass

def create_group_types():
    try:
        flora_group_type = GroupType.objects.get_or_create(name=GroupType.GROUP_TYPES[0][0])[0]
        fauna_group_type = GroupType.objects.get_or_create(name=GroupType.GROUP_TYPES[1][0])[0]
        community_group_type = GroupType.objects.get_or_create(name=GroupType.GROUP_TYPES[2][0])[0]

        flora_group_type.save()
        fauna_group_type.save()
        community_group_type.save()
    except Exception as e:
        print("create_group_types falied: ", e)
        print("-----")

def create_community():
    """
    This will take a fauna data file, create a community entry and save to the database. It will also randomly select a fauna and flora
    to be added to the Community that is created. It is surrounded by try/except
    so if row fails, that row can be recorded as faulty and saved to a file for examination.
    """
    row_failed = False
    failed_rows = []
    data_row = 1

    with open('/home/graeme/workspace/boranga/boranga/components/species_and_communities/tests/communities.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for index, community_row in enumerate(reader):
            if index >= data_row:
                try:
                    community_name = community_row[1]

                    # Don't want it if the name is empty
                    if not community_name: continue
                    community_id = randrange(1000)
                    community_status = "Safe"
                    region = randrange(100)
                    district = randrange(200)
                    group_type = GroupType.objects.get(name=GroupType.GROUP_TYPES[2][0])
                    community = Community.objects.create(group_type=group_type,
                                                         community_name=community_name,
                                                         community_id=community_id,
                                                         community_status=community_status,
                                                         region=region,
                                                         district=district,)
                    # Pick a random fauna to add to community
                    fauna_size = len(Species.objects.filter(group_type__name=GroupType.GROUP_TYPES[1][0]))
                    fauna = Species.objects.get(group_type__name=GroupType.GROUP_TYPES[1][0], id=randrange(fauna_size))
                    community.species.add(fauna)
                    # Pick a random flora to add to community
                    flora_size = len(Species.objects.filter(group_type__name=GroupType.GROUP_TYPES[0][0]))
                    flora = Species.objects.get(group_type__name=GroupType.GROUP_TYPES[0][0], id=randrange(flora_size))
                    community.species.add(fauna)
                    
                except Exception as e:
                    row_failed = True
                    failed_rows.append(community_row)
                    print('{}: {}'.format(e, community_row))
                    # could write falied_rows to file.

                if not row_failed:
                    community.save()

def create_species_fauna():
    """
    This will take a fauna data file, create a species entry and save to the database. It is surrounded by try/except
    so if row fails, that row can be recorded as faulty and saved to a file for examination.
    """
    row_failed = False
    failed_rows = []

    data_row = 2
    with open('/home/graeme/workspace/boranga/boranga/components/species_and_communities/tests/fauna.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for index, fauna_row in enumerate(reader):
            if index >= data_row:
                try:
                    conservation_list = ConservationList.objects.create(name=fauna_row[1])
                    conservation_category = ConservationCategory.objects.create(name=fauna_row[0].split('.')[2])
                    conservation_criteria = ConservationCriteria.objects.create(name=fauna_row[4])
                    conservation_status = ConservationStatus.objects.create(conservation_list=conservation_list,
                                                                            conservation_category=conservation_category,
                                                                            conservation_criteria=conservation_criteria)

                    taxon = fauna_row[6]
                    taxon_id = randrange(5000)
                    family = fauna_row[6]
                    genus = fauna_row[6]
                    phylogenetic_group = fauna_row[6]
                    name_authority = "WA Museum"
                    taxonomy = Taxonomy.objects.create(taxon=taxon,
                                                    taxon_id=taxon_id,
                                                    family=family,
                                                    genus=genus,
                                                    phylogenetic_group=phylogenetic_group,
                                                    name_authority=name_authority,)

                    group_type = GroupType.objects.get(name=GroupType.GROUP_TYPES[1][0])
                    fauna = Species.objects.create(common_name=fauna_row[7],
                                                group_type=group_type,
                                                scientific_name = fauna_row[6],
                                                conservation_status = conservation_status,
                                                region = randrange(500),
                                                district = randrange(100),
                                                image = "path/to/fauna.jpg",
                                                taxonomy = taxonomy

                    )

                    species_id = fauna.id
                    category_id = conservation_category.id
                    status = fauna_row[4]
                    document = "{}.pdf".format(fauna_row[5])
                    document_description = "{}.pdf".format(fauna_row[5])
                    species_document = SpeciesDocument.objects.create(species_id=species_id,
                                                                    category_id=category_id,
                                                                    status=status,
                                                                    document=document,
                                                                    document_description=document_description,)
                    species_document.species.add(fauna)

                    species_id = fauna.id
                    threat_category_id = randrange(1000)
                    threat_description = fauna_row[3]
                    comment = "{} is fauna".format(fauna_row[8])
                    document = "{}.pdf".format(fauna_row[5])
                    source = "WA Museum"
                    conservation_threats = ConservationThreat(species_id=species_id,
                                                            threat_category_id=threat_category_id,
                                                            threat_description=threat_description,
                                                            comment=comment,
                                                            document=document,
                                                            source=source,)
                    
                    _type = "Regular"
                    threat_category_id = randrange(10000)
                    region_id = randrange(1000)
                    district_id = randrange(100)
                    comment = "{} is a fauna plan.".format(fauna_row[8])
                    source = "WA Museum"
                    conservation_plans = ConservationPlan.objects.create(threat_category_id=threat_category_id,
                                                                        region_id=region_id,
                                                                        district_id=district_id,
                                                                        type=_type,
                                                                        comment=comment,
                                                                        source=source,)
                    conservation_plans.species.add(fauna)

                    department_file_numbers = fauna_row[3]
                    community_original_area = randrange(10000)
                    community_original_area_accuracy = randrange(1000)
                    number_of_occurrences = randrange(100)
                    extent_of_occurrences = randrange(100)
                    area_of_occupancy = randrange(100)
                    number_of_iucn_locations = randrange(100)
                    community_original_area_reference = fauna_row[7]
                    distribution = Distribution.objects.create(department_file_numbers=department_file_numbers,
                                                            community_original_area=community_original_area,
                                                            community_original_area_accuracy=community_original_area_accuracy,
                                                            number_of_occurrences=number_of_occurrences,
                                                            extent_of_occurrences=extent_of_occurrences,
                                                            area_of_occupancy=area_of_occupancy,
                                                            number_of_iucn_locations=number_of_iucn_locations,
                                                            community_original_area_reference=community_original_area_reference,
                                                            species=fauna)

                    general_management_advice = "{} is a fauna gen management advice.".format(fauna_row[8])
                    ecological_attributes = "{} is a fauna eco attribute.".format(fauna_row[8])
                    biological_attributes = "{} is a fauna bio attribute.".format(fauna_row[8])
                    specific_survey_advice = "{} is a fauna survey advice.".format(fauna_row[8])
                    comments = "{} is a fauna comment.".format(fauna_row[8])
                    conservation_attributes = ConservationAttributes.objects.create(general_management_advice=general_management_advice,
                                                                                    ecological_attributes=ecological_attributes,
                                                                                    biological_attributes=biological_attributes,
                                                                                    specific_survey_advice=specific_survey_advice,
                                                                                    comments=comments,
                                                                                    species=fauna)
                except Exception as e:
                    row_failed = True
                    failed_rows.append(fauna_row)
                    print('{}: {}'.format(e, fauna_row))
                    # could write falied_rows to file.

                if not row_failed:
                    conservation_list.save()
                    conservation_category.save()
                    conservation_criteria.save()
                    conservation_status.save()
                    taxonomy.save()
                    fauna.save()
                    species_document
                    conservation_threats.save()
                    conservation_plans.save()
                    distribution.save()
                    conservation_attributes.save()

def create_species_flora():
    """
    This will take a flora data file, create a species entry and save to the database. It is surrounded by try/except
    so if row fails, that row can be recorded as faulty and saved to a file for examination.
    """
    row_failed = False
    failed_rows = []

    data_row = 2
    with open('/home/graeme/workspace/boranga/boranga/components/species_and_communities/tests/flora.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for index, flora_row in enumerate(reader):
            if index >= data_row:
                try:
                    conservation_list = ConservationList.objects.create(name=flora_row[1])
                    conservation_category = ConservationCategory.objects.create(name=flora_row[0].split('.')[2])
                    conservation_criteria = ConservationCriteria.objects.create(name=flora_row[4])
                    conservation_status = ConservationStatus.objects.create(conservation_list=conservation_list,
                                                                            conservation_category=conservation_category,
                                                                            conservation_criteria=conservation_criteria)

                    taxon = flora_row[6]
                    taxon_id = randrange(5000)
                    family = flora_row[6]
                    genus = flora_row[6]
                    phylogenetic_group = flora_row[6]
                    name_authority = "WA Museum"
                    taxonomy = Taxonomy.objects.create(taxon=taxon,
                                                    taxon_id=taxon_id,
                                                    family=family,
                                                    genus=genus,
                                                    phylogenetic_group=phylogenetic_group,
                                                    name_authority=name_authority,)

                    group_type = GroupType.objects.get(name=GroupType.GROUP_TYPES[0][0])
                    flora = Species.objects.create(common_name=flora_row[7],
                                                group_type=group_type,
                                                scientific_name = flora_row[6],
                                                conservation_status = conservation_status,
                                                region = randrange(500),
                                                district = randrange(100),
                                                image = "path/to/flora.jpg",
                                                taxonomy = taxonomy

                    )

                    species_id = flora.id
                    category_id = conservation_category.id
                    status = flora_row[4]
                    document = "{}.pdf".format(flora_row[5])
                    document_description = "{}.pdf".format(flora_row[5])
                    species_document = SpeciesDocument.objects.create(species_id=species_id,
                                                                    category_id=category_id,
                                                                    status=status,
                                                                    document=document,
                                                                    document_description=document_description,)
                    species_document.species.add(flora)

                    species_id = flora.id
                    threat_category_id = randrange(1000)
                    threat_description = flora_row[3]
                    comment = "{} is flora".format(flora_row[8])
                    document = "{}.pdf".format(flora_row[5])
                    source = "WA Museum"
                    conservation_threats = ConservationThreat(species_id=species_id,
                                                            threat_category_id=threat_category_id,
                                                            threat_description=threat_description,
                                                            comment=comment,
                                                            document=document,
                                                            source=source,)
                    
                    _type = "Regular"
                    threat_category_id = randrange(10000)
                    region_id = randrange(1000)
                    district_id = randrange(100)
                    comment = "{} is a flora plan.".format(flora_row[8])
                    source = "WA Museum"
                    conservation_plans = ConservationPlan.objects.create(threat_category_id=threat_category_id,
                                                                        region_id=region_id,
                                                                        district_id=district_id,
                                                                        type=_type,
                                                                        comment=comment,
                                                                        source=source,)
                    conservation_plans.species.add(flora)

                    department_file_numbers = flora_row[3]
                    community_original_area = randrange(10000)
                    community_original_area_accuracy = randrange(1000)
                    number_of_occurrences = randrange(100)
                    extent_of_occurrences = randrange(100)
                    area_of_occupancy = randrange(100)
                    number_of_iucn_locations = randrange(100)
                    community_original_area_reference = flora_row[7]
                    distribution = Distribution.objects.create(department_file_numbers=department_file_numbers,
                                                            community_original_area=community_original_area,
                                                            community_original_area_accuracy=community_original_area_accuracy,
                                                            number_of_occurrences=number_of_occurrences,
                                                            extent_of_occurrences=extent_of_occurrences,
                                                            area_of_occupancy=area_of_occupancy,
                                                            number_of_iucn_locations=number_of_iucn_locations,
                                                            community_original_area_reference=community_original_area_reference,
                                                            species=flora)

                    general_management_advice = "{} is a flora gen management advice.".format(flora_row[8])
                    ecological_attributes = "{} is a flora eco attribute.".format(flora_row[8])
                    biological_attributes = "{} is a flora bio attribute.".format(flora_row[8])
                    specific_survey_advice = "{} is a flora survey advice.".format(flora_row[8])
                    comments = "{} is a flora comment.".format(flora_row[8])
                    conservation_attributes = ConservationAttributes.objects.create(general_management_advice=general_management_advice,
                                                                                    ecological_attributes=ecological_attributes,
                                                                                    biological_attributes=biological_attributes,
                                                                                    specific_survey_advice=specific_survey_advice,
                                                                                    comments=comments,
                                                                                    species=flora)
                except Exception as e:
                    row_failed = True
                    failed_rows.append(flora_row)
                    print('{}: {}'.format(e, flora_row))
                    # could write falied_rows to file.

                if not row_failed:
                    conservation_list.save()
                    conservation_category.save()
                    conservation_criteria.save()
                    conservation_status.save()
                    taxonomy.save()
                    flora.save()
                    species_document
                    conservation_threats.save()
                    conservation_plans.save()
                    distribution.save()
                    conservation_attributes.save()

