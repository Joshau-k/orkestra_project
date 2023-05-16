from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.db.models.query_utils import Q
import json

from animals.models import Animal
from animals.serializers import AnimalSerializer


class AnimalView(APIView):
    def get(self, request:Request, format=None):
        species = request.GET.get('species')
        name = request.GET.get('name')
        age = request.GET.get('age')

        query = Q()
        if species:
            query &= Q(species__iexact=species)
        if name:
            query &= Q(name__iexact=name)
        if age:
            query &= Q(age__iexact=age)

        animals = Animal.objects.filter(query)
        serializer = AnimalSerializer(animals, many=True, context=request)
        return Response(serializer.data)

    def post(self, request:Request, format=None):
        data = request.data
        if 'species' in request.data:
            data = request.data.copy()
            data['species'] = data['species'].lower()
        serializer = AnimalSerializer(data=data, many=False, context=request)
        
        if not serializer.is_valid():
            return Response(json.dumps(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)