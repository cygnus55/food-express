from .models import DeliveryLocation

def get_delivery_location(request):
    if request.user.is_anonymous:
        locations = None
    elif request.user.is_customer:
        try:
            locations = DeliveryLocation.objects.filter(customer=request.user.customer)
        except Exception:
            locations = None
    else:
        locations = None
    
    return  {'delivery_locations': locations}
    
