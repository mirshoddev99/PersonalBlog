from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from members.forms import CustomUserRegisterForm
from members.models import CustomUser


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {"login_form": login_form}
        return render(request, 'registration/login.html', context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect("home")

        context = {"login_form": login_form}
        return render(request, 'registration/login.html', context)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("main")


class RegisterView(View):
    def get(self, request):
        user_form = CustomUserRegisterForm()
        contex = {"user_form": user_form}
        return render(request, "registration/register.html", contex)

    def post(self, request):
        user_form = CustomUserRegisterForm(data=request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "You have successfully registered")
            return redirect("members:login")
        return render(request, "registration/register.html", {"user_form": user_form})
