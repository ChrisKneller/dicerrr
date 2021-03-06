# Generated by Django 2.1.5 on 2019-02-17 17:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dice', '0003_auto_20190214_0643'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiceImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.TextField(validators=[django.core.validators.URLValidator()])),
                ('new_image', models.TextField(validators=[django.core.validators.URLValidator()])),
                ('image_width', models.IntegerField()),
                ('image_height', models.IntegerField()),
                ('number_of_dice', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='OriginalPic',
        ),
    ]
