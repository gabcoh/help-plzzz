from django.conf.urls import url

from . import views

app_name = 'help_plz'
urlpatterns = [
    url(r'^(?P<class_pk>[0-9]+)$', views.get_class, name='class'),
    url(r'^(?P<pk>[0-9]+)/start/$', views.start_request, name='start'),
    url(r'^(?P<pk>[0-9]+)/finish/$', views.finish_request, name='finish'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete_request, name='delete'),
    url(r'^(?P<pk>[0-9]+)/concur/$', views.concur_with_request, name='concur'),
    url(r'^(?P<class_pk>[0-9]+)/help/$',
        views.request_help, name='request_help'),
    url(r'^$', views.account, name='account'),
    url(r'^join/$', views.join_class, name='join_class'),
    url(r'^create/$', views.create_class, name='create_class'),
]
