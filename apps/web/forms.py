#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
import os
import datetime
import shutil

from django import forms
from django.forms.widgets import Select
from django.core.exceptions import ValidationError

from apps.web import models
from .bootstrap import BootStrapModelForm
from utils.repository import GitRepository
from django.conf import settings


class ServerForm(BootStrapModelForm):
    class Meta:
        model = models.Server
        fields = '__all__'


class ProjectForm(BootStrapModelForm):
    class Meta:
        model = models.Project
        fields = '__all__'


class RsaForm(BootStrapModelForm):
    class Meta:
        model = models.Rsa
        fields = '__all__'


class ProjectEnvForm(BootStrapModelForm):
    class Meta:
        model = models.ProjectEnv
        fields = '__all__'


class DeployTaskForm(BootStrapModelForm):
    # 自定义字段
    deploy_server = forms.MultipleChoiceField(label='自定义服务器',required=False)

    class Meta:
        model = models.DeployTask
        exclude = ['uid', 'status', 'env']

        widgets = {
            'tag': Select(choices=[]),
            'branch': Select(choices=[]),
            'commit': Select(choices=[]),
        }

    def __init__(self, env_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env_object = env_object
        # 使用widget.choices提交时会与数据库中数据 进行校验
        self.fields['deploy_server'].choices = env_object.servers.values_list('id', 'hostname')

        self.init_git(env_object)

    def init_git(self, env_object):
        """
        初始化git 信息，为动态显示tag, branch, commit
        :param env_object: 项目环境对象
        :return:
        """
        # 获取项目的git对象
        repo_url = env_object.project.repo
        project_name = env_object.project.title
        local_repo_path = os.path.join(settings.LOCAL_REPO_BASE_PATH, project_name)

        repo_object = GitRepository(local_repo_path, repo_url)

        # 为了获取最新的记录， pull
        # # TODO 判断，如果本地文件,压缩包已经存在，先删除再拉取
        # local_repo_zip_file = os.path.join(settings.ZIPREPO_BASE_PATH, project_name)
        # if os.path.exists(local_repo_zip_file):
        #     os.remove(local_repo_zip_file)
        #
        # if os.path.exists(local_repo_path):
        #     print('本地git已经存在')
        #     shutil.rmtree(local_repo_path)
        #     os.mkdir(local_repo_path)
        # repo_object.pull() FIXME

        # 得到所有的tag,赋值给选项
        tag_choice = [(None, '请选择标签')]
        tags = repo_object.tags()
        tag_choice += [(t, t) for t in tags]
        self.fields['tag'].widget.choices = tag_choice

        # 获取分支
        branch_choice = [(None, '请选择分支')]
        branch_choice += [(b, b) for b in repo_object.branches()]
        self.fields['branch'].widget.choices = branch_choice
        # 提交记录
        commit_choices = [(None, '请选择提交记录')]
        self.fields['commit'].widget.choices = commit_choices
        #

    def clean(self):
        tag = self.cleaned_data.get('tag')
        branch = self.cleaned_data.get('branch')
        commit = self.cleaned_data.get('commit')
        deploy_servers = self.cleaned_data.get('deploy_servers')
        deploy_type = self.cleaned_data.get('deploy_type')
        if deploy_type == 1:  # 全量发布
            # 如果选择服务器，则无效,自己手动获取,self.env_object.servers.all()
            if deploy_servers:
                self.add_error('deploy_servers', '全量上线无需选择服务器')
        elif deploy_type == 2:
            # 获取 客户选择的服务
            if not deploy_servers:
                self.add_error('deploy_server', '请选择服务器')
        else:
            self.add_error('deploy_type', '发布类型错误')
        if tag:
            if branch or commit:  # FIXME 分开写
                self.add_error('branch', '基于tag发布请移除分支')
                self.add_error('commit', '基于tag发布请移除提交记录')
            return self.cleaned_data
        else:
            if not branch:
                self.add_error('branch', '基于提交发布,必须选择分支')
            if not commit:
                self.add_error('commit', '必须选择提交记录')
        if branch and commit:
            return self.cleaned_data
        self.add_error('tag', 'tag或branch任选其一')

        return self.cleaned_data

    def save(self, commit=True):
        self.instance.status = 1  # 默认为待发布状态
        self.instance.env = self.env_object
        self.instance.uid = self.create_uid()
        self.instance.save()

        # 将任务和服务器信息添加到deployserver表中，默认状态为1
        deploy_type = self.cleaned_data.get('deploy_type')
        if deploy_type == 1:
            queryset = self.env_object.servers.all()
            deploy_server_id_list = [item.id for item in queryset]
        else:
            deploy_server_id_list = self.cleaned_data['deploy_servers']
        task_id = self.instance.id  # self.instance 为当前任务的对象
        print(' ---', task_id)
        object_list = []
        for server_id in deploy_server_id_list:
            object_list.append(models.DeployServer(deploy_id=task_id, server_id=server_id))
        models.DeployServer.objects.bulk_create(object_list)
        # super().save(commit=True)

    def create_uid(self):
        # 获取 由项目名，提交记录或者tag 时间组成的uid 信息
        project_name = self.env_object.project.title
        version = self.cleaned_data.get('tag')
        # 如果选择了标签就用标签，如果没有应用提交记录
        if not version:
            version = '%s-%s' % (self.cleaned_data['branch'], self.cleaned_data['commit'])
        date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return "%s-%s-%s" % (project_name, version, date)


class DeployStatusForm(BootStrapModelForm):
    class Meta:
        model = models.DeployTask
        fields = ['status', ]
