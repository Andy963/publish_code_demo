#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
# 封装response对象，用于返回字典格式数据

class BaseResponse(object):

    def __init__(self, status=True, data=None, error=None):
        self.status = status
        self.data = data
        self.error = error

    @property
    def dict(self):
        return self.__dict__
