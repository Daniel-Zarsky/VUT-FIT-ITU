from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('redirect_teams', views.redirect_teams, name="redirect_teams"),
]
