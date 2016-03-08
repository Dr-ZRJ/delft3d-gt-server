# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-08 14:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('delft3dworker', '0009_auto_20160205_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workerid', models.CharField(editable=False, max_length=256)),
                ('workingdir', models.CharField(editable=False, max_length=256)),
                ('fileurl', models.CharField(editable=False, max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('status', models.CharField(max_length=256)),
                ('info', models.CharField(max_length=256)),
                ('json', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(editable=False, max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('status', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='TaskProc',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='delft3dworker.Task')),
                ('script', models.CharField(max_length=256, verbose_name=b'File name of script to run')),
                ('fileurl', models.CharField(editable=False, max_length=256)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delft3dworker.SimRun')),
            ],
            bases=('delft3dworker.task',),
        ),
        migrations.CreateModel(
            name='TaskSim',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='delft3dworker.Task')),
                ('run', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='delft3dworker.SimRun')),
            ],
            bases=('delft3dworker.task',),
        ),
        migrations.CreateModel(
            name='TaskVis',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='delft3dworker.Task')),
                ('script', models.CharField(max_length=256, verbose_name=b'File name of script to run')),
                ('fileurl', models.CharField(editable=False, max_length=256)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delft3dworker.SimRun')),
            ],
            bases=('delft3dworker.task',),
        ),
    ]
