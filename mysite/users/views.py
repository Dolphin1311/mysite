from django.shortcuts import render
from django.views.generic import FormView
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

            return render(request, 'users/user_registration.html')
    else:
        user_form = NewUserForm()
        person_form = NewPersonForm()

    return render(request, 'users/user_registration.html', {'user_form': user_form,
                                                            'person_form': person_form})
