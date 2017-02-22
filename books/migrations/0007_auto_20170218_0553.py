# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 05:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20170216_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='GutenbergID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='text',
            name='author',
            field=models.ManyToManyField(blank=True, null=True, to='books.Author'),
        ),
    ]
