from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .cart import Cart
from .forms import CreateOrder
from .models import Product, Cart as CartModel, ProductAudio, ProductPDF, ProductPaperback
from .utils import send_confirmation_email


class HomeView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all()
    context_object_name = 'products'


class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['audio'] = self.object.productaudio_set.first()
        context['pdf'] = self.object.productpdf_set.first()
        context['paperback'] = self.object.productpaperback_set.first()
        context['related_items'] = Product.objects.all()
        return context


class AddToCartView(CreateView):

    AUDIO = 'AUDIO'
    PDF = 'PDF'
    PAPERBACK = 'PAPERBACK'

    def post(self, request, *args, **kwargs):
        unit_price = request.POST.get('unit_price')
        quantity = request.POST.get('quantity')
        product_type = request.POST.get('type')
        product_id = request.POST.get('id')
        if product_type == self.AUDIO:
            product = ProductAudio.objects.get(id=product_id)
        elif product_type == self.PDF:
            product = ProductPDF.objects.get(id=product_id)
        else:
            product = ProductPaperback.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product, unit_price, quantity)
        return HttpResponseRedirect(reverse_lazy('cart'))


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
        send_confirmation_email()
        return HttpResponseRedirect(reverse_lazy('home'))


class ApplyDiscount(FormView):

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        cart.apply_discount(request.POST.get('discount'))
        return HttpResponseRedirect(reverse_lazy('cart'))


