# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-22 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dangjiansite', '0027_auto_20180322_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinfo',
            name='create_time',
            field=models.CharField(default='20:05:20', max_length=50, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='helpinfo',
            name='create_time',
            field=models.CharField(default='20:05:20', max_length=50, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='studyinfo',
            name='create_time',
            field=models.CharField(default='20:05:20', max_length=50, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='thumbinfo',
            name='create_time',
            field=models.CharField(default='20:05:20', max_length=50, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='viewinfo',
            name='create_time',
            field=models.CharField(default='20:05:20', max_length=50, verbose_name='创建时间'),
        ),
    ]