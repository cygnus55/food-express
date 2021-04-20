from django.shortcuts import render
from django.views.generic import TemplateView

from django.template import RequestContext


# Create your views here.


class HomePageView(TemplateView):
    template_name = 'base/home.html'


def handler404(request, *args, **argv):
    return render(request, 'base/404.html')
