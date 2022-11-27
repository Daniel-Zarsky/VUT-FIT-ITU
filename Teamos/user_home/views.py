from django.shortcuts import render


def home(request):
    return render(request, 'user_home/user_home.html')

# Create your views here.
