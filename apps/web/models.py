from django.db import models


# Create your models here.


class Rsa(models.Model):
    status_choices = (
        (1, '启用'),
        (2, '停用'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices)
    private_key = models.TextField(verbose_name='私钥')

    def __str__(self):
        return self.status


class Server(models.Model):
    hostname = models.CharField(verbose_name='主机名', max_length=32)

    def __str__(self):
        return self.hostname


class Project(models.Model):
    title = models.CharField(verbose_name='项目名', max_length=32)
    repo = models.URLField(verbose_name='git仓库地址')

    def __str__(self):
        return self.title


class ProjectEnv(models.Model):
    project = models.ForeignKey(verbose_name='项目环境', to='Project')
    env_choices = (
        (1, '测试'),
        (2, '正式')
    )
    env = models.IntegerField(verbose_name='环境', choices=env_choices)
    path = models.CharField(verbose_name='线上部署路径', max_length=128)
    servers = models.ManyToManyField(verbose_name='服务器', to='Server')

    def __str__(self):
        return self.project


class DeployTask(models.Model):
    uid = models.CharField(verbose_name='任务ID', max_length=64,
                           help_text="任务ID格式为：项目-版本-时间，例如 cmdb-v1-201911012359.zip")
    status_choices = (
        (1, '预发布'),
        (2, '发布中'),
        (3, '成功'),
        (4, '失败'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)
    env = models.ForeignKey(verbose_name='环境', to='ProjectEnv')
    # 正式发布用tag
    tag = models.CharField(verbose_name='版本', max_length=32)
    # 测试发布用branch 、commit
    branch = models.CharField(verbose_name='分支', max_length=32)
    commit = models.CharField(verbose_name='提交记录', max_length=40)

    deploy_type_choice = (
        (1, '全量服务器上线'),
        (2, '自定义服务器上线'),
    )
    deploy_type = models.PositiveSmallIntegerField(verbose_name='上线类型', choices=deploy_type_choice)
    deploy_record = models.ManyToManyField(verbose_name='部署记录',
                                           to='Server',
                                           through='DeployServer',
                                           through_fields=('deploy', 'server'))

    def __str__(self):
        return self.get_status_display()


class DeployServer(models.Model):
    """
    上线记录
    """
    deploy = models.ForeignKey(verbose_name='部署', to='DeployTask')
    server = models.ForeignKey(verbose_name='服务器', to='Server')
    status_choices = (
        (1, '发布中'),
        (2, '失败'),
        (3, '成功'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices)

    def __str__(self):
        return self.server


class DeployServerLog(models.Model):
    deploy_server = models.ForeignKey(verbose_name='上线服务器', to='DeployServer')
    log = models.TextField(verbose_name='日志')

    def __str__(self):
        return self.deploy_server
