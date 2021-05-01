from django.shortcuts import render
from django.views.generic import TemplateView
from restaurants.models import Restaurant
from django.template import RequestContext


# Create your views here.


class HomePageView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        restaurants = Restaurant.objects.all()[:3]
        context['restaurants'] = restaurants
        return context



def handler404(request, *args, **argv):
    return render(request, 'base/404.html')
