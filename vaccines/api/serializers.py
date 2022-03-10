from datetime import date
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


class VaccineRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VaccineRecord
        fields = "__all__"
