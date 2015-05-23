# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_actividade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='password',
        ),
        migrations.AddField(
            model_name='usuario',
            name='actividad',
            field=models.ManyToManyField(to='webapp.Actividade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usuario',
            name='evento',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
