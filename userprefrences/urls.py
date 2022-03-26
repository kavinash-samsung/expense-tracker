from django.urls import path
from userprefrences import views

urlpatterns = [
    path('', views.index, name="prefrences")
]