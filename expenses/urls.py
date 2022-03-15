from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="expenses"),
        path("add-expense", views.add_expense, name="add-expenses"),
        path("edit-expense/<int:id>", views.edit_expense, name="edit-expenses"),
        path("delete-expense/<int:id>", views.delete_expense, name="delete-expenses"),

    ]