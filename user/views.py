from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .forms import UserForm

def user_view(request):
    if request.method == "POST":
        if 'signup' in request.POST:
            signup_form = UserForm(request.POST)
            if signup_form.is_valid():
                user = User.objects.create_user(
                    id=signup_form.cleaned_data['id'],
                    password=signup_form.cleaned_data['password'],
                    nickname=signup_form.cleaned_data['nickname'],
                )
                login(request, user)
                return redirect('/')
        elif 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                return redirect('/')
        elif 'logout' in request.POST:
            logout(request)
            return redirect('/')
    else:
        signup_form = UserForm()
        login_form = AuthenticationForm()

    return render(request, 'user/user.html', {'signup_form': signup_form, 'login_form': login_form})
