__author__ = "Daniel Zarsky - xzarsk04@fit.vutbr.cz"

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task
from projects.models import Project_list
from django.views import View
from user_home.models import User_acc
from teams.models import Teams_list
import simplejson as json
from django.contrib import messages
#from django.views.generic.list import ListView
#from .forms import NameForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse


class TaskUpdateDone(View):
    def get(self, request, pk, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            task = Task.objects.get(name=pk)
            task.delete()
            return JsonResponse({"message": "success"}, status=200)

        print("fail")
        return JsonResponse({"message": "Wrong route"}, status=404)


@login_required(login_url='login')
def tasklist(request):
    data = Task.objects.filter(done=False)
    print(data)
    return render(request, 'to_do_list/Page-1.html', {'data': data})

def addTask(request):
    if request.POST.get('action') == 'post':
        print("tu")
        name = request.POST.get('task_name')
        description = request.POST.get('task_description')
        project = request.POST.get('project')
        deadline = request.POST.get('deadline')
        priority = request.POST.get('priority')

        if int(priority) > 10 or int(priority) < 0:
            return render(request, 'to_do_list/invalid_prio.html')

        else:
             print("project = ", project)
             task = Task(name=name, description=description, project=project, deadline=deadline, priority=priority)
             task.save()

        return JsonResponse({"instance": name}, status=200)

    else:

        match_2 = Project_list.objects.all()
        match = []
        for item in match_2:
            if request.user.username in item.owner:
                match = match + [item.name]

        return render(request, 'to_do_list/Page-2.html', {'projects': match})

def save_task(request):
    # save task to database but do not send others
    return render(request, 'to_do_list/Page-1.html')

def submit_task(request):
    # save task to database and send others
    return render(request, 'to_do_list/Page-1.html')

def home(request):
    return render(request, 'user_home/home.html')

def view_teams(request):
    return render(request, 'teams/list.html')

def view_projects(request):
    return render(request, 'projects/list.html')




