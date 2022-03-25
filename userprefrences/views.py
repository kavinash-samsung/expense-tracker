from locale import currency
from django.shortcuts import render
import os
import json
from django.conf import settings 
from .models import UserPrefrences
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def get_currency_name(user):
    try:
        currency = UserPrefrences.objects.get(user = user)
    except:
        currency = UserPrefrences.objects.create(user=user)
    currency = currency.currency_name()
    return currency

@login_required(login_url="/authentication/login/")
def index(request):
    user_prefrences = UserPrefrences.objects.filter(user=request.user).exists()
    if not user_prefrences:
        user_prefrences = UserPrefrences.objects.create(user=request.user)
        user_prefrences.save()
    else:
        user_prefrences = UserPrefrences.objects.get(user=request.user)
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currency.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    if request.method == "POST":
        currency = request.POST['currency']
        user_prefrences.currency = currency
        messages.success(request, "Prefrences saved")
    user_prefrences.save()


    currency_data.append({'name':user_prefrences.currency_name(), 'value':data[user_prefrences.currency_name()]})
    del data[user_prefrences.currency] 
    for k,v in data.items():
        currency_data.append({'name':k, 'value':v})


    return render(request, 'prefrences/index.html',{'currencies':currency_data})
    