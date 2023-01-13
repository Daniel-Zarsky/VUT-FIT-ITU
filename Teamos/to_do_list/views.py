__author__ = "Daniel Zarsky - xzarsk04@fit.vutbr.cz"

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task
from projects.models import Project_list
from user_home.models import User_acc
from teams.models import Teams_list
import simplejson as json
from django.contrib import messages
#from django.views.generic.list import ListView
#from .forms import NameForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse

@login_required(login_url='login')
def tasklist(request):
    data = Task.objects.filter(done=False)
    print(data)
    return render(request, 'to_do_list/Page-1.html', {'data': data})

# class List_of_tasks(ListView):
#    model = Task
#    context_object_name = 'tasks'

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

# def delete_task(request):
#     return render(request, 'to_do_list/Page-1.html')

def save_task(request):
    # save task to database but do not send others
    return render(request, 'to_do_list/Page-1.html')

def submit_task(request):
    # save task to database and send others
    return render(request, 'to_do_list/Page-1.html')


# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#
#     return render(request, 'name.html', {'form': form})


def home(request):
    return render(request, 'user_home/home.html')


def view_teams(request):
    return render(request, 'teams/list.html')


def view_projects(request):
    return render(request, 'projects/list.html')

def process_completed(request):
         task_name = request.GET.get('task_name')
         data = Task.objects.filter(name=task_name)
         data.update(done=True, priority=0)

         return tasklist(request)


