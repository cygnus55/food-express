from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import RequestContext

from restaurants.models import Restaurant
from foods.models import Food

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["restaurants"]= Restaurant.objects.all()
        context["foods"] = Food.objects.all()
        return context


def handler404(request, *args, **argv):
    return render(request, 'base/404.html')
