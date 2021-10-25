from django.db import models
from django.contrib import admin
from django.apps import AppConfig
from rest_framework import serializers, viewsets


class CompanyConfig(AppConfig):
    """Configures the name of this application

    Inherits from the predefined AppConfig class.
    """
    name = 'company_schema'


class Company(models.Model):
    """Defines the company model in our database

    Inherits from the predefined model class.
    """
    name = models.CharField(primary_key=True, max_length=50)
    cik = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Defines what parameters from the company model should be displayed on the admin panel.

    Inherits from the predefined model admin class.
    """
    list_display = ('name', 'cik')


class CompanySerializer(serializers.ModelSerializer):
    """Serializes the company model in the database, converting a row to a json object and vice versa.

    Inherits from the predefined model serializer.
    """
    class Meta:
        model = Company
        fields = (
            'name',
            'cik'
        )


class CompanyViewSet(viewsets.ModelViewSet):
    """Defines the API Endpoint for the company model in the database.
    
    Inherits from the predefined model viewset.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
