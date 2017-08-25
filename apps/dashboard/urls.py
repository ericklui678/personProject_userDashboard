from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^users/create$', views.user_create),
    url(r'^users/login$', views.user_login),
    url(r'^users/logoff$', views.user_logoff),
    url(r'^dashboard$', views.dashboard),
]
