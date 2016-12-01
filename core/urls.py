from django.conf.urls import url

from core.views import ProductView
from .views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^product/(?P<pk>[0-9]+)/$', ProductView.as_view(), name='product'),
]