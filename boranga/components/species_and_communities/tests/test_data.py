from django.db.models import DateField
from django.test import TestCase

# Create your tests here.
from boranga.components.species_and_communities.models import Species, GroupType, ConservationStatus, ConservationList, \
    ConservationCategory, ConservationCriteria, Taxonomy, Community, SpeciesDocument, ConservationThreat, \
    ConservationPlan, Distribution, ConservationAttributes

def create_test_data():
    print('----------------------------------------------------')
    print('--------------ADDING TEST DATA----------------------')
    print('----------------------------------------------------')
    create_group_types()
    create_species_fauna()
    create_species_flora()
    create_community()

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

    conservation_list = ConservationList.objects.create(name="ConservationList")
    conservation_category = ConservationCategory.objects.create(name="ConservationCategory")
    conservation_criteria = ConservationCriteria.objects.create(name="ConservationCriteria")
    conservation_status = ConservationStatus.objects.create(conservation_list=conservation_list,
                                                            conservation_category=conservation_category,
                                                            conservation_criteria=conservation_criteria)

    group_type = GroupType.objects.create(name=GroupType.GROUP_TYPES[1][0])

    taxon = "Pussy Cat"
    taxon_id = 666
    previous_name = "N/A"
    family = "Muller"
    genus = "Felix"
    phylogenetic_group = "Felus"
    name_authority = "No Idea1-1"
    community_id = 17
    community_number = 18
    community_description = "South-west biodiversity region."
    taxonomy = Taxonomy.objects.create(taxon=taxon,
                                       taxon_id=taxon_id,
                                       previous_name=previous_name,
                                       family=family,
                                       genus=genus,
                                       phylogenetic_group=phylogenetic_group,
                                       name_authority=name_authority,
                                       community_id=community_id,
                                       community_number=community_number,
                                       community_description=community_description,)

    cat = Species.objects.create(common_name="Cat",
                                 group_type = group_type,
                                 scientific_name = "Puss",
                                 name_currency = "No Idea 1",
                                 conservation_status = conservation_status,
                                 region = 1,
                                 district = 1,
                                 image = "path/to/cat.jog",
                                 processing_status = "Complete 1",
                                 taxonomy = taxonomy

    )



    community_name = "Graeme's House"
    community_id = 17
    community_status = "Safe"
    region = 1
    district = 1
    conservation_status = "Priority"
    community = Community.objects.create(community_name=community_name,
                                         community_id=community_id,
                                         community_status=community_status,
                                         region=region,
                                         district=district,)
    community.species.add(cat)
    community.save()

    species_id = cat.id
    category_id = 11
    status = "Priority"
    document = "cat_doc.pdf"
    document_description = "A document describing the endangered status of a cat."
    species_document = SpeciesDocument.objects.create(species_id=species_id,
                                                      category_id=category_id,
                                                      status=status,
                                                      document=document,
                                                      document_description=document_description,)
    species_document.species.add(cat)
    species_document.save()
    species_id = cat.id
    threat_category_id = 1111
    threat_description = "Not very dangerous."
    comment = "Not much to say."
    document = "cat_threat_document.docx"
    source = "Public"
    conservation_threats = ConservationThreat(species_id=species_id,
                                              threat_category_id=threat_category_id,
                                              threat_description=threat_description,
                                              comment=comment,
                                              document=document,
                                              source=source,)
    conservation_threats.save()
    _type = "Regular"
    threat_category_id = 11111
    region_id = 11
    district_id = 111
    comment = "Making too much noise."
    source = "Public"
    conservation_plans = ConservationPlan.objects.create(threat_category_id=threat_category_id,
                                                         region_id=region_id,
                                                         district_id=district_id,
                                                         type=_type,
                                                         comment=comment,
                                                         source=source,)
    conservation_plans.species.add(cat)
    conservation_plans.save()

    department_file_numbers = "123, 234, 345"
    community_original_area = 10
    community_original_area_accuracy = 0.5
    number_of_occurrences = 3
    extent_of_occurrences = 5
    area_of_occupancy = 20
    number_of_iucn_locations = 5
    community_original_area_reference = "South West"
    distribution = Distribution.objects.create(department_file_numbers=department_file_numbers,
                                               community_original_area=community_original_area,
                                               community_original_area_accuracy=community_original_area_accuracy,
                                               number_of_occurrences=number_of_occurrences,
                                               extent_of_occurrences=extent_of_occurrences,
                                               area_of_occupancy=area_of_occupancy,
                                               number_of_iucn_locations=number_of_iucn_locations,
                                               community_original_area_reference=community_original_area_reference,
                                               species=cat)
    distribution.save()

    general_management_advice = "Give them food."
    ecological_attributes = "Too many of them."
    biological_attributes = "Very cuddly."
    specific_survey_advice = "Cuddle them."
    comments = "Very nice animals."
    conservation_attributes = ConservationAttributes.objects.create(general_management_advice=general_management_advice,
                                                                    ecological_attributes=ecological_attributes,
                                                                    biological_attributes=biological_attributes,
                                                                    specific_survey_advice=specific_survey_advice,
                                                                    comments=comments,
                                                                    species=cat)
    conservation_attributes.save()

def create_species_fauna_no_community():

    conservation_list = ConservationList.objects.create(name="ConservationListFauna_no_community")
    conservation_category = ConservationCategory.objects.create(name="ConservationCategory_no_community")
    conservation_criteria = ConservationCriteria.objects.create(name="ConservationCriteria_no_community")
    conservation_status = ConservationStatus.objects.create(conservation_list=conservation_list,
                                                            conservation_category=conservation_category,
                                                            conservation_criteria=conservation_criteria)

    group_type = GroupType.objects.create(name=GroupType.GROUP_TYPES[1][0])

    taxon = "Dog"
    taxon_id = 966
    previous_name = "K9"
    family = "Puppy"
    genus = "Pooch"
    phylogenetic_group = "PuppusDoggus"
    name_authority = "Vet"
    community_id = 19
    community_number = 20
    community_description = "West biodiversity region."
    taxonomy = Taxonomy.objects.create(taxon=taxon,
                                       taxon_id=taxon_id,
                                       previous_name=previous_name,
                                       family=family,
                                       genus=genus,
                                       phylogenetic_group=phylogenetic_group,
                                       name_authority=name_authority,
                                       community_id=community_id,
                                       community_number=community_number,
                                       community_description=community_description,)

    dog = Species.objects.create(common_name="Doggy",
                                 group_type = group_type,
                                 scientific_name = "Doggus",
                                 name_currency = "Good",
                                 conservation_status = conservation_status,
                                 region = 1,
                                 district = 1,
                                 image = "path/to/dog.jog",
                                 processing_status = "LOLOL 1",
                                 taxonomy = taxonomy

    )

    species_id = dog.id
    category_id = 11
    status = "Priority"
    document = "cat_doc.pdf"
    document_description = "A document describing the endangered status of a dog."
    species_document = SpeciesDocument.objects.create(species_id=species_id,
                                                      category_id=category_id,
                                                      status=status,
                                                      document=document,
                                                      document_description=document_description,)
    species_document.species.add(dog)
    species_document.save()
    species_id = dog.id
    threat_category_id = 1122
    threat_description = "Bark bark."
    comment = "Feed ne."
    document = "dog_threat_document.docx"
    source = "Public"
    conservation_threats = ConservationThreat(species_id=species_id,
                                              threat_category_id=threat_category_id,
                                              threat_description=threat_description,
                                              comment=comment,
                                              document=document,
                                              source=source,)
    conservation_threats.save()
    _type = "Thing"
    threat_category_id = 1441
    region_id = 114
    district_id = 1114
    comment = "Making poos."
    source = "Public"
    conservation_plans = ConservationPlan.objects.create(threat_category_id=threat_category_id,
                                                         region_id=region_id,
                                                         district_id=district_id,
                                                         type=_type,
                                                         comment=comment,
                                                         source=source,)
    conservation_plans.species.add(dog)
    conservation_plans.save()

    department_file_numbers = "444"
    community_original_area = 1
    community_original_area_accuracy = 0.75
    number_of_occurrences = 6
    extent_of_occurrences = 3
    area_of_occupancy = 2
    number_of_iucn_locations = 500
    community_original_area_reference = "South West"
    distribution = Distribution.objects.create(department_file_numbers=department_file_numbers,
                                               community_original_area=community_original_area,
                                               community_original_area_accuracy=community_original_area_accuracy,
                                               number_of_occurrences=number_of_occurrences,
                                               extent_of_occurrences=extent_of_occurrences,
                                               area_of_occupancy=area_of_occupancy,
                                               number_of_iucn_locations=number_of_iucn_locations,
                                               community_original_area_reference=community_original_area_reference,
                                               species=dog)
    distribution.save()

    general_management_advice = "Give  food."
    ecological_attributes = "Hug them."
    biological_attributes = "Very barky."
    specific_survey_advice = "Cuddle."
    comments = "Good dog."
    conservation_attributes = ConservationAttributes.objects.create(general_management_advice=general_management_advice,
                                                                    ecological_attributes=ecological_attributes,
                                                                    biological_attributes=biological_attributes,
                                                                    specific_survey_advice=specific_survey_advice,
                                                                    comments=comments,
                                                                    species=dog)
    conservation_attributes.save()

def create_species_flora():

    conservation_list = ConservationList.objects.create(name="ConservationListFlora")
    conservation_category = ConservationCategory.objects.create(name="ConservationCategoryFlora")
    conservation_criteria = ConservationCriteria.objects.create(name="ConservationCriteriaFlora")
    conservation_status = ConservationStatus.objects.create(conservation_list=conservation_list,
                                                            conservation_category=conservation_category,
                                                            conservation_criteria=conservation_criteria)
   
    group_type = GroupType.objects.create(name=GroupType.GROUP_TYPES[0][0])

    taxon = "Rose"
    taxon_id = 777
    previous_name = "N/A"
    family = "Rosa"
    genus = "Flower"
    phylogenetic_group = "RosusFlowerus"
    name_authority = "WA Museum"
    community_id = 12
    community_number = 19
    community_description = "North-west biodiversity region."
    taxonomy = Taxonomy.objects.create(taxon=taxon,
                                       taxon_id=taxon_id,
                                       previous_name=previous_name,
                                       family=family,
                                       genus=genus,
                                       phylogenetic_group=phylogenetic_group,
                                       name_authority=name_authority,
                                       community_id=community_id,
                                       community_number=community_number,
                                       community_description=community_description,)

    rose = Species.objects.create(common_name="Rose",
                                  group_type = group_type,
                                  scientific_name = "RosusFlowerus",
                                  name_currency = "No Idea Flora",
                                  conservation_status = conservation_status,
                                  region = 2,
                                  district = 2,
                                  image = "path/to/rose.jog",
                                  processing_status = "Complete 2",
                                  taxonomy = taxonomy

    )



    community_name = "Garden"
    community_id = 22
    community_status = "Weed problem"
    region = 2
    district = 2
    conservation_status = "Endangered"
    community = Community.objects.create(community_name=community_name,
                                         community_id=community_id,
                                         community_status=community_status,
                                         region=region,
                                         district=district,)
    community.species.add(rose)
    community.save()

    species_id = rose.id
    category_id = 11
    status = "Priority"
    document = "rose_doc.pdf"
    document_description = "A document describing the endangered status of a rose."
    species_document = SpeciesDocument.objects.create(species_id=species_id,
                                                      category_id=category_id,
                                                      status=status,
                                                      document=document,
                                                      document_description=document_description,)
    species_document.species.add(rose)
    species_document.save()
    species_id = rose.id
    threat_category_id = 2222
    threat_description = "Prickly"
    comment = "Blah blah"
    document = "rose_threat_document.docx"
    source = "Museum"
    conservation_threats = ConservationThreat(species_id=species_id,
                                              threat_category_id=threat_category_id,
                                              threat_description=threat_description,
                                              comment=comment,
                                              document=document,
                                              source=source,)
    conservation_threats.save()

    _type = "Special"
    threat_category_id = 3333
    region_id = 22
    district_id = 33
    comment = "Smells nice"
    source = "Person"
    conservation_plans = ConservationPlan.objects.create(threat_category_id=threat_category_id,
                                                         region_id=region_id,
                                                         district_id=district_id,
                                                         type=_type,
                                                         comment=comment,
                                                         source=source,)
    conservation_plans.species.add(rose)
    conservation_plans.save()

    department_file_numbers = "666, 777, 888"
    community_original_area = 12
    community_original_area_accuracy = 2.5
    number_of_occurrences = 10
    extent_of_occurrences = 50
    area_of_occupancy = 200
    number_of_iucn_locations = 7
    community_original_area_reference = "North West"
    distribution = Distribution.objects.create(department_file_numbers=department_file_numbers,
                                               community_original_area=community_original_area,
                                               community_original_area_accuracy=community_original_area_accuracy,
                                               number_of_occurrences=number_of_occurrences,
                                               extent_of_occurrences=extent_of_occurrences,
                                               area_of_occupancy=area_of_occupancy,
                                               number_of_iucn_locations=number_of_iucn_locations,
                                               community_original_area_reference=community_original_area_reference,
                                               species=rose)
    distribution.save()

    general_management_advice = "Water them"
    ecological_attributes = "Pretty"
    biological_attributes = "Nice"
    specific_survey_advice = "Pick them"
    comments = "Pretty nice smelling flower"
    conservation_attributes = ConservationAttributes.objects.create(general_management_advice=general_management_advice,
                                                                    ecological_attributes=ecological_attributes,
                                                                    biological_attributes=biological_attributes,
                                                                    specific_survey_advice=specific_survey_advice,
                                                                    comments=comments,
                                                                    species=rose)
    conservation_attributes.save()

def create_species_flora_no_community():

    conservation_list = ConservationList.objects.create(name="ConservationListFloraNoCom")
    conservation_category = ConservationCategory.objects.create(name="ConservationCategoryFloraNoCom")
    conservation_criteria = ConservationCriteria.objects.create(name="ConservationCriteriaFloraNoCom")
    conservation_status = ConservationStatus.objects.create(conservation_list=conservation_list,
                                                            conservation_category=conservation_category,
                                                            conservation_criteria=conservation_criteria)
   
    group_type = GroupType.objects.create(name=GroupType.GROUP_TYPES[0][0])

    taxon = "Tulip"
    taxon_id = 755
    previous_name = "N/A"
    family = "Ta"
    genus = "FlowerPlant"
    phylogenetic_group = "TupipusFlowerus"
    name_authority = "Herbarium"
    community_id = 12
    community_number = 19
    community_description = "Perth biodiversity region."
    taxonomy = Taxonomy.objects.create(taxon=taxon,
                                       taxon_id=taxon_id,
                                       previous_name=previous_name,
                                       family=family,
                                       genus=genus,
                                       phylogenetic_group=phylogenetic_group,
                                       name_authority=name_authority,
                                       community_id=community_id,
                                       community_number=community_number,
                                       community_description=community_description,)

    tuli = Species.objects.create(common_name="Tulip",
                                  group_type = group_type,
                                  scientific_name = "TulipFlowerus",
                                  name_currency = "No Idea Tulip",
                                  conservation_status = conservation_status,
                                  region = 25,
                                  district = 29,
                                  image = "path/to/Tulip.jog",
                                  processing_status = "Complete Tulip",
                                  taxonomy = taxonomy

    )

    species_id = tuli.id
    category_id = 11
    status = "Priority"
    document = "rose_doc.pdf"
    document_description = "A document describing the endangered status of a rose."
    species_document = SpeciesDocument.objects.create(species_id=species_id,
                                                      category_id=category_id,
                                                      status=status,
                                                      document=document,
                                                      document_description=document_description,)
    species_document.species.add(tuli)
    species_document.save()
    species_id = rose.id
    threat_category_id = 2222
    threat_description = "Nice"
    comment = "Blah Bam bam"
    document = "tulip_threat_document.docx"
    source = "Herbarium"
    conservation_threats = ConservationThreat(species_id=species_id,
                                              threat_category_id=threat_category_id,
                                              threat_description=threat_description,
                                              comment=comment,
                                              document=document,
                                              source=source,)
    conservation_threats.save()

    _type = "Nice"
    threat_category_id = 33335
    region_id = 225
    district_id = 335
    comment = "Smells"
    source = "Goat"
    conservation_plans = ConservationPlan.objects.create(threat_category_id=threat_category_id,
                                                         region_id=region_id,
                                                         district_id=district_id,
                                                         type=_type,
                                                         comment=comment,
                                                         source=source,)
    conservation_plans.species.add(rose)
    conservation_plans.save()

    department_file_numbers = "0, 8, 5, 7"
    community_original_area = 129
    community_original_area_accuracy = 2.55
    number_of_occurrences = 105
    extent_of_occurrences = 505
    area_of_occupancy = 2005
    number_of_iucn_locations = 75
    community_original_area_reference = "North"
    distribution = Distribution.objects.create(department_file_numbers=department_file_numbers,
                                               community_original_area=community_original_area,
                                               community_original_area_accuracy=community_original_area_accuracy,
                                               number_of_occurrences=number_of_occurrences,
                                               extent_of_occurrences=extent_of_occurrences,
                                               area_of_occupancy=area_of_occupancy,
                                               number_of_iucn_locations=number_of_iucn_locations,
                                               community_original_area_reference=community_original_area_reference,
                                               species=tuli)
    distribution.save()

    general_management_advice = "Water"
    ecological_attributes = "Pretty"
    biological_attributes = "Nice"
    specific_survey_advice = "Pick "
    comments = "Nice smelling flower"
    conservation_attributes = ConservationAttributes.objects.create(general_management_advice=general_management_advice,
                                                                    ecological_attributes=ecological_attributes,
                                                                    biological_attributes=biological_attributes,
                                                                    specific_survey_advice=specific_survey_advice,
                                                                    comments=comments,
                                                                    species=tuli)
    conservation_attributes.save()