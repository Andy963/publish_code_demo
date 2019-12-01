import os
import copy
import shutil
import uuid

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views import View

from utils.repository import GitRepository
from utils.ssh import SSHProxy
from apps.web import models
from apps.web import forms
from utils import custom_paginator
from utils.response import BaseResponse


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
    # 获取所有私钥列表
    try:
        rsas = models.Rsa.objects.all()
        request_data = copy.copy(request.GET)
        cur_page_num = request.GET.get('page')
        total_count = rsas.count()
        obj_per_page = settings.PER_PAGE_COUNT
        page_tab_num = settings.PAGE_NUMBER_SHOW
        page_obj = custom_paginator.CustomPage(cur_page_num, total_count, obj_per_page, page_tab_num,
                                               request_data)
        rsa_list = rsas[page_obj.start_data_number:page_obj.end_data_number]
        page_html = page_obj.page_html_func()
        context = {
            'rsas': rsa_list,
            'page_html': page_html,
        }
    except ConnectionError:
        return render(request, '404.html')

    return render(request, 'web/rsa.html', context)


def rsa_delete(request, pk):
    models.Rsa.objects.filter(pk=pk).delete()
    return redirect('web:rsa_list')


def rsa_add(request):
    # 添加rsa
    if request.method == 'GET':
        # 添加rsa
        rsa_form = forms.RsaForm()
        context = {'rsa_form': rsa_form}
        return render(request, 'web/rsa_add_edit.html', context)
    else:
        rsa_form = forms.RsaForm(data=request.POST)
        if rsa_form.is_valid():
            rsa_form.save()
            return redirect('web:rsa_list')
        context = {'rsa_form': rsa_form}
        return render(request, 'web/rsa_add_edit.html', context)


def rsa_edit(request, pk):
    # 编辑rsa
    if request.method == 'GET':
        rsa_obj = models.Rsa.objects.filter(pk=pk).first()
        rsa_form = forms.RsaForm(instance=rsa_obj)
        context = {'rsa_form': rsa_form}
        return render(request, 'web/rsa_add_edit.html', context)
    else:
        rsa_obj = models.Rsa.objects.filter(pk=pk).first()
        rsa_form = forms.RsaForm(instance=rsa_obj, data=request.POST)
        if rsa_form.is_valid():
            rsa_form.save()
            return redirect('web:rsa_list')
        context = {'rsa_form': rsa_form}
        return render(request, 'web/rsa_add_edit.html', context)


def server(request):
    # 服务器列表
    try:
        servers = models.Server.objects.all()
        request_data = copy.copy(request.GET)
        cur_page_num = request.GET.get('page')
        total_count = servers.count()
        obj_per_page = settings.PER_PAGE_COUNT
        page_tab_num = settings.PAGE_NUMBER_SHOW
        page_obj = custom_paginator.CustomPage(cur_page_num, total_count, obj_per_page, page_tab_num,
                                               request_data)
        servers = servers[page_obj.start_data_number:page_obj.end_data_number]
        page_html = page_obj.page_html_func()
        context = {
            'servers': servers,
            'page_html': page_html,
        }
    except ConnectionError:
        return render(request, '404.html')

    return render(request, 'web/server.html', context)


def server_delete(request, pk):
    models.Server.objects.filter(pk=pk).delete()
    return redirect('web:server_list')


def server_add(request):
    # 添加server
    if request.method == 'GET':

        server_form = forms.ServerForm()
        context = {'form': server_form}
        return render(request, 'web/add_edit_form.html', context)
    else:
        server_form = forms.ServerForm(data=request.POST)
        if server_form.is_valid():
            server_form.save()
            return redirect('web:server')
        context = {'form': server_form}
        return render(request, 'web/add_edit_form.html', context)


def server_edit(request, pk):
    # 编辑server
    server_obj = models.Server.objects.filter(pk=pk).first()
    if request.method == 'GET':
        server_form = forms.ServerForm(instance=server_obj)
        context = {'form': server_form}
        return render(request, 'web/add_edit_form.html', context)
    else:
        server_form = forms.ServerForm(instance=server_obj, data=request.POST)
        if server_form.is_valid():
            server_form.save()
            return redirect('web:server')
        context = {'form': server_form}
        return render(request, 'web/add_edit_form.html', context)


def project(request):
    projects = models.Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'web/project.html', context)


def project_delete(request, pk):
    project_obj = models.Project.objects.filter(pk=pk).first()
    project_obj.delete()
    return redirect('web:project')


def project_add(request):
    if request.method == 'GET':
        project_form = forms.ProjectForm()
        context = {'form': project_form}
        return render(request, 'web/add_edit_form.html', context)
    else:
        project_form = forms.ProjectForm(data=request.POST)
        if project_form.is_valid():
            project_form.save()
            return redirect('web:project')
        context = {'form': project_form}
        return render(request, 'web/add_edit_form.html', context)


def project_edit(request, pk):
    if request.method == 'GET':

        project_obj = models.Project.objects.filter(pk=pk).first()
        project_form = forms.ProjectForm(instance=project_obj)
        context = {'form': project_form}
        return render(request, 'web/add_edit_form.html', context)
    else:
        project_obj = models.Project.objects.filter(pk=pk).first()
        project_form = forms.ProjectForm(instance=project_obj, data=request.POST)
        if project_form.is_valid():
            project_form.save()
            return redirect('web:project')
        context = {"form": project_form}
        return render(request, 'web/add_edit_form.html', context)


def project_env(request):
    project_envs = models.ProjectEnv.objects.all()
    context = {'project_envs': project_envs}
    return render(request, 'web/project_env.html', context)


def project_env_delete(request, pk):
    project_env_obj = models.ProjectEnv.objects.filter(pk=pk).first()
    project_env_obj.delete()
    return redirect('web:project_env')


def project_env_add(request):
    if request.method == 'GET':
        project_env_form = forms.ProjectEnvForm()
        context = {'form': project_env_form}
        return render(request, 'web/add_edit_form.html', context)
    else:
        project_env_form = forms.ProjectEnvForm(data=request.POST)
        if project_env_form.is_valid():
            project_env_form.save()
            return redirect('web:project_env')
        context = {'form': project_env_form}
        return render(request, 'web/add_edit_form.html', context)


def project_env_edit(request, pk):
    if request.method == 'GET':
        project_env_obj = models.ProjectEnv.objects.filter(pk=pk).first()
        project_env_form = forms.ProjectEnvForm(instance=project_env_obj)
        context = {'form': project_env_form}
        return render(request, 'web/add_edit_form.html', context)
    else:
        project_env_obj = models.ProjectEnv.objects.filter(pk=pk).first()
        project_env_form = forms.ProjectEnvForm(instance=project_env_obj, data=request.POST)
        if project_env_form.is_valid():
            project_env_form.save()
            return redirect('web:project_env')
        context = {'form': project_env_form}
        return render(request, 'web/add_edit_form.html', context)


def deploy_task(request, env_id):
    project_env_obj = models.ProjectEnv.objects.filter(pk=env_id).first()
    deploy_tasks = models.DeployTask.objects.filter(env=project_env_obj)

    context = {'deploy_tasks': deploy_tasks,
               'project_env_obj': project_env_obj
               }
    return render(request, 'web/deploy_task.html', context)


def deploy_task_add(request, env_id):
    env_object = models.ProjectEnv.objects.filter(id=env_id).first()  # 将env_object传给form表单，获取关联表的值
    if request.method == 'GET':
        deploy_task_form = forms.DeployTaskForm(env_object)
        context = {'deploy_task_form': deploy_task_form, 'env_object': env_object}
        return render(request, 'web/deploy_task_add_edit.html', context)
    else:

        deploy_task_form = forms.DeployTaskForm(env_object, data=request.POST)
        if deploy_task_form.is_valid():
            deploy_task_form.save()
            return redirect(reverse('web:deploy_task', kwargs={'env_id': env_id}))
        context = {'form': deploy_task_form,
                   'env_object':env_object,
                   }
        return render(request, 'web/add_edit_form.html', context)


def deploy_task_edit(request, pk):
    if request.method == 'GET':
        deploy_task_obj = models.DeployTask.objects.filter(pk=pk).first()
        deploy_task_form = forms.DeployStatusForm(instance=deploy_task_obj)
        context = {'form': deploy_task_form}
        return render(request, 'web/add_edit_form.html', context)
    else:
        deploy_task_obj = models.DeployTask.objects.filter(pk=pk).first()
        deploy_task_env = deploy_task_obj.env
        # FIXME delete this
        print(deploy_task_env, type(deploy_task_env))
        deploy_task_form = forms.DeployStatusForm(instance=deploy_task_obj, data=request.POST)
        if deploy_task_form.is_valid():
            deploy_task_obj.save(update_fields=['status', ])
        return redirect(reverse('web:deploy_task', kwargs={'env_id': deploy_task_env.id}))


def deploy_task_delete(request, pk):
    deploy_task_obj = models.DeployTask.objects.filter(pk=pk).first()
    deploy_task_env = deploy_task_obj.env
    models.DeployTask.objects.filter(pk=pk).delete()
    return redirect(reverse('web:deploy_task', kwargs={'env_id': deploy_task_env.id}))


from utils import repository


def deploy_now(rquest, pk):
    # pk： task_id
    deploy_task_obj = models.DeployTask.objects.filter(pk=pk).first()
    # 获取任务环境
    task_env = deploy_task_obj.env
    task_project_repo = task_env.project.repo

    repo_addr = task_project_repo
    project_name = repo_addr.rsplit('/')[-1].split('.')[0]
    local_repo_path = os.path.join(settings.LOCAL_REPO_BASE_PATH, project_name)
    git = GitRepository(local_repo_path, repo_addr)

    abs_file_path = shutil.make_archive(
        base_name=os.path.join(settings.ZIPREPO_BASE_PATH, project_name),
        format='zip',
        root_dir=local_repo_path
    )
    # with SSHProxy('127.0.0.1', 2222, 'root', password='zjgisadmin') as ssh:
    #     ssh.upload(abs_file_path, os.path.join('/opt', project_name + '.zip'))
    return HttpResponse('hello ')


def git_commits(request):
    response = BaseResponse()
    try:
        env_id = request.GET.get('env_id')
        branch = request.GET.get('branch')

        env_object = models.ProjectEnv.objects.filter(id=env_id).first()
        repo_url = env_object.project.repo
        project_name = env_object.project.title
        local_path = os.path.join(settings.LOCAL_REPO_BASE_PATH, project_name)
        repo_object = GitRepository(local_path, repo_url)

        # 先切换分支
        repo_object.change_to_branch(branch)
        # 获取所有提交记录
        commit_list = repo_object.commits()
        response.data = commit_list

    except Exception:
        response.status = False
        response.error = '版本获取 失败'
    return JsonResponse(response.dict)


def deploy_by_channel(request, pk):
    # pk: task_id
    deploy_task_obj = models.DeployTask.objects.filter(pk=pk).first()
    deploy_server_list = models.DeployServer.objects.filter(deploy=deploy_task_obj)
    context = {
        'deploy_server_list':deploy_server_list,
    }

    return render(request, 'web/deploy_by_channel.html', context)


