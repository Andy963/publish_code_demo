

# import os
#
#
# from git import Repo
# from git import Git
# git_ssh_identity_file = os.path.join(os.getcwd(),'../../rsa/id_rsa')
# git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
# Repo.clone_from('https://gitee.com/andy963/blog.git', os.path.join(os.getcwd(), 'blog'),env=dict(GIT_SSH_COMMAND=git_ssh_cmd))
import os
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir = os.path.dirname(BASE_DIR)
private_key_path = os.path.join(dir, 'rsa/id_rsa')

print(private_key_path)