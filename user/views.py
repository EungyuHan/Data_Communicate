from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .forms import UserForm

def signup_view(request):
    form = UserForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            if User.objects.filter(id=form.cleaned_data['id']).exists():
                form.add_error('id', '이미 존재하는 아이디입니다.')
                return render(request, 'user/user.html', {'form': form})
            if User.objects.filter(nickname=form.cleaned_data['nickname']).exists():
                form.add_error('nickname', '이미 존재하는 닉네임입니다.')
                return render(request, 'user/user.html', {'form': form})

            user = User.objects.create_user(
                id=form.cleaned_data['id'],
                password=form.cleaned_data['password'],
                nickname=form.cleaned_data['nickname'],
            )
            login(request, user)
            return redirect('/')
    else:
        form = UserForm()

    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
    else:
        form = AuthenticationForm()

    return render(request, 'user/login.html', {'form': form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')