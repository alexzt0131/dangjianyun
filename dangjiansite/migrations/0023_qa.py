# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-20 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dangjiansite', '0022_examdetail_examinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=500, verbose_name='问题')),
                ('answer', models.CharField(max_length=50, verbose_name='答案')),
                ('answerText', models.CharField(max_length=50, verbose_name='文本答案')),
            ],
        ),
    ]
