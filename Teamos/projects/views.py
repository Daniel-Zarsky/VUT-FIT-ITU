from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Projet_list
from teams.models import Teams_list
from user_home.models import User_acc
from django.contrib.auth.models import User

def list_projects(request):
    data = Projet_list.objects.filter(owner=request.user.username)
    return render(request, 'projects/list.html', {'data':data})


def create_new(request):
    if request.method == 'POST':
        project_list = Projet_list()
        project_list.owner = request.user.username
        project_list.name = request.POST.get('name')
        project_list.save()
        user_data = User_acc.objects.filter(name=request.user.username)
        jsonDec = json.decoder.JSONDecoder()
        previous_data = jsonDec.decode(user_data.members)
        user_member = previous_data + [project_list.name]
        user_data.members = json.dumps(user_member)
        return redirect('/projects')

    return render(request, 'projects/create_new.html')