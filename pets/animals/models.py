from django.db import models

from animals.constants import Species

# Create your models here.
class Animal(models.Model):
    species = models.CharField(max_length=100, choices=Species.as_tuples())
    name = models.CharField(max_length=100)
    age = models.IntegerField() #In years
    #Birthdate may make more sense
