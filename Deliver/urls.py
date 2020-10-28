from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.orders, name='orders'),
    url(r'login/', views.cour_login, name='cour_login'),
    url(r'invite/', views.cour_first_time, name='cour_first_time'),
    url(r'logout/', views.cour_logout, name='cour_logout'),
    url(r'order_info', views.order_info),
    url(r'cour_panel', views.cour_panel, name='cour_panel'),
]
