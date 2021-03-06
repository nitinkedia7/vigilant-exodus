# Generated by Django 2.1.2 on 2018-10-15 08:22

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('capacity', models.IntegerField(default=1000)),
                ('food', models.IntegerField(default=1000)),
                ('water', models.IntegerField(default=1000)),
                ('medicine', models.IntegerField(default=1000)),
                ('point', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Relief Camps',
            },
        ),
        migrations.CreateModel(
            name='Disaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='camp',
            name='disaster',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.Disaster'),
        ),
    ]
