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

from helper.utils import send_email_to_newly_registered_user, send_email_for_password_reset
from helper.utils import token_generator

#for login
from django.contrib import auth

from django.contrib.auth.tokens import PasswordResetTokenGenerator



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
                messages.success(request, "Account created! Activate your account")
                messages.success(request, "Link for account activation is sended to you via mail")
                return render(request, "authentication/user-successful.html")
            else:
                messages.error(request, "user with this email already exists")
        else:
            messages.error(request, "user with this username already exist")
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
            print(f"Outside try block {username}")
            if not user:
                try:
                    print(f"Inside try block {username}")
                    user = User.objects.get(email=username)
                    user = auth.authenticate(username=user.username, password=password)
                except:
                    pass
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome! {user.username.title()} You are now logged in")
                    return redirect('expenses')
            else:
                try:
                    try:
                        user = User.objects.get(username = username)
                    except:
                        user = User.objects.get(email = username)
                         
                    if user.is_active:
                        messages.error(request, f"Your Credentials are wrong")
                    else:
                        messages.error(request, f"Account is not active. Please check your email and activate your account")
                    return render(request, "authentication/login.html")
                except:
                    messages.error(request, f"User with username {username} does not exist! Please Register yourself first")
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


class requestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    
    def post(self, request):
        context = {
            'values':request.POST,
        }
        email = request.POST.get("email")
        if not validate_email(email):
            messages.error(request, 'Please supply a valid email')
            return render(request, 'authentication/reset-password.html', context)
        
        current_site = get_current_site(request)
        
        try:
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            link = reverse('reset-user-password', kwargs={'uidb64':uidb64, 'token':token})
            print(link)
            email_subject = "Reset Your password"

            reset_link_url = 'http://'+current_site.domain+link

            send_email_for_password_reset(email, reset_link_url)

            messages.success(request,"We have sent you an email to reset your password")
            return render(request, 'authentication/reset-password.html')
        except:
            messages.error(request,"User with this email does not exist")
            return render(request, 'authentication/reset-password.html')

    

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        
        context = {
            "uuid64": uidb64,
            "token": token,
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64)) 
            user = User.objects.get(pk = user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Link Already used! Request new one here")
                return render(request, 'authentication/reset-password.html',context)
            
            messages.info(request, "Set new password")
            return render(request, 'authentication/set-new-password.html',context)
        
        except:
            messages.info(request, "Something Went Wrong")
            return render(request, 'authentication/reset-password.html',context)


    def post(self, request, uidb64, token):
        context = {
            "uuid64": uidb64,
            "token": token,
        }
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if(password != password2):
            messages.error(request, "Password do not match")
            return render(request, 'authentication/set-new-password.html',context)
        if(len(password)<6):
            messages.error(request, "Password must be of 6 character or more")
            return render(request, 'authentication/set-new-password.html',context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64)) 
            user = User.objects.get(pk = user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("login")
        except:
            messages.info(request, "Something went wrong, Try Again")
            return render(request, 'authentication/set-new-password.html',context)
    

def account_view(request):
    return render(request, 'authentication/account.html')
