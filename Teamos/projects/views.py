__author__ = "Samuel Simun - xsimun04@fit.vutbr.cz"

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Project_list
from teams.models import Teams_list
from user_home.models import User_acc
from to_do_list.models import Task
import simplejson as json
import json as jsons
from django.contrib.auth.models import User
from datetime import datetime as dt
from django.contrib import messages
from django.utils.dateparse import parse_date, parse_datetime
from itertools import zip_longest
from django.http import JsonResponse
import ast


def list_projects(request):
    user = User_acc.objects.get(name=request.user.username)

    if not user.member:
        user_member = []
        return render(request, 'projects/list.html', {'data': user_member})
    else:
        user_member = ast.literal_eval(user.member)
        out = Project_list.objects.filter(team__in=user_member)
    return render(request, 'projects/list.html', {'data': out})


def create_new(request):
    if request.POST.get('action') == 'post':
        if dt.strptime(request.POST.get('deadline'), '%Y-%m-%d') <  dt.now():
            return JsonResponse({"message" : "Deadline must be after this day, sorry you can't reverse your mistakes :("}, status=400)
        else:
            if Project_list.objects.filter(name = request.POST.get('name')).exists():
                print(Project_list.objects.filter(name = request.POST.get('name')))
                return JsonResponse({"message" : "We are sorry, we already have project with same name :("}, status=400)

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
            return JsonResponse({"message" : request.POST.get('name')}, status=200)

    data = Teams_list.objects.all()
    match =[]
    for item in data:
        if request.user.username in item.members :
            match = match + [item.name]

    return render(request, 'projects/create_new.html', {'teams' : match})

def show_timeline(request):
    class time_line():
        def __init__(self, deadline, deadline_name, deadline_text, priority):
            self.deadline = deadline
            self.deadline_name = deadline_name
            self.deadline_text = deadline_text
            self.priority = priority

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
            data.append(time_line(dead, text, name, -2))


    for item in tasks:
        data.append(time_line(str(item.deadline)[:10], item.description, str(item.name), item.priority))

    data.sort(key=lambda x: x.deadline)


    return render(request, 'projects/deadlines.html', {'project_name' : project_name, 'data_proj' : project, 'list_data':data})

def manage_deadlines(request):
    project_name = request.GET.get('project_name')
    data = Project_list.objects.get(name=project_name)
    jsonDec = json.decoder.JSONDecoder()

    if request.POST.get('action') == 'post':
        print(data.start_of_project)
        if dt.strptime(request.POST.get('date'), '%Y-%m-%d') <  dt.strptime(str(data.start_of_project), '%Y-%m-%d'):
            return JsonResponse({"message":"Deadline must be after day you started or are you hiding something? "}, status=400)
        elif dt.strptime(request.POST.get('date'), '%Y-%m-%d') > dt.strptime(str(data.final_deadline), '%Y-%m-%d'):
            return JsonResponse({"message":"Don't do that, why would you want to set deadline after projects deadline? Im confused, really ... \nAnd little disappointed"}, status=400)
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
        return JsonResponse({"message" : "success", "deadline_name" : request.POST.get('deadline'), "deadline_text" : request.POST.get('message'), "deadline_date" : request.POST.get('date')}, status = 200)


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

    data = Project_list.objects.get(name=project)
    deadline_date_list = ast.literal_eval(data.deadlines)
    deadline_text_list = ast.literal_eval(data.deadlines_text)
    deadline_name_list = ast.literal_eval(data.deadlines_name)

    remove = deadline_name_list.index(to_delete)
    deadline_text_list.pop(remove)
    deadline_date_list.pop(remove)
    deadline_name_list.pop(remove)

    data.deadlines = json.dumps(deadline_date_list)
    data.deadlines_name = json.dumps(deadline_name_list)
    data.deadlines_text = json.dumps(deadline_text_list)

    data.save()
    return JsonResponse({"message" : "success"}, status=200)