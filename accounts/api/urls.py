from unicodedata import name
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r"users",
    views.UserViewsets,
    basename='users'
)

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login")
] + router.urls
