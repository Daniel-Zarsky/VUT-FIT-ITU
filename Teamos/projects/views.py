from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Projet_list
from teams.models import Teams_list
from django.contrib.auth.models import User

def list_projects(request):
    return render(request, 'projects/list.html')


def create_new(request):
    if request.method == 'POST':
        project_list = Projet_list()
        project_list.owner = request.user.username
        project_list.name = request.POST.get('name')
        project_list.save()
        return redirect('/projects')
    return render(request, 'projects/create_new.html')