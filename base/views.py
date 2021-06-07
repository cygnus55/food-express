from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import RequestContext

from restaurants.models import Restaurant
from foods.models import Food


class HomePageView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurants']= Restaurant.objects.filter(available=True)[:8]
        context['foods'] = Food.objects.filter(restaurant__available=True).filter(available=True)[:8]
        return context


class SearchView(TemplateView):
    template_name = 'base/search.html'

    def get_context_data(self, **kwargs):
        keyword = self.request.GET.get('q')
        context = super().get_context_data(**kwargs)
        context['restaurants'] = Restaurant.objects.all()
        context['foods'] = Food.objects.all()
        context['keyword'] = ''
        if keyword:
            context['keyword'] = keyword
            context['restaurants'] = Restaurant.objects.filter(name__icontains=keyword).distinct() | Restaurant.objects.filter(foods__name__icontains=keyword).distinct()
            context['foods'] = Food.objects.filter(name__icontains=keyword)
        return context


def handler404(request, *args, **argv):
    return render(request, 'base/404.html')

class HowToOrder(TemplateView):
    template_name = 'base/how-to-order.html'
