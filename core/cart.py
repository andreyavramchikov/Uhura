from core import models
import datetime

CART_ID = 'CART-ID'


class Cart(object):

    def __init__(self, request):
        cart_id = request.session.get(CART_ID)
        if cart_id:
            cart = models.Cart.objects.get(id=cart_id)
        else:
            cart = self.new(request)

        self.cart = cart

    def __iter__(self):
        for item in self.cart.cartitem_set.all():
            yield item

    def new(self, request):
        cart = models.Cart.objects.create(creation_date=datetime.datetime.now())
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, product, unit_price, quantity=1):
        try:
            item = models.CartItem.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.CartItem.DoesNotExist:
            item = models.CartItem()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else:  # ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity += int(quantity)
            item.save()