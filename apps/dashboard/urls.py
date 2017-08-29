from django.conf.urls import url
from __future__ import absolute_import

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),

    url(r'^users/create$', views.user_create),
    url(r'^users/login$', views.user_login),
    url(r'^users/logoff$', views.user_logoff),
    url(r'^users/edit/(?P<id>\d+)$', views.user_edit),
    url(r'^users/update/(?P<id>\d+)$', views.update),
    url(r'^users/profile$', views.profile),
    url(r'^users/profile/update$', views.profile_update),
    url(r'^users/show/(?P<id>\d+)$', views.show),
    url(r'^users/delete/(?P<id>\d+)$', views.user_delete),

    url(r'^post/create/(?P<id>\d+)$', views.post_create),
    url(r'^comment/create/(?P<post_id>\d+)/(?P<user_id>\d+)/(?P<wall_id>\d+)$', views.comment_create),
]
