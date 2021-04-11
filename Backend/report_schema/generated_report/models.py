from django.db import models
from django.conf import settings
from django.apps import AppConfig
from django.contrib import admin
from rest_framework import viewsets, serializers


class GeneratedReport(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE,
                                   related_name='created_by')
    # TODO Need to create regular expression to use with match field and set the right path.
    path = models.FilePathField(path=f'./', allow_folders=True)

    def __str__(self):
        return f'Report created by {self.created_by}, named: {self.name}'


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'path')


class ReportSchemaConfig(AppConfig):
    name = 'report_schema'


class GeneratedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedReport
        fields = (
            'name',
            'created_by',
            'path'
        )


class GeneratedReportViewSet(viewsets.ModelViewSet):
    queryset = GeneratedReport.objects.all()
    serializer_class = GeneratedReportSerializer
