__author__ = "Daniel Zarsky - xzarsk04@fit.vutbr.cz"

from django.contrib import admin
from .models import Task
#from .views import List_of_tasks

admin.site.register(Task)
#admin.site.register(List_of_tasks)