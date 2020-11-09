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

    path('list', views_list.checkList, name='list'),

]
