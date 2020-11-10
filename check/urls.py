from django.urls import path

from . import views
from . import views_cap
from . import views_list

urlpatterns = [
    path('hsv', views.hsv_check, name='hsv_check'),
    path('multihsv', views.multi_hsv_check, name='multi_hsv_check'),
    path('pos', views.position_check, name='position_check'),
    path('info', views.get_info, name='get_info'),
    path('pic', views.show_pic, name='show_pic'),

    path('cap', views_cap.cap, name='cap'),
    path('cap2', views_cap.cap2, name='cap2'),
    path('cap4', views_cap.cap4, name='cap4'),
    path('cap5', views_cap.cap5, name='cap5'),
    path('cap6', views_cap.cap6, name='cap6'),
    path('cap7', views_cap.cap7, name='cap7'),
    path('cap_phone', views_cap.cap_phone, name='cap_phone'),

    path('list', views_list.checkList, name='list'),
    path('std', views_list.get_info, name='std'),

]
