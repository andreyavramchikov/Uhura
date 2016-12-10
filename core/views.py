import logging

from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView


from .cart import Cart
from .forms import CreateOrder, DiscountForm
from .models import Cart as CartModel, Publication, PublicationEntity
from .utils import send_confirmation_email


logger = logging.getLogger(__name__)


class HomeView(ListView):
    template_name = 'index.html'
    queryset = Publication.objects.all()
    context_object_name = 'publications'


class PublicationView(DetailView):
    model = Publication
    template_name = 'publication.html'
    context_object_name = 'publication'

    def get_context_data(self, **kwargs):
        context = super(PublicationView, self).get_context_data(**kwargs)
        context['publications'] = self.object.publicationentity_set.all()
        context['related_items'] = Publication.objects.all()
        return context


class AddToCartView(CreateView):

    def post(self, request, *args, **kwargs):
        unit_price = request.POST.get('unit_price')
        quantity = request.POST.get('quantity')
        product = PublicationEntity.objects.get(id=request.POST.get('id'))
        cart = Cart(request)
        cart.add(product, unit_price, quantity)
        return HttpResponseRedirect(reverse_lazy('cart'))


class CartView(FormView):
    template_name = 'cart.html'
    form_class = DiscountForm
    queryset = CartModel.objects.all()
    context_object_name = 'items'

    def get(self, request, *args, **kwargs):
        logger.info('Test Info')
        context = self.get_context_data(**kwargs)
        context['cart'] = Cart(request)
        return self.render_to_response(context)


class PlaceOrderView(CreateView):
    form_class = CreateOrder

    def form_valid(self, form):
        form.save()
        send_confirmation_email()
        cart = Cart(self.request)
        cart.clear(self.request)
        return HttpResponseRedirect(reverse_lazy('view_order', args=[cart.cart.pk]))


class OrderView(DetailView):
    model = CartModel
    template_name = 'order.html'
    context_object_name = 'cart'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['order'] = self.get_object()
        return context


class ApplyDiscount(FormView):
    """ It will be a good idea to make this view ajax"""
    form_class = DiscountForm

    def form_valid(self, form):
        request = self.request
        cart = Cart(request)
        discount = form.cleaned_data['discount']
        cart.apply_discount(form.cleaned_data['discount'])
        return JsonResponse({'success': 'Coupon for ${} has been applied'.format(discount),
                             'total': cart.summary()})

    def form_invalid(self, form):
        return JsonResponse({'error': 'Coupon is not correct'})


