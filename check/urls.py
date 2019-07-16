from django.urls import path

from . import views

urlpatterns = [
    path('do', views.check, name='check'),
]