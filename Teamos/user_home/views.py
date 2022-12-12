from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect




@login_required(login_url='login')
def home(request):
    return render(request, 'user_home/user_home.html')

def redirect_teams(request):
    return redirect("/teams")

def redirect_todo(request):
    return redirect("/to_do_list")

def redirect_projects(request):
    return redirect("/projects")

# Create your views here.
