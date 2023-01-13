
#todo remove
from django.forms import ModelForm
from .models import Task

class Create_new_task(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'