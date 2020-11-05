from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from auths.decorators import pos_required
from manage.models import Revenue, Expenses, Salary
from orders.models import OrderItem
from shop.models import Product, Category
from cart.forms import CartAddProductForm

# Create your views here.


class LineChartJSONView(BaseLineChartView):

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
        return ["Expenses"]

    def get_data(self):
        """Return 3 datasets to plot."""
        sales = [x.get_cost() for x in OrderItem.objects.all()]
        revenue = [x.amount for x in Revenue.objects.all()]
        expenses = [x.amount for x in Expenses.objects.all()]
        # if sales is None or sales < [range(7)]:
        #     sales = [range(len(sales) - len(range(7)))]

        return [expenses]


line_chart = TemplateView.as_view(template_name='index.html')
line_chart_json = LineChartJSONView.as_view()


@method_decorator([login_required, pos_required], name='dispatch')
class Home(generic.TemplateView):
    template_name = 'pos/products.html'


@login_required
@pos_required
def search_product_view(request):
    # query = request.GET.get('query')
    # data = {
    #     'query': [Product.objects.filter(name__icontains=query)]
    # }
    # return JsonResponse(data)

    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        artists = Product.objects.filter(name__icontains=str(url_parameter))
    else:
        artists = Product.objects.all()

    ctx["products"] = artists
    ctx['form'] = CartAddProductForm(request.POST)
    if request.is_ajax():
        html = render_to_string(
            template_name="pos/product_result.html", context={"products": artists, "form": CartAddProductForm(request.POST)}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "pos/products.html", context=ctx)


@login_required
@pos_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'pos/detail.html', {'product': product, 'cart_product_form': cart_product_form})


class RecentOrdersView(generic.ListView):
    model = OrderItem
    template_name = 'pos/data/recent/list.html'

    def get_queryset(self):
        return OrderItem.objects.filter(order__sold_by__username=self.request.user.username)

