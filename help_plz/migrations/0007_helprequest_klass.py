# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-14 13:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('help_plz', '0006_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='helprequest',
            name='klass',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='help_plz.Class'),
        ),
    ]
