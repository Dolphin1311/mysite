from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views.generic import ListView
from .forms import UserForm, PersonForm  # , LoginForm
from advertisements.models import AdvertisingSpace


def signup_view(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST)

        if all([user_form.is_valid(), person_form.is_valid()]):
            user = user_form.save()
            person = person_form.save(commit=False)
            person.user = user
            person.save()
            login(request, user)

            return redirect("home")
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
    # form_class = LoginForm


def logout_view(request):
    logout(request)

    return redirect("login")


class UserCabinetAdvSpacesView(ListView, LoginRequiredMixin):
    template_name = "users/user_cabinet_adv_spaces.html"
    context_object_name = "adv_spaces"

    def get_queryset(self):
        # get all adv spaces for current logged in user
        return AdvertisingSpace.objects.filter(user=self.request.user)
