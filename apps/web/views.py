import os
import shutil

from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View

from utils.repository import GitRepository
from utils.ssh import SSHProxy
from apps.web import models
from apps.web import forms


# Create your views here.


def fetch(request):
    if request.method == 'POST':
        repo_addr = request.POST.get('repo_addr')
        project_name = repo_addr.rsplit('/')[-1].split('.')[0]
        local_repo_path = os.path.join(settings.LOCAL_REPO_BASE_PATH, project_name)
        git = GitRepository(local_repo_path, repo_addr)

        abs_file_path = shutil.make_archive(
            base_name=os.path.join(settings.ZIPREPO_BASE_PATH, project_name),
            format='zip',
            root_dir=local_repo_path
        )
        with SSHProxy('127.0.0.1', 2222, 'root', password='zjgisadmin') as ssh:
            ssh.upload(abs_file_path, os.path.join('/opt', project_name + '.zip'))
    return render(request, 'web/index.html')


def home(request):
    servers = models.Server.objects.all()
    context = {
        'servers': servers,
    }
    return render(request, 'web/server.html', context)


def rsa(request):
    rsas = models.Rsa.objects.all()
    context = {
        'rsas': rsas,
    }
    return render(request, 'web/rsa.html', context)


def rsa_delete(request, pk):
    rsa_obj = models.Rsa.objects.filter(pk=pk).first()
    rsa_obj.delete()
    return redirect('web:rsa_list')


def rsa_add_edit(request, pk=None):
    if request.method == 'GET':
        # 编辑rsa
        if pk:
            rsa_obj = models.Rsa.objects.filter(pk=pk).first()
            rsa_form = forms.RsaForm(instance=rsa_obj)
            context = {'rsa_form': rsa_form}
            return render(request, 'web/rsa_add_edit.html', context)

        # 添加rsa
        rsa_form = forms.RsaForm()
        context = {'rsa_form': rsa_form}
        return render(request, 'web/rsa_add_edit.html', context)
    else:
        # 提交编辑
        if pk:
            rsa_obj = models.Rsa.objects.filter(pk=pk).first()
            rsa_form = forms.RsaForm(instance=rsa_obj, data=request.POST)
            if rsa_form.is_valid():
                rsa_form.save()
                return redirect('web:rsa_list')
            context = {'rsa_form': rsa_form}
            return render(request, 'web/rsa_add_edit.html', context)

        # 提交添加rsa
        rsa_form = forms.RsaForm(data=request.POST)
        if rsa_form.is_valid():
            rsa_form.save()
            return redirect('web:rsa_list')
        context = {'rsa_form': rsa_form}
        return render(request, 'web/rsa_add_edit.html', context)


class ServerAddEdit(View):
    def get(self, request, pk=None):
        # 有id时为编辑服务器
        if pk:
            server = models.Server.objects.filter(pk=pk).first()
            server_form = forms.ServerForm(instance=server)
            context = {
                'server_form': server_form,
            }
            return render(request, 'web/server_edit.html', context)
        # 添加服务器
        server_form = forms.ServerForm()
        context = {
            'server_form': server_form,
        }
        return render(request, 'web/server_add_edit.html', context)

    def post(self, request, pk=None):
        # 有Pk是编辑的提交
        if pk:
            server = models.Server.objects.filter(pk=pk).first()
            server_form = forms.ServerForm(data=request.POST, instance=server)
            if server_form.is_valid():
                server_form.save()
                return redirect('web:server_list')
            context = {'server_form': server_form}
            return render(request, 'web/server_edit.html', context)

        # 没有pk值，添加服务器的提交
        server_form = forms.ServerForm(data=request.POST)
        if server_form.is_valid():
            server_form.save()
            return redirect('web:server_list')
        context = {'server_form': server_form}
        return render(request, 'web/server_add_edit.html', context)


def server_list(request):
    servers = models.Server.objects.all()
    context = {
        'servers': servers,
    }
    return render(request, 'web/server.html', context)


def server_delete(request, pk):
    server = models.Server.objects.filter(pk=pk).first()
    server.delete()
    return redirect('web:server_list')


def project(request):
    projects = models.Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'web/project.html', context)


def project_delete(request, pk):
    project_obj = models.Project.objects.filter(pk=pk).first()
    project_obj.delete()
    return redirect('web:project_list')


def project_add_edit(request, pk=None):
    if request.method == 'GET':
        # 有pk时为编辑
        if pk:
            project_obj = models.Project.objects.filter(pk=pk).first()
            project_form = forms.ProjectForm(instance=project_obj)
            context = {'project_form': project_form}
            return render(request, 'web/project_add_edit.html', context)

        # 没有Pk 添加项目
        project_form = forms.ProjectForm()
        context = {'project_form': project_form}
        return render(request, 'web/project_add_edit.html', context)
    else:
        # 编辑
        if pk:
            project_obj = models.Project.objects.filter(pk=pk).first()
            project_form = forms.ProjectForm(instance=project_obj, data=request.POST)
            if project_form.is_valid():
                project_form.save()
                return redirect('web:project_list')
            context = {"project_form": project_form}
            return render(request, 'web/project_add_edit.html', context)
        project_form = forms.ProjectForm(data=request.POST)
        if project_form.is_valid():
            project_form.save()
            return redirect('web:project_list')
        context = {'project_form': project_form}
        return render(request, 'web/project_add_edit.html', context)


def project_env(request):
    project_envs = models.ProjectEnv.objects.all()
    context = {'project_envs': project_envs}
    return render(request, 'web/project_env.html', context)


def project_env_delete(request, pk):
    project_env_obj = models.ProjectEnv.objects.filter(pk=pk).first()
    project_env_obj.delete()
    return redirect('web:project_env_list')


def project_env_add_edit(request, pk=None):
    if request.method == 'GET':
        # 编辑project_env
        if pk:
            project_env_obj = models.ProjectEnv.objects.filter(pk=pk).first()
            project_env_form = forms.ProjectEnvForm(instance=project_env_obj)
            context = {'project_env_form': project_env_form}
            return render(request, 'web/project_env_add_edit.html', context)

        # 添加project_env
        project_env_form = forms.ProjectEnvForm()
        context = {'project_env_form': project_env_form}
        return render(request, 'web/project_env_add_edit.html', context)


    else:
        # 提交编辑
        if pk:
            project_env_obj = models.ProjectEnv.objects.filter(pk=pk).first()
            project_env_form = forms.ProjectEnvForm(instance=project_env_obj, data=request.POST)
            if project_env_form.is_valid():
                # FIXME 不能直接保存
                project_env_form.save()
                return redirect('web:project_env_list')
            context = {'project_env_form': project_env_form}
            return render(request, 'web/project_env_add_edit.html', context)

        # 提交添加
        project_env_form = forms.ProjectEnvForm(data=request.POST)
        if project_env_form.is_valid():
            # FIXME 不能直接保存
            project_env_form.save()
            return redirect('web:project_env_list')
        context = {'project_env_form': project_env_form}
        return render(request, 'web/project_env_add_edit.html', context)
