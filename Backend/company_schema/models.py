from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    cik = models.CharField(max_length=50)

    def __str__(self):
        return self.name
