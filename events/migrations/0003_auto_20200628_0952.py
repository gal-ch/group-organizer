# Generated by Django 3.0.7 on 2020-06-28 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20200627_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='take_on_event',
            field=models.BooleanField(),
        ),
    ]
