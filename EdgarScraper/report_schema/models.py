from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.core.exceptions import ValidationError

from company_schema.models import Company


# Create your models here.
class RawReport(models.Model):
    company = models.ForeignKey(Company, on_delete=CASCADE)
    report_date = models.DateField()
    report_type = models.CharField(max_length=4)
    excel_url = models.URLField()

    # Overwrite save method
    def save(self, *args, **kwargs):
        if self.report_type != '10-Q' and self.report_type != '10-K':
            raise ValidationError('Report Type not Valid.')

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Report {self.report_type} from {self.report_date} for {self.company}'
    

class GeneratedReport(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='created_by')
    path = models.FilePathField(path=f'./', allow_folders=True) # TODO Need to create regular expression to use with match field and set the right path.

    def __str__(self):
        return f'Report created by {self.created_by}, named: {self.name}'