# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 06:20
from __future__ import unicode_literals

from django.db import migrations, models
import django_pgjson.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('category_type', models.IntegerField()),
                ('questions', django_pgjson.fields.JsonBField(null=True)),
            ],
        ),
    ]
