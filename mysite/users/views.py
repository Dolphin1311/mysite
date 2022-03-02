from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin, UpdateView

from orders.forms import FilterOrdersForm
from orders.models import Order
from .forms import UserForm, PersonForm, LoginForm
from advertisements.models import AdvertisingSpace
from .models import User, Person


def signup_view(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST)
        print(user_form.errors, person_form.errors)
        if all([user_form.is_valid(), person_form.is_valid()]):
            user = user_form.save()
            person = person_form.save(commit=False)
            person.user = user
            person.save()
            login(request, user)

            return redirect("user_cabinet")
        else:
            return render(
                request,
                "users/user_registration.html",
                {
                    "user_form": user_form,
                    "person_form": person_form,
                    "title": "Sign up",
                },
            )
    else:
        user_form = UserForm()
        person_form = PersonForm()

    return render(
        request,
        "users/user_registration.html",
        {"user_form": user_form, "person_form": person_form, "title": "Sign up"},
    )


class UserLoginView(LoginView):
    template_name = "users/user_login.html"
    next_page = reverse_lazy("user_cabinet")
    form_class = LoginForm


def logout_view(request):
    logout(request)

    return redirect("login")


class UserCabinetAdvSpacesListView(ListView, LoginRequiredMixin):
    model = AdvertisingSpace
    template_name = "users/user_cabinet_adv_spaces.html"
    context_object_name = "adv_spaces"

    def get_queryset(self):
        # get all adv spaces for current logged in user
        return AdvertisingSpace.objects.filter(user=self.request.user)


class UserCabinetOrdersListView(ListView, LoginRequiredMixin, FormMixin):
    model = Order
    template_name = "users/user_cabinet_orders.html"
    context_object_name = "orders"
    form_class = FilterOrdersForm

    # get filtered orders by settings from form_class
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        orders = Order.objects.all()
        if form.is_valid():
            if form.cleaned_data["end_user"] == "owner":
                orders = Order.objects.filter(
                    is_confirmed=form.cleaned_data["status"],
                    advertising_space__user=self.request.user,
                )
            elif form.cleaned_data["end_user"] == "client":
                orders = Order.objects.filter(
                    is_confirmed=form.cleaned_data["status"], client=self.request.user
                )

        return render(request, self.template_name, {"orders": orders, "form": form})


class UserCabinetUpdatePersonalDataView(TemplateView, LoginRequiredMixin):
    model = User
    form_class = UserForm
    template_name = "users/user_cabinet_data.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = self.form_class(instance=self.request.user)
        context["person_form"] = PersonForm(instance=Person.objects.get(user=self.request.user))

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.request.user)
        person_form = PersonForm(data=request.POST, instance=Person.objects.get(user=self.request.user))

        if all([form.is_valid(), person_form.is_valid()]):
            form.save()
            person_form.save()

            return redirect("login")
        else:
            return render(
                request,
                self.template_name,
                context={
                    "user_form": form,
                    "person_form": person_form
                }
            )
