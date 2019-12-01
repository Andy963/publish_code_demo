#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
from django import template

register = template.Library()


@register.simple_tag
def un_deploy_num(env_object):
    print(env_object.deploytask_set.all())
    total = env_object.deploytask_set.all().count()
    un_deploy = env_object.deploytask_set.filter(status=1).count()
    msg = "%s/%s" %(un_deploy,total)
    print(msg)
    return msg