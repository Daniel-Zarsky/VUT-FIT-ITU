__author__ = "Daniel Zarsky - xzarsk04@fit.vutbr.cz"

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task
from projects.models import Project_list
from django.views import View
from django.http import JsonResponse
import json


# main view of all the tasks with asynchronous communication

class TaskUpdateDone(View):

    def get(self, request, pk, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            task = Task.objects.get(name=pk)
            task.done = True
            task.save()
            return JsonResponse({"message": "success"}, status=200)

        return JsonResponse({"message": "Wrong route"}, status=404)


# main view of all the tasks with asynchronous communication
class TaskUpdateDelete(View):
    def get(self, request, pk, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            task = Task.objects.get(name=pk)
            task.delete()
            return JsonResponse({"message": "success"}, status=200)

        return JsonResponse({"message": "Wrong route"}, status=404)


class TaskShowDone(View):
    def get(self, request):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

            all_tasks = Task.objects.all() #all tasks
            print(all_tasks)
            name = [] #array for done tasks
            for t in all_tasks:
               if t.done:                  #if task is done
                    name = name + [t.name]  #add it to the array

            name = json.dumps(name)
            return JsonResponse({'name' : name}, status=200) #send the array

        return JsonResponse({"message": "Wrong route"}, status=404)


# function for viewing the list of tasks synchronously
@login_required(login_url='login')
def tasklist(request):
    data = Task.objects.filter(done=False)
    print(data)
    return render(request, 'to_do_list/task_list.html', {'data': data})


# function to view a formular for creating tasks
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

        return render(request, 'to_do_list/new_task.html', {'projects': match})


# functions for rendering other pages
def submit_task(request):
    # save task to database and send others
    return render(request, 'to_do_list/task_list.html')


def home(request):
    return render(request, 'user_home/user_home.html')


def view_teams(request):
    return render(request, 'teams/list.html')


def view_projects(request):
    return render(request, 'projects/list.html')
