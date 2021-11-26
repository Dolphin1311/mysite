from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import AdvertisingSpaceForm
from .models import AdvertisingSpace


def index(request: HttpRequest):
    return HttpResponse('First page')


class AddAdv(CreateView):
    form_class = AdvertisingSpaceForm
    template_name = 'advertisements/add_adv.html'
