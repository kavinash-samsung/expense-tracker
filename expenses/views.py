from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Expense
from django.contrib import messages

from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url="/authentication/login/")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        "expenses":expenses,
        "page_obj":page_obj
    }
    return render(request, "expenses/index.html", context)
    
@login_required(login_url="/authentication/login/")
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
    }
    if request.method == "GET":
        return render(request, "expenses/add_expense.html", context)

    if request.method == "POST":
        context["values"] = request.POST
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)
        category = request.POST['category']
        if not category:
            messages.error(request, 'category is required')
            return render(request, 'expenses/add_expense.html', context)
        expense = Expense.objects.create(amount=amount, description=description, category=category, owner=request.user)
        date = request.POST['expense_date']
        if date:
            expense.date = date
        expense.save()
        messages.success(request, 'Expense added successfully')
        return redirect("expenses")
        return render(request, 'expenses/add_expense.html', context)

def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all().exclude(name = expense.category)
    context = {
        'values': expense,
        'categories':categories,
    }
    if request.method == "GET":
        return render(request, 'expenses/edit-expense.html', context)

    if request.method == "POST":
        context["values"] = request.POST

        amount = request.POST['amount']
        if amount:
            expense.amount = amount

        description = request.POST['description']
        if description:
            expense.category = description

        category = request.POST['category']
        if category:
            expense.category = category
        date = request.POST['expense_date'] 
        if date:
            expense.date = date     
        expense.save()
        messages.success(request, 'Expense Updated successfully')
        return redirect("expenses")
        messages.success(request, "Post form Updated")
        return render(request, 'expenses/edit-expense.html', context)
        
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    context = {
        'expense':expense,
    }
    if request.method == "POST":
        expense.delete()
        messages.success(request, 'Expense Deleted successfully')
        return redirect("expenses")
    else:
        return render(request, 'expenses/delete-expense.html', context)