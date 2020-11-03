from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from auths.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    sold_by = models.ForeignKey(User, related_name='saler', on_delete=models.DO_NOTHING, null=True, blank=True)  # for keeping record of who sold the goods
    stock_updated_by = models.ManyToManyField(User, blank=True, related_name='updater')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.DO_NOTHING)
    initial_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/%S', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True, help_text='Checked means the stock is ready for sales')  # set True to allow goods to be visible in product for sales
    created = models.DateTimeField(auto_now_add=True)  # stock created
    quantity = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    expiry_date = models.DurationField(blank=True, null=True)
    serial_number = models.CharField(max_length=200, blank=True, null=True)
    vendor = models.CharField(max_length=200, blank=True)
    vendor_phone = models.CharField(max_length=20, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    vendor_email = models.EmailField(blank=True)
    vendor_website = models.URLField(blank=True)
    stock_cost = models.DecimalField(max_length=9, decimal_places=2, max_digits=11, blank=True)
    transport_fee = models.DecimalField(max_length=9, decimal_places=2, max_digits=11, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #      return reverse('pos:product_detail',args=[self.id, self.slug])
