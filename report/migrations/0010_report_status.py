# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-02 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0009_reportvote_report_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]