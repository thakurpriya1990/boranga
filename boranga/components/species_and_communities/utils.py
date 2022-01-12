from django.db import models
from django.db.models.deletion import CASCADE

class GroupType():
    id = models.IntegerField(default=-1)
    name = models.CharField(max_length=4,
                            default="None")

class Species(models.Model):
    
    species_id = models.IntegerField(default=-1)
    name_id = models.IntegerField(default=-1)
    scientific_name = models.CharField(max_length=128,
                                       default="None")
    common_name = models.CharField(max_length=128,
                                   default="None")
    



    group_type_id = models.ForeignKey(to=GroupType, on_delete=CASCADE)




