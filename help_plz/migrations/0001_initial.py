# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 20:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpRequest',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=50)),
                ('urgency', models.CharField(blank=True, choices=[
                 ('HIGH', 'H'), ('MEDIUM', 'M'), ('LOW', 'L')], max_length=1)),
                ('pub_datetime', models.DateTimeField(
                    auto_now=True, verbose_name='request time')),
                ('public', models.BooleanField(default=True)),
                ('started', models.BooleanField(default=False)),
                ('request_teacher', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(
                    default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('can_add', 'Can create new help request'), ('can_concur', 'Can concur with a help request'), ('can_delete', 'Can delete a help request'), ('can_mark_started', 'Can mark help request as begun'), ('can_mark_done', 'Can mark help request as done'), ('can_view_private', 'Can view private request')),
            },
        ),
    ]
