from django.contrib.auth.models import User
from django.db import models

from core.models import Person


class Vaccine(models.Model):
    class Meta:
        db_table = "vaccines"

    name = models.CharField(max_length=100)
    manufactured_country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.pk} - {self.name}'


class VaccineRecord(models.Model):
    class Meta:
        db_table = "vaccine-records"

    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}-{self.person}'


class Dose(models.Model):
    class Meta:
        db_table = "doses"

    vaccine_records = models.ForeignKey(
        VaccineRecord,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    date = models.DateField(auto_created=True)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    administered_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} - {self.person}'
