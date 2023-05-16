from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.db.models.query_utils import Q

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
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data)

    def post(self, request:Request, format=None):
        serializer = AnimalSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return