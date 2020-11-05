from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q, Sum
from django.shortcuts import render, redirect
import pandas as pd
# Create your views here.
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import generic
from xlrd import XLRDError

from auths.decorators import manager_required
from orders.models import Order, OrderItem
from .forms import ProductForm, ExpensesFormAdd, RevenueForm
from shop.models import Product, Category
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from .forms import ExpensesForm, RevenueFormAdd
from .models import Expenses, Revenue, Salary


@method_decorator([login_required, manager_required], name='dispatch')
class LineChartJSONView(BaseLineChartView):
    # last_month = datetime.now() - timedelta(days=30)
    # data_1 = Expenses.objects.filter(created__gt=last_month).extra(select={'day': 'date(created)'}).values(
    #     'day').annotate(sum=Sum('amount'))
    # data_2 = Revenue.objects.filter(created__gt=last_month).extra(select={'day': 'date(created)'}).values(
    #     'day').annotate(sum=Sum('amount'))

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        revenue = Revenue.objects.all()
        # if revenue < [range(7)] or revenue is None:
        #     revenue = [range(len(revenue) - len(range(7)))]
        days = []
        for sale in revenue[:7]:
            days.append(sale.created.day)
        return [days]

    def get_providers(self):
        """Return names of datasets."""
        return ["Sales"]

    def get_data(self):
        """Return 3 datasets to plot."""
        sales = OrderItem.objects.all()
        revenue = [x.amount for x in Revenue.objects.all()]
        expenses = [x.amount for x in Expenses.objects.all()]
        # if sales is None or sales < [range(7)]:
        #     sales = [range(len(sales) - len(range(7)))]

        return [sales[:7]]


line_chart = TemplateView.as_view(template_name='manage/index.html')
line_chart_json = LineChartJSONView.as_view()


@method_decorator([login_required, manager_required], name='dispatch')
class ManagerHome(generic.TemplateView):
    template_name = 'manage/index.html'

    def get_context_data(self, **kwargs):
        context = super(ManagerHome, self).get_context_data(**kwargs)
        revenue = Revenue.objects.all().aggregate(Sum('amount'))
        expenses = Expenses.objects.all().aggregate(Sum('amount'))
        gross_revenue = OrderItem.objects.all()
        gross_expenses = Salary.objects.all().aggregate(Sum('income'))
        if gross_expenses['income__sum'] is None:
            gross_expenses['income__sum'] = 0
        if gross_revenue is None:
            gross_revenue = 0
        if revenue['amount__sum'] is None:
            revenue['amount__sum'] = 0
        if expenses['amount__sum'] is None:
            expenses['amount__sum'] = 0
        money = 0
        for expense in gross_revenue:
            money = money + (expense.price * expense.quantity)
        context['gross_money'] = money + revenue['amount__sum']
        context['expenses'] = expenses['amount__sum'] + gross_expenses['income__sum']
        context['net_profit'] = context['gross_money'] - context['expenses']
        context['profit'] = 'Profit'
        if context['net_profit'] < 0:
            context['profit'] = 'Loss'
        context['sales'] = money
        return context


@method_decorator([login_required, manager_required], name='dispatch')
class ManagerCreateProduct(generic.CreateView):
    template_name = 'manage/product/add/form.html'
    form_class = ProductForm
    success_url = reverse_lazy('manage:product_list')
    model = Product

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.stock_filled_by = self.request.user
        self.object.save()
        return super().form_valid(form)


@method_decorator([login_required, manager_required], name='dispatch')
class ManagerListProduct(generic.ListView):
    template_name = 'manage/product/list.html'
    context_object_name = 'products'
    model = Product


@method_decorator([login_required, manager_required], name='dispatch')
class ManagerEditProduct(generic.UpdateView):
    model = Product
    template_name = 'manage/product/add/form.html'
    form_class = ProductForm
    success_url = reverse_lazy('manage:product_list')


@login_required
@manager_required
def auto_create_category(request):
    # to create category if none satisfy
    if request.is_ajax():
        pass

    return render(request, 'manage/index.html', {})


@method_decorator([login_required, manager_required], name='dispatch')
class CategoryCreateView(generic.CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('manage:category_list')
    context_object_name = 'cat_form'
    template_name = 'manage/product/category/form.html'


@method_decorator([login_required, manager_required], name='dispatch')
class CategoryUpdateView(generic.UpdateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('manage:category_list')
    context_object_name = 'cat_form'
    template_name = 'manage/product/category/form.html'


@method_decorator([login_required, manager_required], name='dispatch')
class CategoryListView(generic.ListView):
    model = Category
    template_name = 'manage/product/category/list.html'


@method_decorator([login_required, manager_required], name='dispatch')
class RecentOrderView(generic.ListView):
    model = OrderItem
    template_name = 'manage/product/recent/list.html'


@login_required
@manager_required
def create_category_and_product(request):
    pass


@method_decorator([login_required, manager_required], name='dispatch')
class ReportCreateView(generic.CreateView):
    template_name = 'manage/'


@login_required
@manager_required
def manager_report(request):
    order = Order.objects.all()
    order_detail = OrderItem.objects.all()

    return render(request, 'manage/product/tables/table.html', {'order': order, 'order_detail': order_detail})


@method_decorator([login_required, manager_required], name='dispatch')
class ExpensesListView(generic.ListView):
    model = Expenses
    template_name = 'manage/product/expenses/list.html'


def upload_expense_file(request):
    form = ExpensesForm(request.POST, request.FILES)
    count = 0

    if form.is_valid():
        try:
            uploaded_file = pd.read_excel(request.FILES['file']).fillna(value='-')

            # below we gonna load the file inputs

            for row in range(len(uploaded_file)):
                holder_list = []
                for col in range(len(uploaded_file.iloc[row])):
                    holder_list.append(uploaded_file.iloc[row][col])

                expe = Expenses(category=str(holder_list[1]),
                                particulars=str(holder_list[2]),
                                amount=int(holder_list[3]),
                                date=holder_list[4],
                                publisher=request.user,
                                is_file=True)
                expe.save()

        except XLRDError as erro1:
            messages.add_message(request, messages.ERROR, 'Unrecognized document, please upload an excel file')
            redirect('manage:list_expenses')

        except IntegrityError as error:
            messages.add_message(request, messages.ERROR, 'Document already added!')
            redirect('manage:list_expenses')

        messages.add_message(request, messages.ERROR, 'Unrecognized document, please upload an excel file')
        redirect('manage:list_expenses')

    return render(request, 'manage/product/expenses/add_file.html', {'form': form})


class AddExpenses(generic.CreateView):
    model = Expenses
    template_name = 'manage/product/expenses/form.html'
    form_class = ExpensesFormAdd
    success_url = reverse_lazy('manage:list_expenses')
    context_object_name = 'cat_form'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.publisher = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateExpenses(generic.UpdateView):
    model = Expenses
    template_name = 'manage/product/expenses/form.html'
    form_class = ExpensesFormAdd
    success_url = reverse_lazy('manage:list_expenses')
    context_object_name = 'cat_form'


class DeleteExpenses(generic.DeleteView):
    model = Expenses
    template_name = 'manage/product/expenses/confirm.html'
    context_object_name = 'expe-delete'
    success_url = reverse_lazy('manage:list_expenses')

    def form_valid(self):
        messages.add_message(self.request, messages.INFO, 'Item removed successfully')
        return super(DeleteExpenses)


@method_decorator([login_required, manager_required], name='dispatch')
class RevenueListView(generic.ListView):
    model = Revenue
    template_name = 'manage/product/revenue/list.html'
    context_object_name = 'revenus'


def upload_revenue_file(request):
    form = RevenueForm(request.POST, request.FILES)
    count = 0

    if form.is_valid():
        try:
            uploaded_file = pd.read_excel(request.FILES['file']).fillna(value='-')

            # below we gonna load the file inputs

            for row in range(len(uploaded_file)):
                holder_list = []
                for col in range(len(uploaded_file.iloc[row])):
                    holder_list.append(uploaded_file.iloc[row][col])

                expe = Revenue(category=str(holder_list[1]),
                               particulars=str(holder_list[2]),
                               amount=int(holder_list[3]),
                               date=holder_list[4],
                               publisher=request.user,
                            )
                expe.save()

        except XLRDError as erro1:
            messages.add_message(request, messages.ERROR, 'Unrecognized document, please upload an excel file')
            redirect('manage:list_revenue')

        except IntegrityError as error:
            messages.add_message(request, messages.ERROR, 'Document already added!')
            redirect('manage:list_revenue')

        messages.add_message(request, messages.ERROR, 'Unrecognized document, please upload an excel file')
        redirect('manage:list_revenue')

    return render(request, 'manage/product/revenue/add_file.html', {'form': form})


class AddERevenue(generic.CreateView):
    model = Revenue
    template_name = 'manage/product/revenue/form.html'
    form_class = RevenueFormAdd
    success_url = reverse_lazy('manage:list_revenue')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.publisher = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateRevenue(generic.UpdateView):
    model = Expenses
    template_name = 'manage/product/revenue/form.html'
    form_class = ExpensesFormAdd
    success_url = reverse_lazy('manage:list_revenue')
    context_object_name = 'cat_form'


class DeleteRevenue(generic.DeleteView):
    model = Expenses
    template_name = 'manage/product/revenue/confirm.html'
    context_object_name = 'expe-delete'
    success_url = reverse_lazy('manage:list_revenue')

    def form_valid(self):
        messages.add_message(self.request, messages.INFO, 'Item removed successfully')
        return super(DeleteExpenses)
