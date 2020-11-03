from bootstrap_datepicker_plus import DatePickerInput
from django import forms

from manage.models import Expenses, Revenue
from shop.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'description', 'price', 'available', 'quantity']


class ExpensesForm(forms.Form):
    file = forms.FileField(help_text='Upload expense files...')


class RevenueForm(forms.Form):
    file = forms.FileField(help_text='Upload revenue files...')


class ExpensesFormAdd(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Expenses
        fields = ['category', 'particulars', 'amount', 'date']


class RevenueFormAdd(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Revenue
        fields = ['category', 'particulars', 'amount', 'date']
