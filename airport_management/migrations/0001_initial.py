# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-25 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirTrafficController',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ArrivalFlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_code', models.CharField(max_length=10)),
                ('airport', models.CharField(max_length=3)),
                ('day', models.CharField(max_length=9)),
                ('scheduled_datetime', models.DateTimeField()),
                ('carrier', models.CharField(max_length=20, null=True)),
                ('status', models.NullBooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DepartureFlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_code', models.CharField(max_length=10)),
                ('airport', models.CharField(max_length=3)),
                ('day', models.CharField(max_length=9)),
                ('scheduled_datetime', models.DateTimeField()),
                ('carrier', models.CharField(max_length=20, null=True)),
                ('status', models.NullBooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=7)),
            ],
        ),
        migrations.AddField(
            model_name='departureflight',
            name='lane',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departureflight_lane', to='airport_management.Lane'),
        ),
        migrations.AddField(
            model_name='departureflight',
            name='online_atcs',
            field=models.ManyToManyField(related_name='departureflight_online_atc', to='airport_management.AirTrafficController'),
        ),
        migrations.AddField(
            model_name='arrivalflight',
            name='lane',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrivalflight_lane', to='airport_management.Lane'),
        ),
        migrations.AddField(
            model_name='arrivalflight',
            name='online_atcs',
            field=models.ManyToManyField(related_name='arrivalflight_online_atc', to='airport_management.AirTrafficController'),
        ),
    ]
