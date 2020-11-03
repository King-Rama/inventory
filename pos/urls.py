from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import line_chart, line_chart_json

app_name = 'pos'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('products/', views.search_product_view, name='search_product'),
    path('detail/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
    path('recent/sales/', views.RecentOrdersView.as_view(), name='recent-sales')
]
