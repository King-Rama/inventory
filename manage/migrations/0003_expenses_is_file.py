# Generated by Django 3.0.7 on 2020-10-31 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0002_auto_20201031_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='is_file',
            field=models.BooleanField(default=False),
        ),
    ]
