__author__ = "Daniel Zarsky - xzarsk04@fit.vutbr.cz"

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task
from projects.models import Project_list
from django.views import View
from django.http import JsonResponse
import json
from datetime import datetime as dt
from django.shortcuts import redirect

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

        # check = Task.objects.all
        # for task in check:
        #     if task.name == request.POST.get('task_name'):
        #         return JsonResponse({"message": "Task already exists!!!"""}, status=500)
        name = request.POST.get('task_name')
        description = request.POST.get('task_description')
        project = request.POST.get('project')
        deadline = dt.strptime(request.POST.get('deadline'), "%Y-%m-%d").date()
        priority = request.POST.get('priority')
        data = Project_list.objects.get(name=project)
        if int(priority) > 10 or int(priority) < 0:
            return render(request, 'to_do_list/invalid_prio.html')

        elif dt.strptime(request.POST.get('deadline'), '%Y-%m-%d') > dt.strptime(str(data.final_deadline), '%Y-%m-%d'):
            return render(request, 'to_do_list/invalid_prio.html')

        elif dt.strptime(request.POST.get('deadline'), '%Y-%m-%d') < dt.strptime(str(data.start_of_project), '%Y-%m-%d'):
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
    return redirect("/to_do_list")


def home(request):
    return redirect('/user_home')


def view_teams(request):
    return redirect("/teams")


def view_projects(request):
    return redirect("/projects")
