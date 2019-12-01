#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
from django import forms


class BootStrapModelForm(forms.ModelForm):
    # 为表彰添加bootstrap 类样式
    exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in self.exclude_fields:
                field.widget.attrs.update({'class': "form-control"})
