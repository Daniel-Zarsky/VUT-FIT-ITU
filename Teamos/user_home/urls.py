__author__ = "Samuel Simun - xsimun04@fit.vutbr.cz"

from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('redirect_teams', views.redirect_teams, name="redirect_teams"),
    path('redirect_todo', views.redirect_todo, name ="redirect_todo"),
    path('redirect_projects', views.redirect_projects, name="redirect_projects"),
    path('tbd', views.tbd, name="tbd"),
    path("log_out", views.log_out, name="log_out"),
    path("get_invitations", views.get_invitations, name="get_invitations"),
    path("accept_invitation", views.accept_invitation, name="accept_invitation"),
    path("decline_invitation", views.decline_invitation, name="decline_invitation")
]
