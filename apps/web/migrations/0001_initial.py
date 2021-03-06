# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-28 07:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeployServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '发布中'), (2, '失败'), (3, '成功')], verbose_name='状态')),
            ],
        ),
        migrations.CreateModel(
            name='DeployServerLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.TextField(verbose_name='日志')),
                ('deploy_server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.DeployServer', verbose_name='上线服务器')),
            ],
        ),
        migrations.CreateModel(
            name='DeployTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(help_text='任务ID格式为：项目-版本-时间，例如 cmdb-v1-201911012359.zip', max_length=64, verbose_name='任务ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '预发布'), (2, '发布中'), (3, '成功'), (4, '失败')], default=1, verbose_name='状态')),
                ('tag', models.CharField(max_length=32, verbose_name='版本')),
                ('branch', models.CharField(max_length=32, verbose_name='分支')),
                ('commit', models.CharField(max_length=40, verbose_name='提交记录')),
                ('deploy_type', models.PositiveSmallIntegerField(choices=[(1, '全量服务器上线'), (2, '自定义服务器上线')], verbose_name='上线类型')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='项目名')),
                ('repo', models.URLField(verbose_name='git仓库地址')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectEnv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('env', models.IntegerField(choices=[(1, '测试'), (2, '正式')], verbose_name='环境')),
                ('path', models.CharField(max_length=128, verbose_name='线上部署路径')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Project', verbose_name='项目环境')),
            ],
        ),
        migrations.CreateModel(
            name='Rsa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '启用'), (2, '停用')], verbose_name='状态')),
                ('private_key', models.TextField(verbose_name='私钥')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32, verbose_name='主机名')),
            ],
        ),
        migrations.AddField(
            model_name='projectenv',
            name='servers',
            field=models.ManyToManyField(to='web.Server', verbose_name='服务器'),
        ),
        migrations.AddField(
            model_name='deploytask',
            name='deploy_record',
            field=models.ManyToManyField(through='web.DeployServer', to='web.Server', verbose_name='部署记录'),
        ),
        migrations.AddField(
            model_name='deploytask',
            name='env',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.ProjectEnv', verbose_name='环境'),
        ),
        migrations.AddField(
            model_name='deployserver',
            name='deploy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.DeployTask', verbose_name='部署'),
        ),
        migrations.AddField(
            model_name='deployserver',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Server', verbose_name='服务器'),
        ),
    ]
