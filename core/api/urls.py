from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"people", views.PeopleViewset, basename='people')
urlpatterns = router.urls
