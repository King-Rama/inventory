import weasyprint
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from cart.cart import Cart
from shop.models import Product
from .models import OrderItem, Order
from .forms import OrderCreateForm
from django.views import generic


def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm(request.POST)
    if form.is_valid():
        order = form.save(commit=False)
        order.sold_by = request.user
        order.save()
        for item in cart:
            order_item = OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'],
                                     )
            order_item.save()
            prod = Product.objects.get(order_items=order_item)
            prod.quantity = prod.quantity - item['quantity']
            prod.save()
        # clear the cart
        #request.session['order_id'] = order.id
        # redirect for payment
        return redirect(reverse('orders:order-mwisho', kwargs={'pk': order.id}))
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


#@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': str(order)})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response


class OrderDetailView(generic.DetailView):
    model = Order
    context_object_name = 'order_detail'
    template_name = 'orders/detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['order'] = Order.objects.get(id=self.object.id)
        context['order_item'] = OrderItem.objects.filter(order=context['order'])
        context['prod'] = Product.objects.filter(order_items__order__first_name=context['order'].first_name)
        return context
