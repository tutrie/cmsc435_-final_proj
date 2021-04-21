from django.db import models
from django.contrib import admin
from django.apps import AppConfig
from rest_framework import viewsets
from rest_framework import serializers

from company_schema.models import Company, CompanySerializer


class RawReport(models.Model):
    """Defines the RawReport model in our database

    Inherits from the predefined model class.
    """
    company = models.ForeignKey(Company, on_delete=models.deletion.CASCADE)
    report_date = models.DateField()
    parsed_json = models.JSONField(blank=True, null=True)
    excel_url = models.URLField()

    def __str__(self):
        return f'Report from {self.report_date} for {self.company}'


@admin.register(RawReport)
class RawReportAdmin(admin.ModelAdmin):
    list_display = ('company', 'report_date', 'excel_url')


class ReportSchemaConfig(AppConfig):
    """Configures the name of this application

    Inherits from the predefined AppConfig class.
    """
    name = 'report_schema'


class RawReportSerializer(serializers.ModelSerializer):
    """Serializes the RawReport model in the database, converting a row to a json object and vice versa.

    Inherits from the predefined model serializer.
    """

    class Meta:
        model = RawReport
        fields = (
            'company',
            'report_date',
            'excel_url'
        )

    # Overwrite how the company field is serialized
    def to_representation(self, instance):
        self.fields['company'] = CompanySerializer()
        return super(RawReportSerializer, self).to_representation(instance)


class RawReportViewSet(viewsets.ModelViewSet):
    """Defines the API Endpoint for the RawReports model in the database.
    
    Inherits from the predefined model viewset.
    """
    queryset = RawReport.objects.all()
    serializer_class = RawReportSerializer
