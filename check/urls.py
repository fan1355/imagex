from django.urls import path

from . import views

urlpatterns = [
    path('hsv', views.hsv_check, name='hsv_check'),
    path('pos', views.position_check, name='position_check'),
    path('info', views.get_info, name='get_info'),
    path('pic', views.show_pic, name='show_pic'),

]