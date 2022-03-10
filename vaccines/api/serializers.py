from datetime import date, datetime, timedelta
from rest_framework import serializers

from .. import models


class VaccinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vaccine
        fields = "__all__"


class VaccineRecordSerializer(serializers.ModelSerializer):
    doses_taken = serializers.SerializerMethodField()
    next_dose = serializers.SerializerMethodField()

    class Meta:
        model = models.VaccineRecord
        fields = "__all__"

    def get_doses_taken(self, record):
        doses = models.Dose.objects.filter(
            vaccine_records_id=record.id
        ).count()
        return doses

    def get_next_dose(self, record):
        doses = models.Dose.objects.filter(
            vaccine_records_id=record.id
        ).order_by("-date")

        if doses.count() <= 0:
            return date().today()

        else:
            latest_date = doses[0].date
            vaccine = models.Vaccine.objects.get(id=doses[0].vaccine.id)
            return latest_date + timedelta(days=vaccine.period)


class DosesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dose
        fields = "__all__"
