# from django.db import models
# from django.db.models.deletion import CASCADE
# from enumerations import GroupTypes
#
#
# class GroupType(models.Model):
#     """
#
#     """
#     id = models.IntegerField(default=-1)
#     name = models.CharField(max_length=4,
#                             choices=GroupTypes.choices,
#                             default=GroupTypes.FAUNA,)
#
#
# class ConservationList(models.Model):
#     id = models.IntegerField(default=-1)
#     name = models.CharField(max_length=4,
#                             default="None")
#
#
# class ConservationCategory(models.Model):
#     id = models.IntegerField(default=-1)
#     name = models.CharField(max_length=4,
#                             default="None")
#
#
# class ConservationCriteria(models.Model):
#     id = models.IntegerField(default=-1)
#     name = models.CharField(max_length=4,
#                             default="None")
#
#
# class ConservationStatus(models.Model):
#     id = models.IntegerField(default=-1)
#     conservation_list_id = models.ForeignKey(to=ConservationList, on_delete=CASCADE)
#     conservation_category_id = models.ForeignKey(to=ConservationCategory, on_delete=CASCADE)
#     conservation_criteria_id = models.ForeignKey(to=ConservationCriteria, on_delete=CASCADE)
#
#
# class Community(models.Model):
#     id = models.IntegerField(default=-1)
#     community_name = models.CharField(max_length=128,
#                                       default="None")
#     community_id = models.IntegerField(default=-1)
#     community_status
#     region_id = models.IntegerField(default=-1)
#     district_id = models.IntegerField(default=-1)
#
#
# class Species(models.Model):
#
#     species_id = models.IntegerField(default=-1)
#     name_id = models.IntegerField(default=-1)
#     scientific_name = models.CharField(max_length=128,
#                                        default="None")
#     common_name = models.CharField(max_length=128,
#                                    default="None")
#
#     name_currency
#
#     conservation_status_id
#
#     region_id
#
#     district_id
#
#     species_image
#
#     processing_status
#
#
#
#     group_type_id = models.ForeignKey(to=GroupType, on_delete=CASCADE)
#
#
#
#
