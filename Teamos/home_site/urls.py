__author__ = "Samuel Simun - xsimun04@fit.vutbr.cz"

from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("register", views.register, name="register"),
    path("login", views.login_request, name="login"),
]
