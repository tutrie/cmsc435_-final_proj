from django.shortcuts import render
from rest_framework import viewsets

from .models import RawReport, GeneratedReport
from .serializers import RawReportSerializer, GeneratedReportSerializer


class RawReportViewSet(viewsets.ModelViewSet):
    queryset = RawReport.objects.all()
    serializer_class = RawReportSerializer

class GeneratedReportViewSet(viewsets.ModelViewSet):
    queryset = GeneratedReport.objects.all()
    serializer_class = GeneratedReportSerializer
