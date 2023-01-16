__author__ = "Samuel Simun - xsimun04@fit.vutbr.cz"

from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.list_projects, name='list_projects'),
    path('create_new', views.create_new, name='create_new'),
    path('show_timeline', views.show_timeline, name='show_timeline'),
    path('manage_deadlines', views.manage_deadlines, name='manage_deadlines'),
    path('delete_project', views.delete_project, name='delete_project'),
    path('delete_deadline', views.delete_deadline, name='delete_deadline')
    ]