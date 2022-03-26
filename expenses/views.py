from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Category, Expense
from userprefrences.views import get_currency_name

from django.contrib import messages

from django.core.paginator import Paginator
import json
import csv
import xlwt
from django.http import JsonResponse, HttpResponse
import datetime

from helper.utils import html_to_pdf

# Create your views here.


@login_required(login_url="/authentication/login/")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    
    currency = get_currency_name(request.user)
    
    context = {
        "expenses":expenses,
        "page_obj":page_obj,
        "currency":currency,
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

@login_required(login_url="/authentication/login/")
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

        amount = request.POST.get('amount')
        if amount:
            expense.amount = amount

        description = request.POST.get('description')
        if description:
            expense.description = description

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

@login_required(login_url="/authentication/login/")       
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

# @login_required(login_url="/authentication/login/")
def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
    
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            category__istartswith=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)
@login_required(login_url="/authentication/login/")
def expense_stats_view(request):
    context = {}
    return render(request, 'expenses/expense-stats.html', context)

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=180)
    one_year_ago = todays_date - datetime.timedelta(days = 365)

    expenses = Expense.objects.filter(owner=request.user, date__gte = six_months_ago, date__lte = todays_date)

    def get_category(expense):
        return expense.category
    
    category_list = list(set(map(get_category,  expenses)))
    print("ok")

    def get_expense_category_amount(category):
        amount = 0
        print("OK")
        filtered_by_category = expenses.filter(category=category)
        print("OK")
        print(filtered_by_category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    finalrep = {}
    print("ok")
    # for x in expenses:
    for y in category_list:
        print("asdfkjahsfklaj",y)
        finalrep[y] = get_expense_category_amount(y)
    print("ok")
    print(finalrep)
    
    return JsonResponse({'expense_category_data': finalrep}, safe=False)



def export_csv(request):
    response = HttpResponse(content_type="/text/csv")
    response['Content-Disposition'] = 'attachment: filename=Expenses' + \
        str(datetime.datetime.now())+'.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])
    
    return response

def export_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = "attachment: filename=Expenses" + \
        str(datetime.datetime.now())+'.xls'
    
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Expenses")
    
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', "Date"]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list(
        'amount', 'description', 'category', 'date')
    print(rows)
 
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    
    wb.save(response)

    return response


def export_pdf(request):
    pdf_path = "pdfs\expenses-pdf.html"
    expenses = Expense.objects.filter(owner=request.user)
    currency = currency = get_currency_name(request.user)
    context = {
        'expenses':expenses,
        'currency':currency
    }
    pdf = html_to_pdf(pdf_path, context)
    return HttpResponse(pdf, content_type="application/pdf")




