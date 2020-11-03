from django.db import models
from django.utils.translation import gettext_lazy as _

from auths.models import User
from shop.models import Product


class Order(models.Model):
    sold_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    mobile = models.PositiveIntegerField(max_length=10, blank=True, null=True)
    address = models.CharField(_('address'), max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    # def get_total_cost(self):
    #     total_cost = sum(item.get_cost() for item in self.items.all())
    #     return total_cost - total_cost * \
    #         (self.discount / Decimal(100))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
