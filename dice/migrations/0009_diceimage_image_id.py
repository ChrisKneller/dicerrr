# Generated by Django 2.1.5 on 2019-03-29 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dice', '0008_constructioncost'),
    ]

    operations = [
        migrations.AddField(
            model_name='diceimage',
            name='image_id',
            field=models.TextField(default=12345678),
            preserve_default=False,
        ),
    ]
