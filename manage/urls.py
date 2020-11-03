from django.urls import path
from . import views
from .views import line_chart, line_chart_json

app_name = 'manage'

urlpatterns = [
    path('', views.ManagerHome.as_view(), name='manager_home_page'),
    path('product/', views.ManagerCreateProduct.as_view(), name='create_product'),
    path('product/list/', views.ManagerListProduct.as_view(), name='product_list'),
    path('product/edit/<int:pk>/', views.ManagerEditProduct.as_view(), name='product_edit'),
    path('chart/', line_chart, name='line_chart'),
    path('chartJSON/', line_chart_json, name='line_chart_json'),
    path('report/', views.manager_report, name='manager_report'),
    path('new-category/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category-update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('list-of-category/', views.CategoryListView.as_view(), name='category_list'),
    path('order-list/', views.RecentOrderView.as_view(), name='list_order'),
    path('expsenses-list/', views.ExpensesListView.as_view(), name='list_expenses'),
    path('expense-add-file/', views.upload_expense_file, name='add_expense_from_file'),
    path('expenses-add-form/', views.AddExpenses.as_view(), name='add_expenses'),
    path('expenses-update-form/<int:pk>/', views.UpdateExpenses.as_view(), name='update_expenses'),
    path('expenses-delete-form/<int:pk>/', views.DeleteExpenses.as_view(), name='delete_expenses'),
    path('revenue-list/', views.RevenueListView.as_view(), name='list_revenue'),
    path('revenue-add-file/', views.upload_revenue_file, name='add_revenue_from_file'),
    path('revenue-add-form/', views.AddERevenue.as_view(), name='add_revenue'),
    path('revenue-update-form/<int:pk>/', views.UpdateRevenue.as_view(), name='update_revenue'),
    path('revenue-delete-form/<int:pk>/', views.DeleteRevenue.as_view(), name='delete_revenue'),
]
