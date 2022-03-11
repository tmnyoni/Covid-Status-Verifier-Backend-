from ast import Try
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .. import models
from . import serializers
from ..utils import generate_hmac_code


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
        try:
            data = request.data

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            # Creating a user account for each
            # person during person creation.
            username = serializer.validated_data["national_id"]
            password = "pass"

            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "Username already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create(
                username=username,
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                email=serializer.validated_data["email_address"]
            )

            # Saving both the newly added  person and
            # their user account, after doing validation.
            serializer.save()
            user.set_password(password)
            user.save()

            # Sending credentials to the person
            # so that they can access their account.
            subject = "Covid-19 Vaccination Profile"
            message = f"""
            Dear {serializer.validated_data["first_name"]}

            Thank you for vaccinating.
            Find a copy of your credentials to use to access
            your profile account.

            Username: {username}
            Password: {password}

            Thank you
            Ministry of Health and Child care
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[serializer.validated_data["email_address"], ]
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": e.__str__()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

            # Get the object (Person) and re-create
            # the code using the key.
            object_ = get_object_or_404(self.queryset, pk=pk)
            object_qrcode = generate_hmac_code(object_.national_id)

            qrcode = request.data["qrcode"]
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


class StakeHoldersViewset(viewsets.ViewSet):
    queryset = models.StakeHolder.objects.all()
    serializer_class = serializers.StakeHoldersSerializer

    def list(self, request):
        queryset = models.StakeHolder.objects.all()
        serializer = serializers.StakeHoldersSerializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def create(self, request):
        try:
            data = request.data

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            # Creating a user account for each
            # stakeholder during creation.
            username = serializer.validated_data["username"]
            password = "pass"

            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "Username already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create(
                username=username,
                first_name=serializer.validated_data["organisation"],
                last_name=serializer.validated_data["branch"],
                email=serializer.validated_data["email_address"],
                is_staff=True  # all stakeholders are staff members.
            )

            # Saving both the newly added  stakeholder and
            # their user account, after doing validation.
            serializer.save()
            user.set_password(password)
            user.save()

            # After adding the user, assign it
            # to a certain group of users.
            try:
                group = Group.objects.get(name="stakeholders")
                if group:
                    user.groups.add(group)
            except:
                pass

            # Sending credentials to the stakeholder
            # so that they can access their account.
            subject = "Covid-19 Vaccination Profile"
            message = f"""
            Dear {serializer.validated_data["organisation"]}

            Thank you for vaccinating.
            Find a copy of your credentials to use to access
            your profile account.

            Username: {username}
            Password: {password}

            Thank you
            Ministry of Health and Child care
            """

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[serializer.validated_data["email_address"], ]
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"Error": e.__str__()},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
