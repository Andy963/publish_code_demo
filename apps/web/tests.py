

import os


from git import Repo
from git import Git
git_ssh_identity_file = os.path.join(os.getcwd(),'../../rsa/id_rsa')
git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
Repo.clone_from('https://gitee.com/andy963/blog.git', os.path.join(os.getcwd(), 'blog'),env=dict(GIT_SSH_COMMAND=git_ssh_cmd))