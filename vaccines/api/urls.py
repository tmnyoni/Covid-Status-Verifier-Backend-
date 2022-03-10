from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r"vaccines",
    views.VaccinesViewset,
    basename='vaccines'
)

router.register(
    r"vaccine-records",
    views.VaccineRecordViewset,
    basename='vaccine-records'
)

router.register(
    r"doses",
    views.DosesViewset,
    basename='doses'
)

urlpatterns = router.urls
