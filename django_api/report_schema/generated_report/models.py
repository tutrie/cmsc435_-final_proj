from django.db import models
from django.conf import settings
from django.apps import AppConfig
from django.contrib import admin
from rest_framework import viewsets, serializers, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from report_schema.generated_report.permissions import IsOwner


class GeneratedReport(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE,
                                   related_name='created_by')
    # TODO Need to create regular expression to use with match field and set the right path.
    path = models.FilePathField(path='./', allow_folders=True)

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
            'id',
            'name',
            'created_by',
            'path'
        )


class GeneratedReportViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows the user to create
    and retrieve generated reports for the authenticated user.
    """
    queryset = GeneratedReport.objects.all()
    serializer_class = GeneratedReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]  # API user must authenticate with a registered user
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    # Overwrite the create method that is called for a POST request
    def create(self, request, *args, **kwargs):
        user = request.user
        request.data['created_by'] = user.id

        # Create a serialized report from the request data and check if its valid
        report_serializer = GeneratedReportSerializer(data=request.data)
        if report_serializer.is_valid():
            report_serializer.save()
            return Response(report_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(report_serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Overwrite the list method that is called for a GET request
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            reports_for_user = GeneratedReport.objects.all()  # Superusers can see all reports
        else:
            reports_for_user = GeneratedReport.objects.filter(created_by=user)

        filtered_queryset = self.filter_queryset(reports_for_user)
        
        # Take the filtered queryset and serialize it so we can send it in a response.
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
    
    # Overwrite the update method for what a PUT request is made
    def update(self, request, *args, **kwargs):
        user = request.user
        request.data['created_by'] = user.id

        report_to_update = self.get_object()
        
        report_serializer = GeneratedReportSerializer(report_to_update, data=request.data)
        if report_serializer.is_valid():
            report_serializer.save()
            return Response(report_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(report_serializer._errors, status=status.HTTP_400_BAD_REQUEST)
