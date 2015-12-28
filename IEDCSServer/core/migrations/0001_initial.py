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
                ('contentID', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('fileName', models.CharField(max_length=150)),
                ('filepath', models.CharField(max_length=400)),
                ('pages', models.IntegerField(default=0)),
                ('restriction', models.CharField(default=b'World', max_length=150)),
                ('description', models.CharField(default=b'Place description here', max_length=250, blank=True)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('deviceID', models.AutoField(serialize=False, primary_key=True)),
                ('deviceKey', models.CharField(max_length=2048)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('deviceHash', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('playerID', models.AutoField(serialize=False, primary_key=True)),
                ('playerKey', models.CharField(max_length=2048)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('playerIV', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purchaseID', models.AutoField(serialize=False, primary_key=True)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('content', models.ForeignKey(to='core.Content')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.AutoField(serialize=False, primary_key=True)),
                ('userCC', models.CharField(unique=True, max_length=8)),
                ('userKey', models.CharField(max_length=2048)),
                ('username', models.CharField(unique=True, max_length=100)),
                ('userIV', models.CharField(max_length=32, blank=True)),
                ('userSalt', models.CharField(max_length=64, blank=True)),
                ('email', models.CharField(unique=True, max_length=150)),
                ('password', models.CharField(max_length=100)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('magicKey', models.CharField(max_length=2048, blank=True)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='user',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.ForeignKey(to='core.User'),
        ),
        migrations.AddField(
            model_name='device',
            name='player',
            field=models.ForeignKey(to='core.Player'),
        ),
    ]
