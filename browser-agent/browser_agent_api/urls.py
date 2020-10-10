from django.contrib import admin
from .views import inform
from .views import register
from django.urls import path

urlpatterns = [
    path('inform/',inform),    
    path('register/',register),
]
