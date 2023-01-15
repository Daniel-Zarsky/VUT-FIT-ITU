__author__ = "Samuel Simun - xsimun04@fit.vutbr.cz"

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
import json as jsons
import simplejson as json
import ast
from django.http import JsonResponse


from .models import User_acc




@login_required(login_url='login')
def home(request):
    return render(request, 'user_home/user_home.html')

def redirect_teams(request):
    return redirect("/teams")

def redirect_todo(request):
    return redirect("/to_do_list")

def redirect_projects(request):
    return redirect("/projects")

def log_out(request):
    logout(request)
    return redirect("/home")

# Create your views here.
def tbd(request):
    return render(request, 'user_home/tbd.html')

def get_invitations(request):
    user = User_acc.objects.get(name=request.user.username)
    return JsonResponse({"project" : user.invited}, status=200)

def accept_invitation(request):
    project = request.GET.get('project')
    user = User_acc.objects.get(name=request.user.username)

    if user.member is None:
        user_member = []
    else:
        user_member = ast.literal_eval(user.invited)

    user_invited = ast.literal_eval(user.invited)

    to_delete = user_invited.index(project)
    user_invited.pop(to_delete)

    user_member.append(project)

    user.invited = json.dumps(user_invited)
    user.member = json.dumps(user_member)
    user.save()
    return JsonResponse({"message" : "success"}, status=200)

def decline_invitation(request):
    project = request.GET.get('project')
    user = User_acc.objects.get(name=request.user.username)

    user_invited = ast.literal_eval(user.invited)

    to_delete = user_invited.index(project)
    user_invited.pop(to_delete)

    user.invited = json.dumps(user_invited)
    user.save()
    return JsonResponse({"message": "success"}, status=200)
