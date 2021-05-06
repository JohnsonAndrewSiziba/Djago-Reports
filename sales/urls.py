from django.urls import path

from sales.views import (
    SalesListView,
    SaleDetailView,
    home_view
)

app_name = 'sales'

urlpatterns = [
    path('', home_view, name='home'),
    path('sales/', SalesListView.as_view(), name='list'),
    path('sales/<pk>/', SaleDetailView.as_view(), name='detail'),
]
