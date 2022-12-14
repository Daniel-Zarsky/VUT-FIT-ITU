from django.db import models

class User_acc(models.Model):
    name = models.CharField(max_length=100)
    member = models.TextField(null=True)
    invited = models.TextField(null=True)
    img = models.ImageField(upload_to="media/")
