#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'fetch/', fetch, name='fetch'),
    url(r'home', home, name='home'),

    url(r'server/$', ServerAddEdit.as_view(), name='server'),
    url(r'server/(?P<pk>\d+)/$', ServerAddEdit.as_view(), name='server'),
    url(r'server_list/$', server_list, name='server_list'),
    url(r'server_delete/(?P<pk>\d+)/$', server_delete, name='server_delete'),

    url(r'rsa_list/$', rsa, name='rsa_list'),
    url(r'rsa/delete/(?P<pk>\d+)/$', rsa_delete, name='rsa_delete'),
    url(r'rsa/$', rsa_add_edit, name='rsa_add_edit'),
    url(r'rsa/(?P<pk>\d+)/$', rsa_add_edit, name='rsa_add_edit'),

    url(r'project_list/$', project, name='project_list'),
    url(r'project/delete/(?P<pk>\d+)/$', project_delete, name='project_delete'),
    url(r'project/(?P<pk>\d+)/$', project_add_edit, name='project_add_edit'),
    url(r'project/$', project_add_edit, name='project_add_edit'),

    url(r'project_env_list/$', project_env, name='project_env_list'),
    url(r'project_env/delete/(?P<pk>\d+)/$', project_delete, name='project_env_delete'),
    url(r'project_env/(?P<pk>\d+)/$', project_env_add_edit, name='project_env_add_edit'),
    url(r'project_env/$', project_env_add_edit, name='project_env_add_edit'),

]
