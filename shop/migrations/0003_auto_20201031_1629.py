# Generated by Django 3.0.7 on 2020-10-31 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20201031_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, max_length=9),
        ),
        migrations.AlterField(
            model_name='product',
            name='transport_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, max_length=9),
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor_phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor_website',
            field=models.URLField(blank=True),
        ),
    ]