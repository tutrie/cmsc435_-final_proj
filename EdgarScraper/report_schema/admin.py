from django.contrib import admin

from .models import RawReport, GeneratedReport
# Register your models here.
@admin.register(RawReport)
class RawReportAdmin(admin.ModelAdmin):
    list_display = ('company', 'report_date', 'report_type', 'excel_url')

@admin.register(GeneratedReport)
class RawReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'path')