from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.base, name='base'),
    url(r'^manage/$', views.index, name='index'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^invite/$', views.first_time, name='firsttime'),
    url(r'^addproduct/$', views.add_product, name='add_product'),
    url(r'^', views.product),
]
