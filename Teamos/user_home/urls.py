from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('redirect_teams', views.redirect_teams, name="redirect_teams"),
    path('redirect_todo', views.redirect_todo, name ="redirect_todo"),
    path('redirect_projects', views.redirect_projects, name="redirect_projects"),
    path("log_out", views.log_out, name="log_out")
]
