from django.contrib import admin
from django.urls import path, include, register_converter
from . import views
from .converters import DateConverter

register_converter(DateConverter, 'date')

urlpatterns = [
    path("", views.index, name="index"),
    path("<date:date>", views.viewExpenses),
    path("changemonth", views.changeMonth, name="changeMonth"),
    path("expense/edit/<int:id>",views.editExpense),
    path("expense/add",views.newExpense),
    path("category/add",views.newCategory),
    path("category/edit/<int:id>",views.editCategory),
]