# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-29 11:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('XMZ', '0004_xmz_urtracker_title'),
    ]

    operations = [
        migrations.DeleteModel(
            name='XMZ_SVNLog',
        ),
        migrations.DeleteModel(
            name='XMZ_URTracker',
        ),
    ]
