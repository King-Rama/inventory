from django.contrib import admin

# Register your models here.
from manage.models import Salary, Expenses, Revenue

admin.site.register(Salary)

admin.site.register(Expenses)
admin.site.register(Revenue)
