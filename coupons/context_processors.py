from .models import Coupon

def get_restaurant_coupons(request):
    if request.user.is_anonymous:
        coupons = None
    elif request.user.is_restaurant:
        coupons = Coupon.activated.filter(restaurant=request.user.restaurant)
    else:
        coupons = None
    return {'active_coupons': coupons}