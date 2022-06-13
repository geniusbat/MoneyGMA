from django.contrib import admin
from django.urls import path, include, register_converter
from . import views
from .converters import DateConverter

register_converter(DateConverter, 'date')

urlpatterns = [
    path("index", views.index, name="index"),
    path("", views.login, name="login"),
    path("unlog", views.unlog, name="unlog"),
    path("login", views.handleLogin, name="handleLogin"),
    path("<date:date>", views.viewExpenses),
    path("viewMonthlyExpenses/<int:year>/<int:monthNum>", views.viewMonthlyExpenses, name="viewMonthlyExpenses"),
    path("viewYearlyExpenses/<int:year>", views.viewYearlyExpenses, name="viewYearlyExpenses"),
    path("changemonth", views.changeMonth, name="changeMonth"),
    path("expense/edit/<int:id>",views.editExpense, name="editExpense"),
    path("expense/add",views.newExpense, name="addExpense"),
    path("category",views.viewCategories, name="categories"),
    path("category/add",views.newCategory, name="addCategory"),
    path("category/edit/<str:name>",views.editCategory, name="editCategory"),
    path("pools", views.moneyPools, name="moneyPools"),
    path("pools/<int:poolId>/expenses", views.viewPoolExpenses, name="viewPoolExpenses"),
    path("pools/edit/<int:poolId>", views.editPool, name="editPool"),
    path("pools/add", views.addPool, name="addPool"),
]