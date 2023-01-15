__author__ = "Samuel Simun - xsimun04@fit.vutbr.cz"

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from urllib.parse import urlencode
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, HttpResponse

from .models import Teams_list
from user_home.models import User_acc
from django.shortcuts import redirect
import simplejson as json
from .form import Create_form
import ast


def delete_member(request) :
    team_name = request.GET.get('team')
    user_name = request.GET.get('user')
    print(team_name)
    print(user_name)
    team = Teams_list.objects.get(name=team_name)
    user = User_acc.objects.get(name=user_name)

    team_invited = ast.literal_eval(team.invited)
    user_invited = ast.literal_eval(user.invited)

    to_delete = team_invited.index(user_name)
    team_invited.pop(to_delete)

    to_delete = user_invited.index(team_name)
    user_invited.pop(to_delete)

    team.invited = json.dumps(team_invited)
    user.invited = json.dumps(user_invited)

    user.save()
    team.save()
    return JsonResponse({"message" : "success"})


class TaskUpdateAddView(View):
    def get(self, request, pk, *args, **kwargs):
        pass


@login_required(login_url='login')
def list(request):
    data = User_acc.objects.get(name=request.user.username)
    out = []
    print(data.member)
    if data.member is None:
        pass
    else:
        teams = ast.literal_eval(data.member)
        for team in teams:
            out.append(Teams_list.objects.get(name=team))

    return render(request, 'teams/list.html', {'data': out})

def leave_team(request):
    team_name = request.GET.get('team')
    user = User_acc.objects.get(name=request.user.username)
    team = Teams_list.objects.get(name=team_name)

    user_member = ast.literal_eval(user.member)
    team_members = ast.literal_eval(team.members)

    to_delete = user_member.index(team_name)
    user_member.pop(to_delete)

    to_delete = team_members.index(request.user.username)
    team_members.pop(to_delete)

    user.member = json.dumps(user_member)
    team.members = json.dumps(team_members)

    print(user.member)
    user.save()
    team.save()
    return JsonResponse({"message" : "success"}, status=200)

def create_new(request):
    if request.POST.get('action') == 'post':
        teams_list = Teams_list()
        teams_list.name = request.POST.get('name')
        teams_list.photo = request.FILES.get('image')
        teams_list.owner = request.user.username
        teams_list.members = json.dumps([request.user.username])
        teams_list.save()
        name = request.POST.get('name')

        user = User_acc.objects.get(name=request.user.username)
        if user.member is None:
            user_member = []
        else:
            user_member = ast.literal_eval(user.member)

        user_member.append(name)
        user.member = json.dumps(user_member)
        user.save()
        return JsonResponse({"message": name}, status=200)
    else:
        return render(request, 'teams/create_new.html')


def invite_people(request):
    team_name = request.GET.get('team')
    jsonDec = json.decoder.JSONDecoder()
    if request.POST.get('action') == 'post':
        new = request.POST.get('name')
        if not User_acc.objects.filter(name=new).exists():
            return JsonResponse({"error": "User doesn't exists"}, status=400)

        else:
            team_data = Teams_list.objects.get(name=team_name)
            user_data = User_acc.objects.get(name=new)

            team_members = ast.literal_eval(team_data.members)
            if new in team_members:
                return JsonResponse({"error" : "User is already member!"}, status=400)

            if team_data.invited is None:
                team_invited =[]
            else:
                team_invited = ast.literal_eval(team_data.invited)
            if new in team_invited:
                return JsonResponse({"error" : "User is already invited!"}, status=400)

            if user_data.invited is None:
                user_data.invited = json.dumps([team_name])
            else:
                user_invite = jsonDec.decode(user_data.invited)
                user_data.invited = json.dumps(user_invite + [team_name])

            user_data.save()

            if team_data.invited is None:
                team_data.invited = json.dumps([new])

            else:
                invited = jsonDec.decode(team_data.invited)
                team_data.invited = json.dumps(invited + [new])
            team_data.save()
            return JsonResponse({"instance": new}, status=200)

    data = Teams_list.objects.get(name=team_name)
    members = jsonDec.decode(data.members)
    if data.invited is None:
        members_inv = None
    else:
        members_inv = jsonDec.decode(data.invited)

    return render(request, 'teams/invite.html', {'team_name': team_name, 'data': members, 'data_inv': members_inv})
