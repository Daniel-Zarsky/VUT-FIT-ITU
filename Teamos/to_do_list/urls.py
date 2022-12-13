
from django.contrib import admin
from django.urls import path, include

from . import views, List_of_tasks

urlpatterns = [
    path('', views.List_of_tasks, name='taskList'),
    path("addTask", views.addTask, name='addTask'),
    path("submit_task", views.submit_task, name='submit_task'),
    path("delete_task", views.delete_task, name='delete_task'),
    path("save_task", views.save_task, name='save_task')
]
