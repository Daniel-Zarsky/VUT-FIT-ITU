from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.list_projects, name='list_projects'),
    path('create_new', views.create_new, name='create_new')
    ]