# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_gutenbergid'),
    ]

    operations = [
        migrations.AddField(
            model_name='gutenbergid',
            name='html_file',
            field=models.FileField(default='file_field_default', upload_to=''),
            preserve_default=False,
        ),
    ]
