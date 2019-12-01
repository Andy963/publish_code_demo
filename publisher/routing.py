#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.sessions import CookieMiddleware, SessionMiddlewareStack
from apps.web import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        url(r'^channel/(?P<task_id>\d+)/$', consumers.DeployConsumer),
    ])
})
