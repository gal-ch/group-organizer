# Generated by Django 3.0.7 on 2020-07-03 16:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0004_auto_20200630_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='charge_users',
            field=models.ManyToManyField(blank=True, related_name='in_charge_of', to=settings.AUTH_USER_MODEL),
        ),
    ]