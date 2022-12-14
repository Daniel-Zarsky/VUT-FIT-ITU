from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Project_list
from teams.models import Teams_list
from user_home.models import User_acc
import simplejson as json
from django.contrib.auth.models import User
from datetime import datetime as dt
from django.contrib import messages
from django.utils.dateparse import parse_date, parse_datetime


def list_projects(request):
    data = Project_list.objects.filter(owner=request.user.username)
    return render(request, 'projects/list.html', {'data':data})


def create_new(request):
    if request.method == 'POST':
        if dt.strptime(request.POST.get('deadline'), '%Y-%m-%d') <  dt.now():
            messages.error(request, "Deadline must be after this day, sorry you can't reverse your mistakes :(")
        else:
            jsonDec = json.decoder.JSONDecoder()
            project_list = Project_list()
            project_list.owner = request.user.username
            project_list.name = request.POST.get('name')
            project_list.team = request.POST.get('team')
            project_list.start_of_project = dt.now().strftime("%Y-%m-%d")
            project_list.final_deadline = dt.strptime(request.POST.get('deadline'), "%Y-%m-%d").date()
            project_list.save()
            team_list = Teams_list.objects.get(name=request.POST.get('team'))

            if team_list.projects is None:
                team_list.projects = json.dumps([request.POST.get('name')])
            else:
                old = jsonDec.decode(team_list.projects)
                team_list.projects = json.dumps(old + [request.POST.get('name')])
            team_list.save()
            return redirect('/projects')

    data = Teams_list.objects.all()
    match =[]
    for item in data:
        if request.user.username in item.members :
            match = match + [item.name]

    return render(request, 'projects/create_new.html', {'teams' : match})

def show_timeline(request):
    project_name = request.GET.get('project_name')
    project = Project_list.objects.get(name=project_name)

    return render(request, 'projects/deadlines.html', {'project_name' : project_name})

def manage_deadlines(request):
    return 