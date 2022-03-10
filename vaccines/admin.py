from django.contrib import admin
from . import models

admin.site.register(models.Vaccine)
admin.site.register(models.Dose)
