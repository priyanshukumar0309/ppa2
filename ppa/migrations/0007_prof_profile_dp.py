# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-06 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppa', '0006_student_profile_dp'),
    ]

    operations = [
        migrations.AddField(
            model_name='prof',
            name='profile_dp',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
