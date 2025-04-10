from datetime import datetime, timezone
from django.core.exceptions import *
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from frontend import template
# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user.last_login = datetime.now(timezone.utc)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Invalid username or password')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        try:
            validate_password(password)
            user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name,date_joined=datetime.now(timezone.utc))
            user.save()
            return redirect('login')
        except ValidationError:
            messages.warning(request,'The password must contain at least 8 characters.')
        except IntegrityError:
            messages.warning(request,'Username already taken')
    return render(request, 'register.html')

def home_view(request):
    return render(request,'index.html')
def logout_view(request):
    logout(request)
    return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not (username and old_password and new_password and confirm_password):
            messages.error(request, 'Vui lòng nhập đầy đủ thông tin.')
            return render(request, 'reset-pass.html')
        
        user = authenticate(request, username=username, password=old_password)

        if user is not None:
            if new_password == confirm_password:
                try:
                    user.set_password(new_password)
                    user.save()

                    messages.success(request, 'Password has been successfully changed. Please log in again with the new password!')
                    return redirect('login')  
                except Exception as e:
                    messages.error(request, f'Có lỗi xảy ra: {str(e)}')
            else:
                messages.error(request, 'New password and confirmation password do not match!')
        else:
            messages.error(request, 'Username or old password is incorrect!')

    return render(request, 'reset-pass.html')
