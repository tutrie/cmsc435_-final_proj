from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

from company.models import Company


# Create your models here.
class RawReport(models.Model):
    company = models.ForeignKey(Company, on_delete=CASCADE)
    report_date = models.DateField()
    url = models.URLField()

    def __str__(self):
        return f'Report on {self.report_date} for {self.company}'
    

class GeneratedReport(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    url = models.URLField()

    def __str__(self):
        return f'Report created by {self.user}, named: {self.name}'