from expenses.models import Expense
from income.models import UserIncome
from userprefrences.views import get_currency_name
from helper.utils import html_to_pdf
from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    return render(request, "index.html")


def summary_pdf(request):
    pdf_path = "summary-pdf.html"
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