# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-22 07:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dangjiansite', '0026_auto_20180321_2033'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_day', models.CharField(default='2018-03-22', max_length=50, verbose_name='创建日期')),
                ('create_time', models.CharField(default='15:12:33', max_length=50, verbose_name='创建时间')),
                ('reply', models.TextField(max_length=500, verbose_name='回复内容')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('idjinfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dangjiansite.DjInfo', verbose_name='党建用户')),
            ],
        ),
        migrations.CreateModel(
            name='StudyInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_day', models.CharField(default='2018-03-22', max_length=50, verbose_name='创建日期')),
                ('create_time', models.CharField(default='15:12:33', max_length=50, verbose_name='创建时间')),
                ('reply', models.TextField(max_length=500, verbose_name='回复内容')),
                ('title', models.CharField(max_length=150, verbose_name='标题')),
                ('idjinfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dangjiansite.DjInfo', verbose_name='党建用户')),
            ],
        ),
        migrations.CreateModel(
            name='ThumbInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_day', models.CharField(default='2018-03-22', max_length=50, verbose_name='创建日期')),
                ('create_time', models.CharField(default='15:12:33', max_length=50, verbose_name='创建时间')),
                ('reply', models.TextField(max_length=500, verbose_name='回复内容')),
                ('title', models.CharField(max_length=150, verbose_name='标题')),
                ('idjinfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dangjiansite.DjInfo', verbose_name='党建用户')),
            ],
        ),
        migrations.CreateModel(
            name='ViewInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_day', models.CharField(default='2018-03-22', max_length=50, verbose_name='创建日期')),
                ('create_time', models.CharField(default='15:12:33', max_length=50, verbose_name='创建时间')),
                ('pub_content', models.TextField(max_length=500, verbose_name='回复内容')),
                ('idjinfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dangjiansite.DjInfo', verbose_name='党建用户')),
            ],
        ),
        migrations.AddField(
            model_name='examinfo',
            name='create_time',
            field=models.CharField(default='15:12:33', max_length=50, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='dailydetail',
            name='create_day',
            field=models.CharField(default='2018-03-22', max_length=50, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='dailyresult',
            name='create_day',
            field=models.CharField(default='2018-03-22', max_length=50, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='errlog',
            name='create_day',
            field=models.CharField(default='2018-03-22', max_length=50, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='examdetail',
            name='create_day',
            field=models.CharField(default='2018-03-22', max_length=50, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='examinfo',
            name='create_day',
            field=models.CharField(default='2018-03-22', max_length=50, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='thumblog',
            name='create_day',
            field=models.CharField(default='2018-03-22', max_length=50, verbose_name='创建日期'),
        ),
    ]
