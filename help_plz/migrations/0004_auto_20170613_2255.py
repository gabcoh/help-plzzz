# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 22:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help_plz', '0003_auto_20170613_2251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='helprequest',
            options={'permissions': (('can_concur', 'Can concur with help requests'), ('can_mark_started', 'Can mark help request as begun'), ('can_mark_done', 'Can mark help request as done'), ('can_view_private', 'Can view private requests'))},
        ),
    ]