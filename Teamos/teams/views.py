from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from urllib.parse import urlencode
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse

from .models import Teams_list
from user_home.models import User_acc
from django.shortcuts import redirect
import simplejson as json
from .form import Create_form




@login_required(login_url='login')
def list(request):
    #data = Teams_list.objects.all()
    data = Teams_list.objects.filter(owner=request.user.username)
    return render(request, 'teams/list.html', {'data': data})


def create_new(request):
    if request.method == 'POST':
        teams_list = Teams_list()
        teams_list.name = request.POST.get('name')
        teams_list.photo = request.FILES.get('image')
        teams_list.owner = request.user.username
        teams_list.members = json.dumps([request.user.username])
        teams_list.save()
        return redirect('{}?{}'.format(reverse('invite'), urlencode({'team':teams_list.name})))
    else:
        return render(request, 'teams/create_new.html')


def invite_people(request):
    team_name = request.GET.get('team')
    jsonDec = json.decoder.JSONDecoder()
    if request.method == 'POST':
        new = request.POST.get('name')
        if not User_acc.objects.filter(name = new).exists():
            messages.error(request, "User not found !")

        else:
            team_data = Teams_list.objects.get(name=team_name)
            user_data = User_acc.objects.get(name=new)

            if user_data.invited is None:
                user_data.invited = json.dumps([team_name])
            else:
                user_invite = jsonDec.decode(user_data.invited)
                user_data.invited = json.dumps(user_invite +[team_name])

            user_data.save()

            if team_data.invited is None:
                team_data.invited = json.dumps([new])

            else:
                invited = jsonDec.decode(team_data.invited)
                team_data.invited = json.dumps(invited + [new])
            team_data.save()



    data = Teams_list.objects.get(name=team_name)
    members = jsonDec.decode(data.members)
    if data.invited is None:
        members_inv = None
    else :
        members_inv = jsonDec.decode(data.invited)

    return render(request, 'teams/invite.html', {'team_name': team_name, 'data' : members, 'data_inv': members_inv})

def show_dash(request):
    team_name = request.GET.get('team_name')
    print(team_name)
    return render(request, 'teams/invite.html')
    



# Create your views here.
