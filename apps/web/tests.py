import os

from git import Repo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(BASE_DIR)
private_key_path = os.path.join(root_dir, 'rsa/id_rsa')
git_ssh_cmd = 'ssh -i %s' % private_key_path
Repo.clone_from('https://gitee.com/andy963/blog.git', os.path.join(os.getcwd(), 'blog'),
                env=dict(GIT_SSH_COMMAND=git_ssh_cmd))
