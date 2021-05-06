import json

from django.db import models
from django.conf import settings
from django.apps import AppConfig
from django.contrib import admin
from rest_framework import viewsets, serializers, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
import json

from report_schema.generated_report.permissions import IsOwner

class GeneratedReport(models.Model):
    """Defines the GeneratedReport model in our database

    Inherits from the predefined model class.
    """
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE,
                                   related_name='created_by')
    json_schema = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Report created by {self.created_by}, named: {self.name}'


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    """Defines what parameters from the generated report model should be displayed on the admin panel.

    Inherits from the predefined model admin class.
    """
    list_display = ('name', 'created_by')


class ReportSchemaConfig(AppConfig):
    """Configures the name of this application

    Inherits from the predefined AppConfig class.
    """
    name = 'report_schema'


class GeneratedReportSerializer(serializers.ModelSerializer):
    """Serializes the GeneratedReport model in the database, converting a row to a json object and vice versa.

    Inherits from the predefined model serializer.
    """
    class Meta:
        model = GeneratedReport
        fields = (
            'id',
            'name',
            'created_by',
            'json_schema'
        )


class GeneratedReportViewSet(viewsets.ModelViewSet):
    """Defines the API Endpoint for the GeneratedReport model in the database.
    All API requests require basic authentication with an existing user in the database.

    Inherits from the predefined model viewset.
    """
    queryset = GeneratedReport.objects.all()
    serializer_class = GeneratedReportSerializer
    # API user must authenticate with a registered user
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    # Overwrite the create method that is called for a POST request
    def create(self, request: Request, *args, **kwargs) -> Response:
        """Overwrites the default create method for the GeneratedReport viewset.
        Creates a generated report object in the database.
        This function is called when a user makes a POST request to the /api/generated_reports/ endpoint.

        Args:
            request (Request): Accepts a request object with a json body
            that has the fields defined on the object model.


        Returns:
            Response: Returns a response object with a status code and a json body representing the created object.
        """
        user = request.user
        data = request.data.copy()
        data['created_by'] = user.id

        report_serializer = GeneratedReportSerializer(data=data)
        if report_serializer.is_valid():
            report_serializer.save()
            return Response(report_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(report_serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    # Overwrite the list method that is called for a GET request
    def list(self, request: Request, *args, **kwargs) -> Response:
        """Overwrites the default list method for the GeneratedReport viewset.
        Filters and sends all generated reports for the authenticated user.
        This function is called when a user makes a GET request to the /api/generated_reports/ endpoint.

        Args:
            request (Request): Accepts a request object with no body.


        Returns:
            Response: Returns a response object with a status code and a json body with all of
            the authenticated user's generated reports.
        """
        user = request.user
        can_see_all_reports = user.is_superuser
        if can_see_all_reports:
            reports_for_user = GeneratedReport.objects.all()
        else:
            reports_for_user = GeneratedReport.objects.filter(created_by=user)

        filtered_queryset = self.filter_queryset(reports_for_user)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)

    # Overwrite the update method for what a PUT request is made
    def update(self, request, *args, **kwargs):
        """Overwrites the default update method for the GeneratedReport viewset.
        Updates the specified generated report in the database.
        This function is called when a user makes a PUT request to the /api/generated_reports/ endpoint.
        The user should include the generated report's pk in the kwargs of the request.

        Args:
            request (Request): Accepts a request object with a json body that
            has the fields defined on the object model.


        Returns:
            Response: Returns a response object with a status code and a json body representing the updated object.

        """
        user = request.user
        request.data['created_by'] = user.id

        report_to_update = self.get_object()

        report_serializer = GeneratedReportSerializer(
            report_to_update, data=request.data)
        if report_serializer.is_valid():
            report_serializer.save()
            return Response(report_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(report_serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='analysis',
            url_name='report_analysis')
    def analysis(self, request):

        # proxy
        if not request.user or not request.data or 'report_id' not in \
                                                       request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # proxy
        try:
            report = GeneratedReport.objects.get(id=request.data['report_id'])
        except GeneratedReport.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        report_data = json.loads(report.json_schema)

        # using jason's code
        # active_report = ActiveReport({})
        # active_report.generated_report = report_data
        # active_report.min_max_avg()

        # using util version
        analysis = min_max_avg(report_data)

        # ToDo save analysis as a new generated report

        return Response(analysis, status=status.HTTP_200_OK)


    @action(methods=['POST'], detail=False, url_path='get-form-data', url_name='get-form-data')
    def get_form_data(self, request):
        from report_schema.generated_report.utils import get_sheets_and_rows, validate_get_form_data_request
    
        valid_request, msg = validate_get_form_data_request(request)
        if not valid_request:
            return Response({'msg': f'Invalid request: {msg}'}, status.HTTP_400_BAD_REQUEST)

        data = request.data
        try:
            form_data = get_sheets_and_rows(
                request.user,
                data['report_name'],
                data['company'],
                data['cik'],
                data['years']
            )
        except Exception:
            return Response({'msg': 'Error getting form data.'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        if form_data:
            return Response({'form_data': json.dumps(form_data)}, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['POST'], detail=False, url_path='create-report', url_name='create-report')
    def create_report(self, request):
        from report_schema.generated_report.utils import create_generated_report, validate_create_report_request

        valid_request, msg = validate_create_report_request(request)
        if not valid_request:
            return Response({'msg': f'Invalid request: {msg}'}, status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        try:
            gen_report_id = create_generated_report(
                request.user,
                data['report_name'],
                data['form_data'],
                data['type']
            )
        except Exception:
            return Response({'msg': 'Error filtering report.'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        if gen_report_id:
            return Response({'id': gen_report_id}, status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
