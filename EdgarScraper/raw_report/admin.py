from django.contrib import admin

from .models import RawReport


# Register your models here.
@admin.register(RawReport)
class RawReportAdmin(admin.ModelAdmin):
    list_display = ('company', 'report_date', 'url')
