from pyexpat import model
from statistics import mode
from django.db import models


class Person(models.Model):
    class Meta:
        db_table = "people"

    image = models.ImageField(null=True, blank=True, upload_to="people")
    national_id = models.CharField(primary_key=True, max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    home_address = models.CharField(max_length=200)
    email_address = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)
    vaccinate = models.BooleanField(default=True)

    def __str__(self):
        return str(self.national_id)


class StakeHolder(models.Model):
    class Meta:
        db_table = "stakeholders"

    organisation = models.CharField(max_length=100)
    representative_name = models.CharField(max_length=50)
    representative_id = models.CharField(max_length=50)
    contacts = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
