# Generated by Django 3.0.7 on 2020-06-20 22:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0005_auto_20200620_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='charge_users',
            field=models.ManyToManyField(related_name='charge_users', to=settings.AUTH_USER_MODEL),
        ),
    ]