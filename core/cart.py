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

    @staticmethod
    def new(request):
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

    def count(self):
        result = 0
        for item in self.cart.item_set.all():
            result += 1 * item.quantity
        return result

    def summary(self):
        result = 0
        for item in self.cart.cartitem_set.all():
            result += item.total_price
        return result - self.cart.discount

    def apply_discount(self, discount):
        cart = self.cart
        cart.discount = discount
        cart.save()

    def clear(self):
        for item in self.cart.cartitem_set.all():
            item.delete()
