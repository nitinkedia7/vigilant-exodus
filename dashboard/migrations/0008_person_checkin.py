# Generated by Django 2.1.2 on 2018-10-26 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20181018_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='checkin',
            field=models.CharField(default='false', max_length=40),
        ),
    ]
