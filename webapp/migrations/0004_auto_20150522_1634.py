# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20150520_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='id',
        ),
        migrations.AddField(
            model_name='usuario',
            name='fondo',
            field=models.CharField(default=123, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='letra',
            field=models.CharField(default=123, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=200, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
