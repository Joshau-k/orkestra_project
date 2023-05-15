from rest_framework import serializers

from animals.models import Animal

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['species', 'name', 'age']