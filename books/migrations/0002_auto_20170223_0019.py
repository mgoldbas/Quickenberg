# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 00:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gutenberg',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gutenberg',
            name='html_number',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='books.GutenbergID'),
        ),
    ]
