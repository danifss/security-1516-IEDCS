# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('contentId', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('deviceID', models.AutoField(serialize=False, primary_key=True)),
                ('deviceKey', models.CharField(max_length=1024)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('playerID', models.AutoField(serialize=False, primary_key=True)),
                ('playerKey', models.CharField(max_length=1024)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purchaseID', models.AutoField(serialize=False, primary_key=True)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('contentID', models.ForeignKey(to='core.Content')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.AutoField(serialize=False, primary_key=True)),
                ('userKey', models.CharField(max_length=1024)),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(unique=True, max_length=150)),
                ('password', models.CharField(max_length=100)),
                ('firstName', models.CharField(max_length=100, null=True)),
                ('lastName', models.CharField(max_length=100, null=True)),
                ('fileKey', models.CharField(max_length=1024, blank=True)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('playerID', models.ForeignKey(to='core.Player')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='players',
            field=models.ManyToManyField(to='core.Player'),
        ),
    ]
