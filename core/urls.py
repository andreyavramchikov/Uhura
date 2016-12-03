from django.conf.urls import url

from .views import HomeView, ProductView, AddToCartView, CartView, PlaceOrderView, ApplyDiscount

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^product/(?P<pk>[0-9]+)/$', ProductView.as_view(), name='product'),
    url(r'^add_to_cart/$', AddToCartView.as_view(), name='add_to_cart'),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^order/$', PlaceOrderView.as_view(), name='order'),
    url(r'^discount/$', ApplyDiscount.as_view(), name='discount'),
]