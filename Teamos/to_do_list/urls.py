__author__ = "Daniel Zarsky - xzarsk04@fit.vutbr.cz"

from django.urls import path, include
from . import views
app_name ="to_do_list"

urlpatterns = [
    path('', views.tasklist, name='tasklist'),
    path("addTask", views.addTask, name='addTask'),
    path("home", views.home, name='home'),
    path("view_teams", views.view_teams, name='view_teams'),
    path("view_projects", views.view_projects, name='view_projects'),
    path("task_delete/<str:pk>/", views.TaskUpdateDelete.as_view(), name='task_delete'),
    path("task_done/<str:pk>/", views.TaskUpdateDone.as_view(), name='task_done'),
    path("show_done", views.TaskShowDone.as_view(), name='show_done'),

]
