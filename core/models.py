from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from .validators import validate_size


class Publication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class PublicationEntity(models.Model):
    PDF = 'PDF'
    PAPERBACK = 'PAPERBACK'
    AUDIO = 'AUDIO'
    PUBLICATION_TYPE_CHOICES = (
        (PDF, 'PDF'),
        (PAPERBACK, 'PAPERBACK'),
        (AUDIO, 'AUDIO'),
    )

    publication = models.ForeignKey('Publication')
    publication_type = models.CharField(max_length=10, choices=PUBLICATION_TYPE_CHOICES)
    price = models.PositiveIntegerField(null=True)
    link = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return '{}_{}'.format(self.publication.name, self.publication_type)


class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    discount = models.PositiveIntegerField(default=0)

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
    card_number = models.CharField(max_length=50)
    expiration_year = models.IntegerField()
    expiration_date = models.DateField()
    email = models.EmailField(max_length=100)

    def __unicode__(self):
        return self.delivery_address


class Discount(models.Model):
    code = models.CharField(max_length=16, validators=[validate_size])
    discount = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.code
