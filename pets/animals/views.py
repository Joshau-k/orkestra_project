from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from animals.models import Animal
from animals.serializers import AnimalSerializer


class AnimalView(APIView):
    def get(self, request, format=None):
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AnimalSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return