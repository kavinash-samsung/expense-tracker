from expenses.models import Expense
from income.models import UserIncome
from userprefrences.views import get_currency_name
from helper.utils import html_to_pdf, stats_till_today
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url="/authentication/login/")
def home(request):
    
    last_six_month_expense = stats_till_today(Expense, request.user, 180)
    last_one_month_expense = stats_till_today(Expense, request.user, 30)

    last_six_month_income = stats_till_today(UserIncome, request.user, 180)
    last_one_month_income = stats_till_today(UserIncome, request.user, 30)

    context = {
        'last_six_month_expense':last_six_month_expense,
        'last_one_month_expense':last_one_month_expense,
        'last_six_month_income':last_six_month_income,
        'last_one_month_income':last_one_month_income
    }

    return render(request, "index.html", context)


def summary_pdf(request):
    pdf_path = "pdfs/summary-pdf.html"
    income = UserIncome.objects.filter(owner=request.user)
    expense = Expense.objects.filter(owner=request.user)
    currency = currency = get_currency_name(request.user)
    context = {
        'expenses':expense,
        'income':income,
        'currency':currency
    }
    pdf = html_to_pdf(pdf_path, context)
    return HttpResponse(pdf, content_type="application/pdf")