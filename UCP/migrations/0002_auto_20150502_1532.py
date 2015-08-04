# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('UCP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NTypeUnclaimedProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('property_id', models.BigIntegerField(unique=True, verbose_name=b'Property Id')),
                ('notification_date', models.CharField(max_length=20, verbose_name=b'Notification Date')),
                ('date_reported', models.CharField(max_length=20, verbose_name=b'Date Reported')),
                ('date_last_contact', models.CharField(max_length=20, verbose_name=b'Date of Last Contact')),
                ('owners_name', models.TextField(verbose_name=b'Owner(s) Name')),
                ('owners_address', models.TextField(verbose_name=b'Reported Owner Address')),
                ('business_contact_information', models.TextField(verbose_name=b'Business Contact Information')),
                ('type_of_property', models.CharField(max_length=2000, verbose_name=b'Type of Property')),
                ('cash_reported', models.CharField(max_length=100, verbose_name=b'Cash Reported')),
                ('shares_reported', models.CharField(max_length=100, verbose_name=b'Shares Reported')),
                ('name_security_reported', models.CharField(max_length=500, verbose_name=b'Name of Security Reported')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Unclaimed Property N Type',
                'verbose_name_plural': 'Unclaimed Properties N Type',
            },
        ),
        migrations.AlterModelOptions(
            name='unclaimedproperty',
            options={'verbose_name': 'Unclaimed Property P Type', 'verbose_name_plural': 'Unclaimed Properties P Type'},
        ),
        migrations.AlterField(
            model_name='unclaimedproperty',
            name='cash_reported',
            field=models.DecimalField(verbose_name=b'Cash Reported', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='unclaimedproperty',
            name='cash_reported_text',
            field=models.CharField(max_length=100, verbose_name=b'Cash Reported (Text)'),
        ),
        migrations.AlterField(
            model_name='unclaimedproperty',
            name='date_added_to_site',
            field=models.CharField(max_length=20, verbose_name=b'Date'),
        ),
        migrations.AlterField(
            model_name='unclaimedproperty',
            name='owners_address',
            field=models.TextField(verbose_name=b'Reported Owner Address'),
        ),
        migrations.AlterField(
            model_name='unclaimedproperty',
            name='owners_name',
            field=models.TextField(verbose_name=b'Owner(s) Name'),
        ),
        migrations.AlterField(
            model_name='unclaimedproperty',
            name='property_id',
            field=models.BigIntegerField(unique=True, verbose_name=b'Property Id'),
        ),
        migrations.AlterField(
            model_name='unclaimedproperty',
            name='reported_by',
            field=models.CharField(max_length=2000, verbose_name=b'Reported By'),
        ),
        migrations.AlterField(
            model_name='unclaimedproperty',
            name='source',
            field=models.CharField(max_length=20, verbose_name=b'Source'),
        ),
        migrations.AlterField(
            model_name='unclaimedproperty',
            name='type_of_property',
            field=models.CharField(max_length=2000, verbose_name=b'Type of Property'),
        ),
    ]
