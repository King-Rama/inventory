# Generated by Django 3.0.7 on 2020-11-03 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20201103_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='mobile',
            field=models.PositiveIntegerField(blank=True, max_length=10, null=True),
        ),
    ]