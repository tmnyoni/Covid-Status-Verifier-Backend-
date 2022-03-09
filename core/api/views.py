from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .. import models
from . import serializers


class PeopleViewset(viewsets.ViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.Person

    def list(self, request):
        queryset = models.Person.objects.all()
        serializer = serializers.PersonSerializer(queryset, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)
