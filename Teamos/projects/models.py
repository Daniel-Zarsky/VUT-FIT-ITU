from django.db import models
import datetime
from django.utils import timezone

class Project_list(models.Model):
    owner = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    start_of_project = models.DateField(default=timezone.now, null=True)
    final_deadline = models.DateField(default=timezone.now, null=True)
    deadlines_name = models.TextField(null=True)
    deadlines = models.TextField(null=True)
    deadlines_text = models.TextField(null=True)
    team = models.CharField(max_length=100, null=True)

