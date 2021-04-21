from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.apps import AppConfig
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import action

from company_schema.models import Company, CompanySerializer
from report_schema.proxy import strip_request, valid_raw_request
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

    @action(methods=['GET'], detail=False, url_path='get_raw_reports',
            url_name='get_raw_reports')
    def get_raw_reports(self, request) -> Response:

        request = strip_request(request)
        is_valid, msg_dict = valid_raw_request(request)
        if not is_valid:
            return Response(
                json.dumps(msg_dict), status=status.HTTP_400_INVALID
            )

        response = {
            'company_name': request['name'],
            'company_cik': request['cik'],
            'report_type': request['report_type'],
            'reports': {
                '<report_year>': '<report_url>',
            },
            'notes': [
                'Additional notes go here!'
            ]
        }

        raw_reports_in_db = utils.raw_reports_from_db(request)

        if not raw_reports_in_db:
            company_model = Company.objects.create(
                name=request['company'], cik=request['cik']
            )

            response['reports'] = utils.download_and_create_reports(
                request, company_model
            )
        else:
            for report_model in raw_reports_from_db:
                # NEED TO CHANGE DATETIME MODEL TO STRING
                # OR CONVERT DATETIME TO STRING
                year_str = str(report_model.report_date.year)
                response['reports'][year_str] = report_model.excel_url

        return Response(response, status=status.HTTP_200_OK)
