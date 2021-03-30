from django.db import models

# Create your models here.
class RawReport(models.Model):
    company = models.ForeignKey()
    