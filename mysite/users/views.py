from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import NewUserForm, NewPersonForm


def sign_up_user(request):
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
                                                            'person_form': person_form,
                                                            'title': 'Sign up'})


def sign_in_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)

                return redirect('home')
            else:
                print('Invalid email or password')

    form = AuthenticationForm()

    return render(request, 'users/user-login.html', context={'form': form,
                                                             'title': 'Sign in'})


