# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 09:45
from __future__ import unicode_literals

from django.db import migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='answers',
            field=django_pgjson.fields.JsonBField(null=True),
        ),
    ]