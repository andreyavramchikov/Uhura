from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from core.models import Product


class HomeView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all()
    context_object_name = 'products'


class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

