from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Source, UserIncome
from userprefrences.models import UserPrefrences

from django.contrib import messages

from django.core.paginator import Paginator
import json
from django.http import JsonResponse

# Create your views here.

@login_required(login_url="/authentication/login/")
def index(request):
    sources = Source.objects.all()
    userIncome = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(userIncome, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPrefrences.objects.get(user = request.user).currency_name()
    context = {
        "income":userIncome,
        "page_obj":page_obj,
        "currency":currency,
    }
    return render(request, "income/index.html", context)
    
@login_required(login_url="/authentication/login/")
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources':sources,
    }
    if request.method == "GET":
        return render(request, "income/add_income.html", context)

    if request.method == "POST":
        context["values"] = request.POST
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        description = request.POST['description']
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/add_income.html', context)
        source = request.POST.get('source')
        if not source:
            messages.error(request, 'source is required')
            return render(request, 'income/add_income.html', context)
        income = UserIncome.objects.create(amount=amount, description=description, source=source, owner=request.user)
        date = request.POST['income_date']
        if date:
            income.date = date
        income.save()
        messages.success(request, 'Income added successfully')
        return redirect("income")
        return render(request, 'income/add_income.html', context)

@login_required(login_url="/authentication/login/")
def edit_income(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all().exclude(name = income.source)
    context = {
        'values': income,
        'sources':sources,
    }
    if request.method == "GET":
        return render(request, 'income/edit-income.html', context)

    if request.method == "POST":
        context["values"] = request.POST

        amount = request.POST['amount']
        if amount:
            income.amount = amount

        description = request.POST['description']
        if description:
            income.category = description

        source = request.POST.get('source')
        if source:
            income.source = source
        date = request.POST['income_date'] 
        if date:
            income.date = date     
        income.save()
        messages.success(request, 'Income Updated successfully')
        return redirect("income")
        messages.success(request, "Post form Updated")
        return render(request, 'income/edit-income.html', context)

@login_required(login_url="/authentication/login/")       
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    context = {
        'income':income,
    }
    if request.method == "POST":
        income.delete()
        messages.success(request, 'Income Deleted successfully')
        return redirect("income")
    else:
        return render(request, 'income/delete-income.html', context)

# @login_required(login_url="/authentication/login/")
def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
    
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            source__istartswith=search_str, owner=request.user)

        data = income.values()
        return JsonResponse(list(data), safe=False)


