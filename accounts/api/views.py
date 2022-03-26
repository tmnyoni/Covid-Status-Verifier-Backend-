from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import(
    models,
    authenticate
)
from django.middleware import csrf

from rest_framework import( 
    status,
    viewsets,
    views
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


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
        except Exception as error:
            return Response(
                data={"Error": error},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def get_user_token(user):
    tokens = RefreshToken.for_user(user)
    return {
        "refresh": str(tokens),
        "access": str(tokens.access_token)
    }


class LoginView(views.APIView):
    """
    Handles the login.

    It authenticate the user and creates a token for the user
    and then it creates the HTTP_Cookie.
    """
    
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = request.data
        response = Response()

        username = data.get("username")
        password = data.get("password")

        if username is None or password is None:
            return Response(
                {"error": "Please provide both username and password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                data = get_user_token(user)

                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )

                csrf.get_token(request)
                response.data = {"Success": "Logged in successfully"}
                return response

        else:
            return Response(
                {"error": "Invalid Credentials"},
                status=status.HTTP_404_NOT_FOUND
            )