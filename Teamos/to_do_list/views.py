from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def tasklist(request):
    return render(request, 'to_do_list/Page-1.html')

def addTask(request):
    return render(request, 'to_do_list/Page-2.html')

def delete_task(request):
    return render(request, 'to_do_list/Page-1.html')

def save_task(request):
    # save task to database but do not send others
    return render(request, 'to_do_list/Page-1.html')

def submit_task(request):
    # save task to database and send others
    return render(request, 'to_do_list/Page-1.html')
