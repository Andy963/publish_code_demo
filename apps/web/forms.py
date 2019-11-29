#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy

from django import forms

from apps.web import models

class ServerForm(forms.ModelForm):
    class Meta:
        model=models.Server
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    class Meta:
        model=models.Project
        fields = '__all__'


class RsaForm(forms.ModelForm):
    class Meta:
        model = models.Rsa
        fields = '__all__'


class ProjectEnvForm(forms.ModelForm):
    class Meta:
        model=models.ProjectEnv
        fields = '__all__'