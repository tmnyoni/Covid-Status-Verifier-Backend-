from decouple import config
from rest_framework import serializers

from .. import models


class VaccinesSerializer(serializers.Serializer):
    class Meta:
        model = models.Vaccine
        exclude = "__all__"


class DosesSerializer(serializers.Serializer):
    class Meta:
        model = models.Dose
        exclude = "__all__"
