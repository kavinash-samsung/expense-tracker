from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Source, UserIncome
from userprefrences.models import UserPrefrences

from django.contrib import messages

from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import csv, xlwt
import datetime
# Create your views here.

@login_required(login_url="/authentication/login/")
def index(request):
    sources = Source.objects.all()
    userIncome = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(userIncome, 4)
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

@login_required(login_url="/authentication/login/")   
def income_stats_view(request):
    context = {}
    return render(request, 'income/income-stats.html', context)

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=180)
    one_year_ago = todays_date - datetime.timedelta(days = 365)

    income = UserIncome.objects.filter(owner=request.user, date__gte = six_months_ago, date__lte = todays_date)

    def get_income(income):
        return income.source
    
    source_list = list(set(map(get_income,  income)))
    print("ok")

    def get_income_source_amount(source):
        amount = 0
        print("OK")
        filtered_by_source = income.filter(source=source)
        print("OK")
        print(filtered_by_source)
        for item in filtered_by_source:
            amount += item.amount
        return amount

    finalrep = {}
    print("ok")
    # for x in income:
    for y in source_list:
        print("asdfkjahsfklaj",y)
        finalrep[y] = get_income_source_amount(y)
    print("ok")
    print(finalrep)
    
    return JsonResponse({'income_source_data': finalrep}, safe=False)

def export_csv(request):
    response = HttpResponse(content_type="/text/csv")
    response['Content-Disposition'] = 'attachment: filename=Income'+\
        str(datetime.datetime.now())+'.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Amount', "Description", "Source", "Date"])

    income = UserIncome.objects.filter(owner=request.user)

    for inc in income:
        writer.writerow([inc.amount, inc.description, inc.source, inc.date])
    
    return response

def export_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = "attachment: filename=Income" + \
        str(datetime.datetime.now())+'.xls'
    
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Income")
    
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Source', "Date"]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = UserIncome.objects.filter(owner=request.user).values_list(
        'amount', 'description', 'source', 'date')
    print(rows)
 
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    
    wb.save(response)

    return response





