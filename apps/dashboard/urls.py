from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^users/create$', views.user_create),
    url(r'^users/login$', views.user_login),
    url(r'^users/logoff$', views.user_logoff),
    url(r'^users/edit/(?P<id>\d+)$', views.user_edit),
    url(r'^users/update/(?P<id>\d+)$', views.update),
]
