from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods

# Create your views here.
class UserLogin(View):
    template_name="user/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('these are username and password in post')
        print(username, password)

        user = authenticate(request, username=username, password=password)
        print('this is the returned user from aunthenticate....')
        print(user)

        if user is not None:
            print('everything is good login me')
            login(request, user)
            return redirect("register")
        
        else:
            print('Invalid credentials....')
            messages.info(request, 'Invalid credentials!')
            return render(request, self.template_name)