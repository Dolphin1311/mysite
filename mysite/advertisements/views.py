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


# def add_adv(request: HttpRequest):
#     if request.method == 'POST':
#         form = AdvertisingSpaceForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#         else:
#             print('Data is not valid')
#         print(form.cleaned_data)
#
#     else:
#         form = AdvertisingSpaceForm()
#
#     return render(request, 'advertisements/add_adv.html', {'title': 'Add adv', 'form': form})
