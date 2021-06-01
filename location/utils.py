from django.contrib.gis.geoip2 import GeoIP2
from requests import get


def get_geolocation(ip):
    geo = GeoIP2()
    country = geo.country(ip)
    city = geo.city(ip)
    latitude, longitude = geo.lat_lon(ip)
    return {
        'country': country, 
        'city': city, 
        'latitude': latitude,
        'longitude': longitude
        }


def get_your_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        ip = xff.split(',')[0]
        print('#################',ip)
    else:
        ip = get('https://api.ipify.org').text
        print('***************',ip)
    return ip