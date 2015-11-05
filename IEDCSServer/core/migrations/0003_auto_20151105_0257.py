# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151105_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='firstName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastName',
            field=models.CharField(max_length=100),
        ),
    ]
