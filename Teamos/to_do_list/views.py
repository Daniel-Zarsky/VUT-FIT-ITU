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

@login_required(login_url='login')
def tasklist(request):
    data = Task.objects.filter(user=request.user.username, done=False)
    print(data)
    return render(request, 'to_do_list/Page-1.html', {'data': data})

# class List_of_tasks(ListView):
#    model = Task
#    context_object_name = 'tasks'

def addTask(request):
    if request.method == 'POST':
        name = request.POST['task_name']
        description = ['team_name']
        user = request.POST['user_name']
        project = request.POST['project_name']
        deadline = request.POST['date']
        priority = request.POST['priority']
        if not user and not project:
            return render(request, 'to_do_list/none.html')

        if int(priority) > int(10) or int(priority) < int(0):
            return render(request, 'to_do_list/invalid_prio.html')

        if not Projet_list.objects.filter(name=project).exists():
            return render(request, 'to_do_list/invalid_project.html')

        if not User_acc.objects.filter(name=user).exists():
            return render(request, 'to_do_list/invalid_user.html')



        if Projet_list.objects.filter(name=project).first().team != User_acc.objects.filter(name=user).first().member:
              return render(request, 'to_do_list/user_project.html')

        else:
         task = Task(name=name, description=description, user=user, project=project, deadline=deadline, priority=priority)
         task.save()

        return tasklist(request)

    return render(request, 'to_do_list/Page-2.html')

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


