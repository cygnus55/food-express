from re import IGNORECASE, compile, escape as rescape
from typing import Union

from django import template
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from restaurants.models import Restaurant
from foods.models import Food
from fav.models import Favorite

register = template.Library()


@register.simple_tag
def add(a: int, b: int) -> int:
    return a + b


@register.filter(name='highlight')
def highlight(text: str, search):
    rgx = compile(rescape(search), IGNORECASE)
    return mark_safe(
        rgx.sub(
            lambda m: '<b class="text text-danger bg-warning">{}</b>'.format(m.group()),
            text
        )
    )


@register.simple_tag
def matching_food(obj: Restaurant, keyword=None) -> int:
    count = obj.foods.filter(name__icontains=keyword).count()
    return count


@register.simple_tag
def is_favourite(obj: Union[Food, Restaurant], user) -> bool:
    fav = Favorite.objects.get_favorite(user, obj)
    if fav:
        return True
    return False