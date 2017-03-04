from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name = 'index'),
    url(r'^addNewWifi/$', views.addNewWifi, name = 'addNewWifi'),
    url(r'^findWifiPoints/$', views.findWifiPoints, name = 'findWifiPoints'),
]