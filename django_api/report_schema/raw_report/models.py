from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.apps import AppConfig
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import action

from company_schema.models import Company, CompanySerializer
from . import utils


class RawReport(models.Model):
    company = models.ForeignKey(Company, on_delete=models.deletion.CASCADE)
    report_date = models.DateField()
    report_type = models.CharField(max_length=4)
    parsed_json = models.JSONField(blank=True, null=True)
    excel_url = models.URLField()

    # Overwrite default save method
    def save(self, *args, **kwargs):
        report_type_is_valid = self.report_type == '10-Q' or self.report_type == '10-K'
        if not report_type_is_valid:
            raise ValidationError('Report Type not Valid.')

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Report {self.report_type} from {self.report_date} for {self.company}'


@admin.register(RawReport)
class RawReportAdmin(admin.ModelAdmin):
    list_display = ('company', 'report_date', 'report_type', 'excel_url')


class ReportSchemaConfig(AppConfig):
    name = 'report_schema'


class RawReportSerializer(serializers.ModelSerializer):
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
    """
    API endpoint that allows users to create and retrieve raw reports.
    """
    queryset = RawReport.objects.all()
    serializer_class = RawReportSerializer


    @action(methods=['GET'], detail=False, url_path='get_raw_reports', url_name='get_raw_reports')
    def get_raw_reports(self, request) -> Response:

        # check that request is valid
        is_valid, msg = request_is_valid()
        if not is_valid:
            return Response(json.dumps(msg), status=status.HTTP_400_INVALID)
    
        # check if in the database (query the model)

        # If its not, call siyao's code
        urls = utils.function_that_gets_urls_from_edgar
        # create company model for that company if we dont have it
        # Create objects and add them to django database using the urls



        data = {
            'company_name': request['name'],
            'company_cik': request['cik'],
            'report_type': request['report_type'],
            'report_date': {
                '<report_year>': '<report_url>',
            },
            'notes': [
                'Additional notes go here!'
            ]
        }

        return Response(data, status=status.HTTP_200_OK)