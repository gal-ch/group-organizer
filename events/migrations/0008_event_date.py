# Generated by Django 3.0.7 on 2020-07-03 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20200703_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
    ]
