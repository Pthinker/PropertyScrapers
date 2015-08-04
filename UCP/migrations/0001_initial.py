# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnclaimedProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('property_id', models.BigIntegerField(unique=True)),
                ('date_added_to_site', models.CharField(max_length=20)),
                ('source', models.CharField(max_length=20)),
                ('owners_name', models.TextField()),
                ('owners_address', models.TextField()),
                ('type_of_property', models.CharField(max_length=2000)),
                ('cash_reported_text', models.CharField(max_length=100)),
                ('cash_reported', models.DecimalField(max_digits=10, decimal_places=2)),
                ('reported_by', models.CharField(max_length=2000)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
