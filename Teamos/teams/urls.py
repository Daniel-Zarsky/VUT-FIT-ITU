from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('create_new', views.create_new, name='create_new'),
    path('invite', views.invite_people, name='invite'),
    path('show_table', views.show_dash, name='show_table')
]
