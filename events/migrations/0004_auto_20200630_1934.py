# Generated by Django 3.0.7 on 2020-06-30 19:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0003_auto_20200628_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='charge_users',
            field=models.ManyToManyField(related_name='in_charge_of', to=settings.AUTH_USER_MODEL),
        ),
    ]
