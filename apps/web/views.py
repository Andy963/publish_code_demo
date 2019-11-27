import os
import shutil

from django.shortcuts import render
from django.conf import settings

from utils.repository import GitRepository
from utils.ssh import SSHProxy


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
            ssh.upload(abs_file_path, os.path.join('/opt', project_name+'.zip'))
    return render(request, 'web/index.html')
