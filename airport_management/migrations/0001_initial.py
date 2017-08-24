# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 00:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arrival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_code', models.CharField(max_length=10)),
                ('carrier', models.CharField(max_length=20)),
                ('origin_airport', models.CharField(max_length=3)),
                ('destined_airport', models.CharField(max_length=3)),
                ('departing_local_time', models.DateTimeField()),
                ('expected_landing_local_time', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Departure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_code', models.CharField(max_length=10)),
                ('carrier', models.CharField(max_length=20)),
                ('origin_airport', models.CharField(max_length=3)),
                ('destined_airport', models.CharField(max_length=3)),
                ('departing_local_time', models.DateTimeField()),
                ('expected_landing_local_time', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]