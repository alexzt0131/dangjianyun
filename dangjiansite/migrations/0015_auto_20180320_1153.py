# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-20 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dangjiansite', '0014_auto_20180320_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailydetail',
            name='study2Detail',
        ),
        migrations.AlterField(
            model_name='dailydetail',
            name='study1Detail',
            field=models.TextField(default='', max_length=500, verbose_name='在线阅读学习资料与学习资料写体会详细'),
        ),
    ]
