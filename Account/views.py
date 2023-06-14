from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings
import random

from .models import Customer, User_otp

def Login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":

        otps = request.POST.get('otp')

        if otps:
            user = request.POST.get('user')
            usr = User.objects.get(username=user)
            if int(otps) == User_otp.objects.filter(user = usr).last().otp:
                usr.is_active = True
                usr.save()
                auth.login(request, usr)
                return redirect('/')
            else:
                messages.warning(request, f"You Entered wrong OTP")
                return render(request, 'login.html', {'otp':True, 'user':user})

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in successfully.")
            return redirect("/")
        elif not User.objects.filter(username = username).exists():
            messages.warning(request, "Please enter correct credentials")
            return redirect('/Account/login')
        elif not User.objects.get(username=username).is_active:
            user = User.objects.get(username = username)
            user_otp = random.randint(100000, 999999)
            User_otp.objects.create(user = user, otp = user_otp)
            msg = f"hello {user.username},\nYour Otp is {user_otp}\nThanks!"
            send_mail(
                "Welcome to Wishfood",
                msg,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently = False
            )
            return render(request, 'login.html', {'otp':True, 'user':user})
        else:
            messages.warning(request, "Please enter correct credentials")
            return redirect('/Account/login')
    else:
        context = {}
        return render(request, 'login.html', context)

def Signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        otps = request.POST.get('otp')

        if otps:
            user = request.POST.get('user')
            usr = User.objects.get(username=user)
            if int(otps) == User_otp.objects.filter(user = usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.success(request, f"Account Created for {usr.username}")
                return redirect('login')
            else:
                messages.warning(request, f"You Entered wrong OTP")
                return render(request, 'signup.html', {'otp':True, 'user':user})

        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists')
                return redirect('/Account/signup')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'This email address already exists')
                return redirect('/Account/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.is_active = False
                user.save()
                user_otp = random.randint(100000, 999999)
                User_otp.objects.create(user = user, otp = user_otp)
                msg = f"hello {user.username},\nYour Otp is {user_otp}\nThanks!"
                send_mail(
                    "Welcome to Wishfood",
                    msg,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently = False
                )
                
                Customer.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email,
                )
                return render(request, 'signup.html', {'otp':True, 'user':user})
                #return redirect('/Account/login')
        else:
            messages.warning(request, 'Password does not match')
            return redirect('/Account/signup')
    else:
        return render(request, 'signup.html')

def Logout(request):
    auth.logout(request)
    return redirect("/")

def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                return redirect('/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'change_password.html', {'form': fm})
    else:
        return redirect('/accounts/login')
