#!usr/bin/env python
# *- coding:utf-8 -*-
# Author: Andy
import json
import time
import shutil
import os

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from django.conf import settings

from apps.web import models
from utils.repository import GitRepository
from utils.ssh import SSHProxy


class DeployConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        self.accept()

        task_id = self.scope['url_route']['kwargs'].get('task_id')
        # 如果获取websoceket通过url传古来的参数
        # task_id=12/11
        # 把当前连接的用户添加到一个QQ群。
        async_to_sync(self.channel_layer.group_add)(task_id, self.channel_name)

    def websocket_receive(self, message):
        print('接收到消息', message)
        # 1. 接受到客户端跟我说开始发布
        # 2. 开始发布，一旦开始之后
        #       每次执行一个步骤，就当前群中发送一个消息。
        task_id = self.scope['url_route']['kwargs'].get('task_id')
        text = message['text']
        deploy_json = json.loads(text)
        if deploy_json.get('action') == 'start':
            async_to_sync(self.channel_layer.group_send)(task_id, {
                'type': 'send_message',
                'message': '{"status":200,"msg":"开始...","percent":10}'
            })

            deploy_task_obj = models.DeployTask.objects.filter(pk=task_id).first()
            # 获取任务环境
            task_env = deploy_task_obj.env
            task_project_repo = task_env.project.repo

            msg = {
                "status": 200,
                "msg": "正在连接到",
                "percent": 30
            }
            async_to_sync(self.channel_layer.group_send)(task_id, {
                'type': 'send_message',
                'message': json.dumps(msg)
            })

            repo_addr = task_project_repo
            project_name = repo_addr.rsplit('/')[-1].split('.')[0]
            local_repo_path = os.path.join(settings.LOCAL_REPO_BASE_PATH, project_name)
            msg = {
                "status": 200,
                "msg": "正在拉取代码",
                "percent": 50
            }

            async_to_sync(self.channel_layer.group_send)(task_id, {
                'type': 'send_message',
                'message': json.dumps(msg)
            })
            git = GitRepository(local_repo_path, repo_addr)
            msg = {
                "status": 200,
                "msg": "拉取成功,正准备打包",
                "percent": 70
            }
            async_to_sync(self.channel_layer.group_send)(task_id, {
                'type': 'send_message',
                'message': json.dumps(msg)
            })

            abs_file_path = shutil.make_archive(
                base_name=os.path.join(settings.ZIPREPO_BASE_PATH, project_name),
                format='zip',
                root_dir=local_repo_path
            )
            msg = {
                "status": 200,
                "msg": "打包成功,开始上传",
                "percent": 80
            }
            async_to_sync(self.channel_layer.group_send)(task_id, {
                'type': 'send_message',
                'message': json.dumps(msg)
            })

            BASE_DIR = settings.BASE_DIR
            msg = {
                "status": 200,
                "msg": "上传成功, 开始解压",
                "percent": 90
            }
            async_to_sync(self.channel_layer.group_send)(task_id, {
                'type': 'send_message',
                'message': json.dumps(msg)
            })
            private_key_path = os.path.join(BASE_DIR, 'rsa/id_rsa')
            remote_file_path = os.path.join('/opt', project_name + '.zip')
            with SSHProxy('107.174.101.162', 5188, 'root', private_key_path=private_key_path) as ssh:
                ssh.upload(abs_file_path, remote_file_path)

            msg = {
                "status": 200,
                "msg": "解压完成",
                "percent": 100
            }
            async_to_sync(self.channel_layer.group_send)(task_id, {
                'type': 'send_message',
                'message': json.dumps(msg)
            })

        # TODO 发布成功要将task_status 改成发布成功

    def send_message(self, event):
        print('发送消息%s' % event['message'])
        message = event['message']
        self.send(message)
        time.sleep(1)

    # websocket_disconnect 使用时用.
    def websocket_disconnect(self, message):
        task_id = self.scope['url_route']['kwargs'].get('task_id')
        async_to_sync(self.channel_layer.group_discard)(task_id, self.channel_name)
        raise StopConsumer() # 服务端主动断开连接
