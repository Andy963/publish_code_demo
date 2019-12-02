#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'home', home, name='home'),

    url(r'server/list/$', server, name='server'),
    url(r'server/edit/(?P<pk>\d+)/$', server_edit, name='server_edit'),
    url(r'server/add/$', server_add, name='server_add'),
    url(r'server/delete/(?P<pk>\d+)/$', server_delete, name='server_delete'),

    url(r'rsa/list/$', rsa, name='rsa'),
    url(r'rsa/add/$', rsa_add, name='rsa_add'),
    url(r'rsa/delete/(?P<pk>\d+)/$', rsa_delete, name='rsa_delete'),
    url(r'rsa/edit/(?P<pk>\d+)/$', rsa_edit, name='rsa_edit'),

    url(r'project/list/$', project, name='project'),
    url(r'project/add/$', project_add, name='project_add'),
    url(r'project/delete/(?P<pk>\d+)/$', project_delete, name='project_delete'),
    url(r'project/edit/(?P<pk>\d+)/$', project_edit, name='project_edit'),

    url(r'project/env/list/$', project_env, name='project_env'),
    url(r'project/env/delete/(?P<pk>\d+)/$', project_env_delete, name='project_env_delete'),
    url(r'project/env/edit/(?P<pk>\d+)/$', project_env_edit, name='project_env_edit'),
    url(r'project/env/add/$', project_env_add, name='project_env_add'),

    url(r'deploy/task/list/(?P<env_id>\d+)/$', deploy_task, name='deploy_task'),
    url(r'deploy/task/add/(?P<env_id>\d+)$', deploy_task_add, name='deploy_task_add'),
    url(r'deploy/task/edit/(?P<pk>\d+)$', deploy_task_edit, name='deploy_task_edit'),
    url(r'deploy/task/delete/(?P<pk>\d+)$', deploy_task_delete, name='deploy_task_delete'),

    url(r'deploy/now/(?P<pk>\d+)/$', deploy_now, name='deploy_now'),
    url(r'deploy/channel/(?P<pk>\d+)/$', deploy_by_channel, name='deploy_by_channel'),

    url(r'git/commits/$', git_commits, name='git_commits')
]
