from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,CreateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.forms import  UserCreationForm
from space.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password

# Create your views here.
class loginView(View):
    template_name="accounts/login.html"
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        user=User.objects.filter(email=email)
        if not user.exists():
            return HttpResponse("Account not found!!")
        
        user_obj=authenticate(email=email,password=password)
        if user_obj:
            login(request,user_obj)
            if user_obj.role == "seller":
                return redirect("seller")
            elif user_obj.role == "buyer":
                return redirect("price")
            else:
                return redirect("/")
        return HttpResponse("Invalid Credentials")

class SignUpView(View):
    def get(self, request):
        return render(request, "accounts/signup.html")
    
    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        role = request.POST["role"]
        if password == confirm_password:
            User.objects.create(email=email, password=make_password(password), role=role)
        else:
            return HttpResponse("Password does not match.")
        return redirect("login")


   