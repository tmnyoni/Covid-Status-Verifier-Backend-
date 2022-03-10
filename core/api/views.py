from django.shortcuts import get_object_or_404
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
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        object_ = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(object_)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, pk=None):
        object_ = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(
            object_,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        object_ = get_object_or_404(self.queryset, pk=pk)
        object_.delete()
        return Response(
            data={"Success": "Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
