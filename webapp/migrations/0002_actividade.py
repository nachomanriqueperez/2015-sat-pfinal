# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('precio', models.CharField(max_length=200)),
                ('fecha', models.CharField(max_length=200)),
                ('hora_inicio', models.CharField(max_length=200)),
                ('tipo', models.CharField(max_length=200)),
                ('duracion', models.CharField(max_length=200)),
                ('es_larga', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
