from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.views.generic import ListView, DetailView

from sales.forms import SalesSearchForm
from sales.models import Sale
import pandas as pd

from sales.utils import get_customer_from_id, get_salesman_from_id


def home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    form = SalesSearchForm(request.POST or None)

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        # print(date_from, date_to, chart_type)

        sale_qs = Sale.objects.filter(created__lte=date_to, created__gte=date_from)
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)
            positions_data = []

            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(),
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
        else:
            print("No data")

    context = {
        'form': form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
    }
    return render(request, 'sales/home.html', context)


class SalesListView(ListView):
    model = Sale
    template_name = 'sales/main.html'


def sales_list_view(request):
    qs = Sale.objects.all()
    return render(request, 'sales/main.html', {'object_list': qs})


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'


def sale_detail_view(request, pk):
    obj = Sale.objects.get(pk=pk)
    # or
    # obj = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/detail.html', {'object': obj})
