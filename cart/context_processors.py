from cart.cart import Cart
from cart.forms import CartAddFoodForm


def cart(request):
    return {'cart': Cart(request), 'cart_add_form': CartAddFoodForm()}