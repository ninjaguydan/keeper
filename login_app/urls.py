from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('signup', views.signup),
    path('login', views.login),
    path('dummi', views.dummi_login),
]