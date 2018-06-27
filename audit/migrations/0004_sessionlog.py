# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-26 09:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0003_auto_20180626_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_tag', models.CharField(max_length=128, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('bind_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audit.BindHost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]