from rest_framework import serializers

from .models import RawReport, GeneratedReport

class RawReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawReport
        fields = (
            'company',
            'report_date',
            'url'
        )


class GeneratedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedReport
        fields = (
            'name',
            'user',
            'url'
        )