from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth import models
from . import serializers


class UserViewsets(viewsets.ViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def list(self, request):
        queryset = models.User.objects.all()
        serializer = serializers.UserSerializer(queryset, many=True)
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
            data={"Success": "User deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=["POST"])
    def create_user_groups(self, request):
        try:
            if request.method == "POST":
                data = request.data

                group_name = data["group_name"]
                #permissions = data["permissions"]

                group = models.Group.objects.create(name=group_name)
                group.save()
                if group:
                    # set permissions.
                    pass

                return Response(
                    data={"Success": "Group added succesfully"},
                    status=status.HTTP_201_CREATED
                )
        except Exception as err:
            return Response(
                data={"Error": err.__str__()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
