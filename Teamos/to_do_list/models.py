from django.db import models
from django.contrib.auth.models import User

class
# Create your models here.
class Task(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    #team=  models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    done = models.BooleanField(default=False)
    deadline = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField()

    def _str_(self):
        return self.title

    class Meta:
        ordering =['complete']