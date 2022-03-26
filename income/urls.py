from django.urls import path
from income import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
        path("", views.index, name="income"),
        path("add-income", views.add_income, name="add-income"),
        path("edit-income/<int:id>", views.edit_income, name="edit-income"),
        path("delete-income/<int:id>", views.delete_income, name="delete-income"),
        path("search-income", csrf_exempt(views.search_income), name="search-income"),
        path("income-source-summary", views.income_source_summary, name="income-source-summary"),
        path("income-stats", views.income_stats_view, name="income-stats"),
        path("export-csv", views.export_csv, name="inc-export-csv"),
        path("export-xls", views.export_excel, name="inc-export-excel"),
        path("export-pdf", views.export_pdf, name="inc-export-pdf"),
    ]