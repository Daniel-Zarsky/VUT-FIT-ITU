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
from teams.models import Teams_list


@login_required(login_url='login')
def home(request) :
    return render(request, 'user_home/user_home.html')


# Redirect to teams
def redirect_teams(request) :
    return redirect("/teams")


# Redirect to To Do List
def redirect_todo(request) :
    return redirect("/to_do_list")

# Redirect to projects
def redirect_projects(request) :
    return redirect("/projects")


# Log out
def log_out(request) :
    logout(request)
    return redirect("/home")


# Request for all pending invitations
def get_invitations(request) :
    user = User_acc.objects.get(name=request.user.username)
    return JsonResponse({"project" : user.invited}, status=200)


# Modal window -> answer is accept
def accept_invitation(request) :
    project = request.GET.get('project')
    user = User_acc.objects.get(name=request.user.username)
    team = Teams_list.objects.get(name=project)

    if user.member is None :
        user_member = []
    else :
        user_member = ast.literal_eval(user.member)

    user_invited = ast.literal_eval(user.invited)

    to_delete = user_invited.index(project)
    user_invited.pop(to_delete)

    user_member.append(project)

    user.invited = json.dumps(user_invited)
    user.member = json.dumps(user_member)
    user.save()

    team_member = ast.literal_eval(team.members)
    team_invitations = ast.literal_eval(team.invited)

    to_delete = team_invitations.index(request.user.username)
    team_invitations.pop(to_delete)

    team_member.append(request.user.username)

    team.invited = json.dumps(team_invitations)
    team.members = json.dumps(team_member)
    team.save()
    return JsonResponse({"message" : "success"}, status=200)


# Modal window -> answer is remove
def decline_invitation(request) :
    project = request.GET.get('project')
    user = User_acc.objects.get(name=request.user.username)

    user_invited = ast.literal_eval(user.invited)

    to_delete = user_invited.index(project)
    user_invited.pop(to_delete)

    user.invited = json.dumps(user_invited)
    user.save()
    return JsonResponse({"message" : "success"}, status=200)
