from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.apps import AppConfig
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.request import Request

from company_schema.models import Company, CompanySerializer


class RawReport(models.Model):
    """Defines the RawReport model in our database

    Inherits from the predefined model class.
    """
    company = models.ForeignKey(Company, on_delete=models.deletion.CASCADE)
    report_date = models.DateField()
    report_type = models.CharField(max_length=4)
    parsed_json = models.JSONField(blank=True, null=True)
    excel_url = models.URLField()

    # Overwrite default save method
    def save(self, *args, **kwargs):
        """This function overwrites the default save method for this model.
        It is automatically called by django when it attempts to save an object into the database.

        Raises:
            ValidationError: [description]
        """
        report_type_is_valid = self.report_type == '10-Q' or self.report_type == '10-K'
        if not report_type_is_valid:
            raise ValidationError('Report Type not Valid.')

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Report {self.report_type} from {self.report_date} for {self.company}'


@admin.register(RawReport)
class RawReportAdmin(admin.ModelAdmin):
    """Defines what parameters from the raw report model should be displayed on the admin panel.

    Inherits from the predefined model admin class.
    """
    list_display = ('company', 'report_date', 'report_type', 'excel_url')


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
            'report_type',
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
