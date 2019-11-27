#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
from django.conf.urls import url
from .views import fetch

urlpatterns = [
    url(r'fetch/', fetch, name='fetch'),
]
