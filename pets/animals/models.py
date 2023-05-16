from django.db import models

from animals.constants import Species

class LowercaseCharField(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()

# Create your models here.
class Animal(models.Model):
    species = LowercaseCharField(max_length=100, choices=Species.as_tuples())
    name = models.CharField(max_length=100)
    age = models.IntegerField() #In years
    #Birthdate may make more sense
