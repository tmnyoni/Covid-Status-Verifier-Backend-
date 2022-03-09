from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .. import models
from . import serializers


class PeopleViewset(viewsets.ViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer

    def list(self, request):
        queryset = models.Person.objects.all()
        serializer = serializers.PersonSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
