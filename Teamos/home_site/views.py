__author__ = "Samuel Simun - xsimun04@fit.vutbr.cz"

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from . import views
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import CreateUserForm
from django.forms import inlineformset_factory
from user_home.models import User_acc

# Create your views here.
def index(request):
    return render(request, 'home_site/Home.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home_site:index")


def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/user_home')

    return render(request, 'home_site/login.html')
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            messages.success(request, "Account was created for " + form.cleaned_data.get('username'))
            new_user = User_acc()
            form.save()
            new_user.name = request.POST.get('username')
            new_user.save()
            return redirect('login')


    return render(request, 'home_site/register.html', {'form' : form})

