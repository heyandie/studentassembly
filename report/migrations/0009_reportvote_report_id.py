# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-28 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_remove_reportvote_report_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportvote',
            name='report_id',
            field=models.UUIDField(),
            preserve_default=False,
        ),
    ]
