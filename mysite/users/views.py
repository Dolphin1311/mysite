from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .forms import NewUserForm, NewPersonForm


def register_user(request):
    if request.method == 'POST':
        user_form = NewUserForm(request.POST)
        person_form = NewPersonForm(request.POST)

        if all([user_form.is_valid(), person_form.is_valid()]):
            user = user_form.save()
            person = person_form.save(commit=False)
            person.user = user
            person.save()
            login(request, user)

            return render(request, 'users/user-registration.html')
    else:
        user_form = NewUserForm()
        person_form = NewPersonForm()

    return render(request, 'users/user-registration.html', {'user_form': user_form,
                                                            'person_form': person_form})


class LoginUserView(FormView):
    template_name = 'users/user-login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #
    #     if form.is_valid():
    #         email = form.cleaned_data['email']
    #         password = form.cleaned_data['email']
    #         user = authenticate(email=email, password=password)
    #
    #         if user is not None:
    #             login(request, user)
    #
    #         else:
    #             print('Invalid username or login.')
    #     else:
    #         print('Form is not valid.')

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)

        return render(request, self.template_name, {'form': form})
