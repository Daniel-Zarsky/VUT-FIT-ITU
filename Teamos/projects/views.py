from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Project_list
from teams.models import Teams_list
from user_home.models import User_acc
from to_do_list.models import Task
import simplejson as json
from django.contrib.auth.models import User
from datetime import datetime as dt
from django.contrib import messages
from django.utils.dateparse import parse_date, parse_datetime
from itertools import zip_longest


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
    class time_line():
        def __init__(self, deadline, deadline_name, deadline_text):
            self.deadline = deadline
            self.deadline_name = deadline_name
            self.deadline_text = deadline_text

    jsonDec = json.decoder.JSONDecoder()
    project_name = request.GET.get('project_name')
    project = Project_list.objects.get(name=project_name)
    tasks = Task.objects.filter(project=project_name)

    data = []

    if project.deadlines is not None:
        project_deadline = jsonDec.decode(project.deadlines)
        project_deadline_text = jsonDec.decode(project.deadlines_text)
        project_deadline_name = jsonDec.decode(project.deadlines_name)

        for dead,text,name in list(zip_longest(project_deadline, project_deadline_text, project_deadline_name)):
            data.append(time_line(dead, text, name))


    for item in tasks:
        data.append(time_line(item.deadline, item.description, item.name))

    data.sort(key=lambda x: x.deadline)


    return render(request, 'projects/deadlines.html', {'project_name' : project_name, 'data_proj' : project, 'list_data':data})

def manage_deadlines(request):
    project_name = request.GET.get('project_name')
    data = Project_list.objects.get(name=project_name)
    jsonDec = json.decoder.JSONDecoder()

    if request.method == 'POST':
        if dt.strptime(request.POST.get('date'), '%Y-%m-%d') <  dt.now():
            messages.error(request, "Deadline must be after this day, sorry you can't reverse your mistakes :(")
        else:
            if data.deadlines is None:
                data.deadlines = json.dumps([request.POST.get('date')])
                data.deadlines_text = json.dumps([request.POST.get('message')])
                data.deadlines_name = json.dumps([request.POST.get('deadline')])
            else:
                deadline = jsonDec.decode(data.deadlines)
                data.deadlines = json.dumps(deadline + [request.POST.get('date')])

                deadline_text = jsonDec.decode(data.deadlines_text)
                data.deadlines_text = json.dumps(deadline_text + [request.POST.get('message')])

                deadline_name = jsonDec.decode(data.deadlines_name)
                data.deadlines_name = json.dumps(deadline_name + [request.POST.get('deadline')])

            data.save()


    if data.deadlines is None:
        deadlines_data = None
    else:
        deadlines = jsonDec.decode(data.deadlines)
        deadlines_text = jsonDec.decode(data.deadlines_text)
        deadlines_names = jsonDec.decode(data.deadlines_name)
        deadlines_data = list(zip_longest(deadlines, deadlines_text, deadlines_names))



    return render(request, 'projects/manage.html', {'data' : data, 'deadlines_data' : deadlines_data})

def delete_project(request):
    to_delete = request.GET.get('project_name')
    Project_list.objects.get(name=to_delete).delete()
    return redirect('/projects')

def delete_deadline(request):
    to_delete = request.GET.get('deadline_name')
    project = request.GET.get('project_name')
    jsonDec = json.decoder.JSONDecoder()
    return redirect('/projects/manage_deadlines?project_name=' + project)

    data = Project_list.objects.get(name=project)

    deadline = jsonDec.decode(data.deadlines)
    deadline_name = jsonDec.decode(data.deadlines_name)
    deadline_text = jsonDec.decode(data.deadlines_text)


    index = deadline_name.index(to_delete)



    data.deadlines = json.dumps(deadline.pop(index))
    data.deadlines_text = json.dumps(deadline_text.pop(index))
    data.deadlines_name = json.dumps(deadline_name.pop(index))
    data.save()

    return redirect('/projects/manage_deadlines?project_name='+ project)