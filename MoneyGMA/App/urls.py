from django.contrib import admin
from django.urls import path, include, register_converter
from . import views
from .converters import DateConverter

register_converter(DateConverter, 'date')

urlpatterns = [
    path("", views.index, name="index"),
    path("<date:date>", views.viewExpenses),
    path("viewMonthlyExpenses/<int:year>/<int:monthNum>", views.viewMonthlyExpenses, name="viewMonthlyExpenses"),
    path("changemonth", views.changeMonth, name="changeMonth"),
    path("expense/edit/<int:id>",views.editExpense, name="editExpense"),
    path("expense/add",views.newExpense, name="addExpense"),
    path("category",views.viewCategories, name="categories"),
    path("category/add",views.newCategory, name="addCategory"),
    path("category/edit/<str:name>",views.editCategory, name="editCategory"),
    path("pools", views.moneyPools, name="moneyPools"),
    path("pools/<int:poolId>", views.viewPool, name="viewPool"),
    path("pools/edit/<int:poolId>", views.editPool, name="editPool"),
    path("pools/add", views.addPool, name="addPool"),
]