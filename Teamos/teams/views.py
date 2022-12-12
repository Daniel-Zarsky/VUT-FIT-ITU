from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def list(request):
    return render(request, 'teams/list.html')

# Create your views here.
