# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-21 21:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('external_id', models.CharField(max_length=100)),
                ('source', models.CharField(choices=[('Spotify', 'Spotify'), ('Amazon', 'Amazon'), ('Google', 'Google')], max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('created_on',),
            },
        ),
    ]
