from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .. import models
from . import serializers


class VaccinesViewset(viewsets.ViewSet):
    queryset = models.Vaccine.objects.all()
    serializer_class = serializers.VaccinesSerializer

    def list(self, request):
        queryset = models.Vaccine.objects.all()
        serializer = serializers.VaccinesSerializer(queryset, many=True)
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


class VaccineRecordViewset(viewsets.ViewSet):
    queryset = models.VaccineRecord.objects.all()
    serializer_class = serializers.VaccineRecordSerializer

    def list(self, request):
        queryset = models.VaccineRecord.objects.all()
        serializer = serializers.VaccineRecordSerializer(queryset, many=True)
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


class DosesViewset(viewsets.ViewSet):
    queryset = models.Dose.objects.all()
    serializer_class = serializers.DosesSerializer

    def list(self, request):
        queryset = models.Dose.objects.all()
        serializer = serializers.DosesSerializer(queryset, many=True)
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
