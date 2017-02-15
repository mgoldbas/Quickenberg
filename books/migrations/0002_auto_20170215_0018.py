# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 00:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_squashed_0006_auto_20170206_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_broken_up', models.BooleanField(default=False)),
                ('regex', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='bookfile',
            name='book_title',
        ),
        migrations.AlterField(
            model_name='bookchapter',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.BookFile'),
        ),
        migrations.AlterField(
            model_name='bookchapter',
            name='chapter',
            field=models.CharField(max_length=200),
        ),
    ]
