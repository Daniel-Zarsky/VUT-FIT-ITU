from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task
from django.views.generic.list import ListView
@login_required(login_url='login')
def tasklist(request):
    return render(request, 'to_do_list/Page-1.html')

class List_of_tasks(ListView):
    model = Task
    context_name = 'tasks'

def addtask(request):
    if request.method == 'POST':
        name = request.POST['task_name']
        description= request.POST['task_description']
        user = request.POST['user_name']
        team = request.POST['team_name']
        deadline = request.POST['date']
        priority = request.POST['priority']

        task = Task(name=name, description=description, user=user, team=team, deadline=deadline, priority=priority)

     # if (Task.priority > "10" or Task.priority < "0"):
     #      return HttpResponse('Error priority outside of the bounds.(0-10)')

        task.save()

        return render(request, 'to_do_list/Page-1.html')
    return render(request, 'to_do_list/Page-2.html')

def delete_task(request):
    return render(request, 'to_do_list/Page-1.html')

def save_task(request):
    # save task to database but do not send others
    return render(request, 'to_do_list/Page-1.html')

def submit_task(request):
    # save task to database and send others
    return render(request, 'to_do_list/Page-1.html')





