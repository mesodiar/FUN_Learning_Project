from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_slug


from django.db import models
from report import models as report_models

class Items(models.Model):
        name = models.TextField()
        stage = models.IntegerField()
        report_id = models.ForeignKey(report_models.Report)
        status = models.BooleanField(default=False)
