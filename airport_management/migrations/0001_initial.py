# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 23:13
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
                ('code', models.CharField(max_length=10)),
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
                ('sch_local_datetime', models.DateTimeField()),
                ('carrier', models.CharField(max_length=20, null=True)),
                ('proper_atc', models.NullBooleanField()),
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
                ('sch_local_datetime', models.DateTimeField()),
                ('carrier', models.CharField(max_length=20, null=True)),
                ('proper_atc', models.NullBooleanField()),
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
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departureflight_lane', to='airport_management.Lane'),
        ),
        migrations.AddField(
            model_name='departureflight',
            name='online_atc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departureflight_online_atc', to='airport_management.AirTrafficController'),
        ),
        migrations.AddField(
            model_name='departureflight',
            name='past_atcs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departureflight_past_atcs', to='airport_management.AirTrafficController'),
        ),
        migrations.AddField(
            model_name='arrivalflight',
            name='lane',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrivalflight_lane', to='airport_management.Lane'),
        ),
        migrations.AddField(
            model_name='arrivalflight',
            name='online_atc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrivalflight_online_atc', to='airport_management.AirTrafficController'),
        ),
        migrations.AddField(
            model_name='arrivalflight',
            name='past_atcs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrivalflight_past_atcs', to='airport_management.AirTrafficController'),
        ),
        migrations.AddField(
            model_name='airtrafficcontroller',
            name='past_flights_arrival',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='airport_management.ArrivalFlight'),
        ),
        migrations.AddField(
            model_name='airtrafficcontroller',
            name='past_flights_departure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='airport_management.DepartureFlight'),
        ),
    ]
