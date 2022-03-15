from email import message
from msilib.schema import Shortcut
from wsgiref import validate
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from validate_email import validate_email
#import for encoding user token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.urls import reverse
from .utils import send_email_to_newly_registered_user
from .utils import token_generator

#for login
from django.contrib import auth

# Create your views here.
def userAlreadyAuthenticated(user):
    if user.is_authenticated:
        return True
    return False

class RegistrationView(View):
    def get(self, request):
        if userAlreadyAuthenticated(request.user):
            return redirect("expenses")
        return render(request, "authentication/register.html")
    
    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        context = {
            'fieldValues':request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password)<6:
                    messages.error(request, "Password must contain minimum 6 character")
                    return render(request, "authentication/register.html", context)
                user = User.objects.create_user(username=username, email = email)
                user.set_password(password)
                user.is_active = False
                domain = get_current_site(request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token})
                activation_url = "http://"+domain+link
                send_email_to_newly_registered_user(username, email, activation_url)
                user.save()
                messages.success(request, "Account successfully created")
                return render(request, "authentication/login.html")
            else:
                message.error(request, "user with this email already exists")
        else:
            message.error(request, "user with this username already exist")
        return render(request, "authentication/register.html")
    
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not token_generator.check_token(user, token):
                messages.success(request, "Account already Activated")
                return redirect("login"+"?message="+"User already activated")

            if user.is_active:
                messages.success(request, "Account already activated Successfully")
                return redirect("login")
            user.is_active = True
            user.save()
            messages.success(request, "Account activated Successfully")
            return redirect('login')
        except Exception as e:
            pass
        return redirect("login")


class LoginView(View):
    def get(self, request):
        if userAlreadyAuthenticated(request.user):
            return redirect("expenses")
        return render(request, "authentication/login.html")

    def post(self, request):
        data = request.POST
        username = data["username"]
        password = data["password"]
        if(username and password):
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome! {user.username} You are now logged in")
                    return redirect('expenses')
                else:
                  messages.error(request, f"Account is not active. Please check your email.")
                  return render(request, "authentication/login.html")
            else:
                messages.error(request, f"Either your Credentials are wrong or")
                messages.error(request, f"Maybe you haven't activated your account, Please check your mail and activate your account")
                return render(request, "authentication/login.html")
        messages.error(request, "Please fill all fields")
        return render(request, "authentication/login.html")


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been successfully Logged out")
        return redirect("login") 


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"].lower()

        if not str(username).isalnum() or username.isnumeric():
            return JsonResponse({'username_error':"Username should be alphanumeric"}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':"Username is already taken"}, status=409)
        return JsonResponse({"username_valid":True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"].lower()

        if not validate_email(email):
            return JsonResponse({'email_error':"Email format incorrect"}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':"Email already exists"}, status=409)
        return JsonResponse({"email_valid":True})