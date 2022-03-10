import hashlib
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

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

    @action(detail=True, methods=["post"])
    def recognize_qrcode(self, request, pk=None):
        if request.method == "POST":

            if "qrcode" not in request.data:
                return Response(
                    data={"Error": "Field qrcode required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            qrcode = request.data["qrcode"]
            object_ = get_object_or_404(self.queryset, pk=pk)
            object_qrcode = hashlib.sha3_512(
                object_.national_id.encode()
            ).hexdigest()

            if qrcode == object_qrcode:
                return Response(
                    data={"Success": "Qrcode verified"},
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    data={"Error": "Qrcode Verification failed"},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            data={"Error": "Something happened"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @action(detail=True, methods=["post"])
    def recognize_face(self, request, pk=None):
        if request.method == "POST":
            if "image" not in request.data:
                return Response(
                    data={"Error": "Field image required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            '''
            # logic to recognise the faces.
            if image == object_face:
                return Response(
                    data={"Success": "Qrcode verified"},
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    data={"Error": "Qrcode Verification failed"},
                    status=status.HTTP_404_NOT_FOUND
                )
            '''

        return Response(
            data={"Error": "Something happened"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
