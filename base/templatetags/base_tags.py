from re import IGNORECASE, compile, escape as rescape

from django import template
from django.utils.safestring import mark_safe

from restaurants.models import Restaurant

register = template.Library()


@register.simple_tag
def add(a, b):
    return a + b


@register.filter(name='highlight')
def highlight(text, search):
    rgx = compile(rescape(search), IGNORECASE)
    return mark_safe(
        rgx.sub(
            lambda m: '<b class="text text-danger bg-warning">{}</b>'.format(m.group()),
            text
        )
    )


@register.simple_tag
def matching_food(obj: Restaurant, keyword=None):
    count = obj.foods.filter(name__icontains=keyword).count()
    return count
