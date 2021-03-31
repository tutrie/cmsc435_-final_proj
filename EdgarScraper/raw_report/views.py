from rest_framework import viewsets
from .models import RawReport
from .serializers import RawReportSerializer


# Create your views here.
class RawReportViewSet(viewsets.ModelViewSet):
    queryset = RawReport.objects.all()
    serializer_class = RawReportSerializer
