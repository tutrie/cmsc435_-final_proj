from rest_framework import serializers
from .models import RawReport


class RawReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawReport
        fields = (
            'company',
            'report_date',
            'url'
        )
