from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Report(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey('auth.User')

    def __unicode__(self):
          return 'Report: ' + u"%s" % self.id
