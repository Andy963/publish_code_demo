# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-29 01:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsa',
            name='username',
            field=models.CharField(default='root', max_length=32, verbose_name='用户'),
        ),
    ]
