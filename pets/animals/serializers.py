from django.forms import ValidationError
from rest_framework import serializers

from animals.models import Animal
from animals.constants import ALLOWED_SPECIES

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['species', 'name', 'age']

    def validate_species(self, value):
        if self.context.method != 'POST':  
            return value
        if value not in ALLOWED_SPECIES:
            raise ValidationError(f"Adding pet of species '{value}' is not allowed")
        return value
