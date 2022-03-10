from decouple import config
from rest_framework import serializers

from .. import models


class VaccinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vaccine
        fields = "__all__"


class DosesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dose
        fields = "__all__"
