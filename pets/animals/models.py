from django.db import models

# Create your models here.

SPECIES = [('Cat', 'Cat'), ('Dog', 'Dog')]

class Animal(models.Model):
    species = models.CharField(max_length=100, choices=SPECIES)
    name = models.CharField(max_length=100)
    age = models.IntegerField() #In years
    #Birthdate may make more sense
