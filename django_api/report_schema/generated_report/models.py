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
        request.data._mutable = True
        request.data['created_by'] = user.id
        request.data._mutable = False

        report_serializer = GeneratedReportSerializer(data=request.data)
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
    def analysis(self, request, report_id=None):

        print(report_id)
        print(request.data)

        response = {}
        return Response(response, status=status.HTTP_200_OK)


    @action(methods=['POST'], detail=False, url_path='get-form-data', url_name='get-form-data')
    def get_form_data(self, request):
        from report_schema.generated_report.utils import get_sheets_and_rows
    
        valid_request, msg = self.validate_request_get_form(request)
        if not valid_request:
            return Response({'msg': f'Invalid request: {msg}'}, status.HTTP_400_BAD_REQUEST)

        data = request.data
        form_data = get_sheets_and_rows(
            request.user,
            data['report_name'],
            data['company'],
            data['cik'],
            data['years']
        )
        
        if form_data:
            return Response({'form_data': json.dumps(form_data)}, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_INVALID)

    @action(methods=['POST'], detail=False, url_path='create-report', url_name='create-report')
    def create_report(self, request):
        from report_schema.generated_report.utils import create_generated_report

        valid_request, msg = self.validate_request_create_report(request)
        
        if not valid_request:
            return Response({'msg': f'Invalid request: {msg}'}, status.HTTP_400_BAD_REQUEST)
        
        # Expecting
        data = request.data
        gen_report_id = create_generated_report(
            request.user,
            data['report_name'], # String
            data['form_data'], # int list
            data['type'] # string
        )

        return Response({'id': gen_report_id}, status.HTTP_200_OK)

    def validate_request_create_report(self, request):
        data = request.data
        keys_in_request = 'report_name' in data \
                        and 'form_data' in data \
                        and 'type' in data
        
        if not keys_in_request:
            return False, 'Correct keys not in request body.'

        correct_types = isinstance(data['report_name'], str) and \
                        isinstance(data['form_data'], str) and \
                        isinstance(data['type'], str)

        if not correct_types:
            return False, 'Key values not the right type in the request body.'

        acceptable_types = {'json', 'xlsx'}
        if data['type'] not in acceptable_types:
            return False, 'File type is invalid.'
        
        report_exists = GeneratedReport.objects.filter(created_by=request.user, name=data['report_name'])
        if not report_exists:
            return False, 'That report does not exist yet.'

        return (True, 'Valid.')

    def validate_request_get_form(self, request):
        data = request.data
        keys_in_request = 'report_name' in data \
                        and 'company' in data \
                        and 'cik' in data \
                        and 'years' in data
        
        if not keys_in_request:
            return False, 'Correct keys not in request body.'

        correct_types = isinstance(data['report_name'], str) and \
                        isinstance(data['company'], str) and \
                        isinstance(data['cik'], str) and \
                        isinstance(data['years'], str)
        
        if not correct_types:
            return False, 'Key values not the right type in the request body.'

        acceptable_years = {'2016', '2017', '2018', '2019', '2020', '2021'}
        for year in data['years'].split(','):
            if not (year in acceptable_years):
                return False, 'Year selected is not a valid year.'

        name_exists = GeneratedReport.objects.filter(created_by=request.user, name=data['report_name'])
        if name_exists:
            return False, 'That user has already created a report with that name.'

        return True, 'Valid.'

