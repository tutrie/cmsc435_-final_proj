from django.db import models
from django.contrib import admin
from django.apps import AppConfig
from rest_framework import serializers, viewsets


class CompanyConfig(AppConfig):
    name = 'company_schema'


class Company(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    cik = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cik')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'name',
            'cik'
        )


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
