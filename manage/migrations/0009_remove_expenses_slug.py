# Generated by Django 3.0.7 on 2020-11-03 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0008_remove_revenue_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expenses',
            name='slug',
        ),
    ]