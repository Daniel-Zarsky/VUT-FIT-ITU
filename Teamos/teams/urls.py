__author__ = "Samuel Simun - xsimun04@fit.vutbr.cz"

from django.contrib import admin
from django.urls import path, include

from . import views
app_name = "teams"

urlpatterns = [
    path('', views.list, name='list'),
    path('create_new', views.create_new, name='create_new'),
    path('invite', views.invite_people, name='invite'),
    path('delete_member/<str:pk>/', views.TaskUpdateDeleteView.as_view(), name="delete" ),
    path("leave_team", views.leave_team, name="leave_team")
]