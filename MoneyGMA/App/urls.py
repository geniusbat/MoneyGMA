from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("expense/edit/<int:id>",views.editExpense),
    path("expense/add",views.newExpense),
    path("category/add",views.newCategory),
    path("category/edit/<int:id>",views.editCategory),
]