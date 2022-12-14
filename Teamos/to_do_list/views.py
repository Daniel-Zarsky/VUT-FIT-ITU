from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task
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
        team = request.POST['team_name']
        deadline = request.POST['date']
        priority = request.POST['priority']

        task = Task(name=name, description=description, user=user, team=team, deadline=deadline, priority=priority)
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


def view_projects(request): #todo
    return render(request, 'home_site/About.html')

def process_completed(request):
         name = request.GET.get('task_name')
         data = Task.objects.filter(name=name)
         print("input")
         print(data)
         data.update(done=True, priority=0)
         print("updated")
         print(data)
         return tasklist(request)


