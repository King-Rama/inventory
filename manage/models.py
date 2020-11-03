from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField
# Create your models here.
from auths.models import User

#
# class Category(models.Model):
#     name = models.CharField(max_length=200, db_index=True)
#     slug = models.SlugField(max_length=200, unique=True)
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(Category, self).save(*args, **kwargs)
#
#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'category'
#         verbose_name_plural = 'categories'
#
#     def __str__(self):
#         return self.name
#
#
# class WareHouse(models.Model):
#     WAREHOUSE_CHOICES = (
#         (1, 'rent'),
#         (2, 'owned')
#     )
#
#     warehouse_name = models.CharField(max_length=100, db_index=True)
#     slug = models.SlugField(max_length=100, unique=True)
#     district = models.CharField(max_length=100, blank=True, null=True)
#     country = CountryField()
#     lease_type = models.PositiveSmallIntegerField(choices=WAREHOUSE_CHOICES, default=2)
#     rent = models.DecimalField(max_length=9, decimal_places=2, max_digits=11)
#     created = models.DateTimeField(auto_now_add=True)
#     workers = models.ManyToManyField(User, related_name='workers')
#     full = models.BooleanField(default=False)
#     running_cost = models.DecimalField(max_length=9, decimal_places=2, max_digits=11)
#     location = models.CharField(max_length=500, blank=True, null=True)
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.warehouse_name)
#         super(WareHouse, self).save(*args, **kwargs)
#
#
# class Stock(models.Model):
#     STOCK_TYPE = (
#         (1, 'flammable'),
#         (2, 'non-flammable')
#     )
#
#     name = models.CharField(max_length=100, db_index=True)
#     slug = models.SlugField(max_length=100, unique=True)
#     serial_number = models.CharField(max_length=200, blank=True, null=True)
#     arrived = models.DateTimeField(auto_now_add=True)
#     expiry_date = models.DateTimeField()
#     vendor = models.CharField(max_length=200)
#     vendor_phone = models.CharField(max_length=20)
#     vendor_email = models.EmailField()
#     vendor_website = models.URLField()
#     description = models.TextField(blank=True, null=True)
#     warehouse = models.ForeignKey(WareHouse, on_delete=models.DO_NOTHING, related_name='warehouses')
#     stock_cost = models.DecimalField(max_length=9, decimal_places=2, max_digits=11)
#     transport_fee = models.DecimalField(max_length=9, decimal_places=2, max_digits=11)
#     type = models.PositiveSmallIntegerField(choices=STOCK_TYPE)
#     units = models.PositiveSmallIntegerField(blank=True, null=True)
#     created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_by')
#     updated_by = models.ManyToManyField(User, related_name='updated_by')
#     category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='stock_category')
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(Stock, self).save(*args, **kwargs)


class Salary(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salaries', null=True)
    income = models.DecimalField(max_length=9, decimal_places=2, max_digits=11, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)
    worker = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)


class Expenses(models.Model):
    is_file = models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True, null=True)
    particulars = models.CharField(max_length=500, blank=True, null=True)
    amount = models.DecimalField(max_length=9, decimal_places=2, max_digits=11)
    publisher = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='expenses_pub')
    date = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class Revenue(models.Model):
    category = models.CharField(max_length=100, blank=True, null=True)
    particulars = models.CharField(max_length=500, blank=True, null=True)
    amount = models.DecimalField(max_length=9, decimal_places=2, max_digits=11)
    date = models.DateField(blank=True, null=True)
    publisher = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='revenue_pub')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

