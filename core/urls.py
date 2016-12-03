from django.conf.urls import url

from .views import HomeView, PublicationView, AddToCartView, CartView, PlaceOrderView, ApplyDiscount, OrderView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^publication/(?P<pk>[0-9]+)/$', PublicationView.as_view(), name='publication'),
    url(r'^add_to_cart/$', AddToCartView.as_view(), name='add_to_cart'),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^order/(?P<pk>[0-9]+)/$', OrderView.as_view(), name='view_order'),
    url(r'^order/$', PlaceOrderView.as_view(), name='order'),
    url(r'^discount/$', ApplyDiscount.as_view(), name='discount'),
]
