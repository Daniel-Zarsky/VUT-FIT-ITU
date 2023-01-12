__author__ = "Samuel Simun - xsimun04@fit.vutbr.cz"

from django.forms import ModelForm
from .models import Teams_list

class Create_form(ModelForm):
    class Meta:
        model = Teams_list
        fields = '__all__'
