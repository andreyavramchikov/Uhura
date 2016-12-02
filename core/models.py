from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.models import ContentType


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class ProductAudio(models.Model):
    product = models.ForeignKey(Product)
    url = models.CharField(max_length=235)
    price = models.IntegerField(null=True)

    def __unicode__(self):
        return '{}_audio'.format(self.product.name)


class ProductPDF(models.Model):
    product = models.ForeignKey(Product)
    url = models.CharField(max_length=235)
    price = models.IntegerField(null=True)

    def __unicode__(self):
        return '{}_pdf'.format(self.product.name)


class ProductPaperback(models.Model):
    product = models.ForeignKey(Product)
    url = models.CharField(max_length=235)
    price = models.IntegerField(null=True)

    def __unicode__(self):
        return '{}_paperback'.format(self.product.name)


class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    discount = models.PositiveIntegerField(default=10)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del (kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', verbose_name=_('cart'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    # product as a generic relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)

    def total_price(self):
        return self.quantity * self.unit_price

    total_price = property(total_price)


class Order(models.Model):
    delivery_address = models.CharField(max_length=255)
    card_name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=40)
    expiration_year = models.IntegerField()
    expiration_date = models.DateField()
    email = models.EmailField(max_length=100)
