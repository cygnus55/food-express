from .cart import Cart
from .forms import CartAddFoodForm

def cart(request):
    return {'cart': Cart(request), 'cart_add_form': CartAddFoodForm()}