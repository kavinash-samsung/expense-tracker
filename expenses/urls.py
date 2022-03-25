from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
        path("", views.index, name="expenses"),
        path("add-expense", views.add_expense, name="add-expenses"),
        path("edit-expense/<int:id>", views.edit_expense, name="edit-expenses"),
        path("delete-expense/<int:id>", views.delete_expense, name="delete-expenses"),
        path("search-expenses", csrf_exempt(views.search_expenses), name="search-expenses"),
        path("expense-category-summary", views.expense_category_summary, name="expense-category-summary"),
        path("expense-stats", views.expense_stats_view, name="expense-stats"),
        path("export-csv", views.export_csv, name="exp-export-csv"),
        path("export-xls", views.export_excel, name="exp-export-excel"),
        path("export-pdf", views.export_pdf, name="exp-export-pdf"),

    ]