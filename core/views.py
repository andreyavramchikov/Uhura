from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView

from .cart import Cart
from .forms import CreateOrder
from .models import Product, Cart as CartModel


class HomeView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all()
    context_object_name = 'products'


class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'


class AddToCartView(CreateView):

    def post(self, request, *args, **kwargs):
        unit_price = request.POST.get('unit_price')
        quantity = request.POST.get('quantity')
        cart = Cart(request)
        cart.add(Product.objects.get(id=request.POST.get('id')), unit_price, quantity)
        return HttpResponseRedirect('/')


class CartView(TemplateView):
    template_name = 'cart.html'
    queryset = CartModel.objects.all()
    context_object_name = 'items'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['cart'] = Cart(request)
        return self.render_to_response(context)


class PlaceOrderView(CreateView):
    form_class = CreateOrder

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/')


