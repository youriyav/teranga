# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('idNotification', models.AutoField(serialize=False, primary_key=True, db_column='idNotification')),
                ('Notitype', models.IntegerField(default=0, db_column='type')),
                ('is_read', models.IntegerField(default=0, db_column='is_read')),
                ('is_sync', models.IntegerField(default=0, db_column='is_sync')),
                ('dateCreation', models.DateTimeField(default=django.utils.timezone.now, db_column='dateCreation')),
                ('content', models.CharField(max_length=300, db_column='content')),
                ('titre', models.CharField(max_length=50, null=True, db_column='titre')),
                ('url', models.CharField(max_length=250, null=True, db_column='url')),
                ('client', models.ForeignKey(to='client.Client', db_column='client')),
            ],
            options={
                'db_table': 'notification',
            },
        ),
    ]
