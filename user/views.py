from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User
from .forms import UserForm

def signup_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(id=form.cleaned_data['id']).exists():
                return render(request, 'signup.html', {'error': 'ID already exists'})
            if User.objects.filter(nickname=form.cleaned_data['nickname']).exists():
                return render(request, 'signup.html', {'error': 'Nickname already exists'})
            
            user = User.objects.create_user(
                id=form.cleaned_data['id'],
                password=form.cleaned_data['password'],
                nickname=form.cleaned_data['nickname'],
            )
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        id = request.POST['id']
        password = request.POST['password']
        user = authenticate(request, username=id, password=password)
        if user is not None:
            login(request, user)
            return redirect('/chat')  # Redirect to a success page
        else:
            return render(request, 'login.html', {'error': 'Invalid login'})
    return render(request, 'user/login.html')

# 로그아웃 view 작성
