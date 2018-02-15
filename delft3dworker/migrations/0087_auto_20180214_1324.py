# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-14 13:24
from __future__ import unicode_literals

import delft3dworker.utils
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delft3dworker', '0086_auto_20170425_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='container_starttime',
            field=models.DateTimeField(blank=True, default=delft3dworker.utils.tz_now),
        ),
        migrations.AlterField(
            model_name='container',
            name='container_stoptime',
            field=models.DateTimeField(blank=True, default=delft3dworker.utils.tz_now),
        ),
        migrations.AlterField(
            model_name='container',
            name='task_starttime',
            field=models.DateTimeField(blank=True, default=delft3dworker.utils.tz_now),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='parameters',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
        migrations.RunSQL('ALTER TABLE delft3dworker_scenario ALTER COLUMN "parameters" TYPE jsonb USING "parameters"::text::jsonb;',
            reverse_sql='ALTER TABLE delft3dworker_scenario ALTER COLUMN "parameters" TYPE text USING "parameters"::text;'
        ),
        migrations.AlterField(
            model_name='scenario',
            name='scenes_parameters',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
        migrations.RunSQL('ALTER TABLE delft3dworker_scenario ALTER COLUMN "scenes_parameters" TYPE jsonb USING "scenes_parameters"::text::jsonb;',
            reverse_sql='ALTER TABLE delft3dworker_scenario ALTER COLUMN "scenes_parameters" TYPE text USING "scenes_parameters"::text;'
        ),
        migrations.AlterField(
            model_name='scene',
            name='date_created',
            field=models.DateTimeField(blank=True, default=delft3dworker.utils.tz_now),
        ),
        migrations.AlterField(
            model_name='scene',
            name='info',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
        migrations.RunSQL('ALTER TABLE delft3dworker_scene ALTER COLUMN "info" TYPE jsonb USING "info"::text::jsonb;',
            reverse_sql='ALTER TABLE delft3dworker_scene ALTER COLUMN "info" TYPE text USING "info"::text;'
        ),
        migrations.AlterField(
            model_name='scene',
            name='parameters',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
        migrations.RunSQL('ALTER TABLE delft3dworker_scene ALTER COLUMN "parameters" TYPE jsonb USING "parameters"::text::jsonb;',
            reverse_sql='ALTER TABLE delft3dworker_scene ALTER COLUMN "parameters" TYPE text USING "parameters"::text;'
        ),
        migrations.AlterField(
            model_name='searchform',
            name='sections',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
        migrations.RunSQL('ALTER TABLE delft3dworker_searchform ALTER COLUMN "sections" TYPE jsonb USING "sections"::text::jsonb;',
            reverse_sql='ALTER TABLE delft3dworker_searchform ALTER COLUMN "sections" TYPE text USING "sections"::text;'
        ),
        migrations.AlterField(
            model_name='searchform',
            name='templates',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=[]),
        ),
        migrations.RunSQL('ALTER TABLE delft3dworker_searchform ALTER COLUMN "templates" TYPE jsonb USING "templates"::text::jsonb;',
            reverse_sql='ALTER TABLE delft3dworker_searchform ALTER COLUMN "templates" TYPE text USING "templates"::text;'
        ),
        migrations.AlterField(
            model_name='template',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
        migrations.RunSQL('ALTER TABLE delft3dworker_template ALTER COLUMN "meta" TYPE jsonb USING "meta"::text::jsonb;',
            reverse_sql='ALTER TABLE delft3dworker_template ALTER COLUMN "meta" TYPE text USING "meta"::text;'
        ),
        migrations.AlterField(
            model_name='template',
            name='sections',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
        migrations.RunSQL('ALTER TABLE delft3dworker_template ALTER COLUMN "sections" TYPE jsonb USING "sections"::text::jsonb;',
            reverse_sql='ALTER TABLE delft3dworker_template ALTER COLUMN "sections" TYPE text USING "sections"::text;'
        ),
        migrations.AlterField(
            model_name='version_svn',
            name='versions',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=b'{}'),
        ),
        migrations.RunSQL('ALTER TABLE delft3dworker_version_svn ALTER COLUMN "versions" TYPE jsonb USING "versions"::text::jsonb;',
            reverse_sql='ALTER TABLE delft3dworker_version_svn ALTER COLUMN "versions" TYPE text USING "versions"::text;'
        ),
    ]