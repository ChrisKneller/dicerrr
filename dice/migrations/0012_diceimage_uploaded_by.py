# Generated by Django 2.1.5 on 2020-02-08 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dice', '0011_remove_diceimage_uploaded_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='diceimage',
            name='uploaded_by',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
