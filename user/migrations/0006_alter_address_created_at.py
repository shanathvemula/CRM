# Generated by Django 5.0.3 on 2024-04-05 09:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_address_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 5, 14, 44, 2, 201248)),
        ),
    ]
