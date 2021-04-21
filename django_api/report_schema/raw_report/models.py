from django.core.exceptions import ValidationError
from django.apps import AppConfig
from django.contrib import admin
from django.db import models

from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action

from company_schema.models import Company, CompanySerializer


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
    def get_raw_reports(self, request):
        from report_schema.proxy import Proxy
        response, status_code = Proxy().retrieve_raw_reports(request)

        if status_code == 400:
            return Response(
                response, status=status.HTTP_400_INVALID
            )

        return Response(response, status=status.HTTP_200_OK)
