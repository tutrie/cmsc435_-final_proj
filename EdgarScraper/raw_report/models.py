from django.db import models
from django.db.models.deletion import CASCADE
from company.models import Company

# Create your models here.
class RawReport(models.Model):
    company = models.ForeignKey(Company, on_delete=CASCADE)
    report_date = models.DateField()
    url = models.URLField()

    def __str__(self):
        return f'Report on {self.report_date} for {self.company}'
