# Generated by Django 2.1.5 on 2020-02-08 17:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dice', '0014_diceimage_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diceimage',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
