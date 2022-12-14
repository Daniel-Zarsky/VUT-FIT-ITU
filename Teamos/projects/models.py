from django.db import models
import datetime
from django.utils import timezone

class Projet_list(models.Model):
    owner = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    final_deadline = models.DateField(default=timezone.now, null=True)
    deadlines = models.TextField(null=True)
    team = models.CharField(max_length=100, null=True)

