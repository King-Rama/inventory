# Generated by Django 3.0.7 on 2020-11-03 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0006_expenses_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revenue',
            name='name',
        ),
        migrations.RemoveField(
            model_name='revenue',
            name='quantity',
        ),
        migrations.AddField(
            model_name='revenue',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]