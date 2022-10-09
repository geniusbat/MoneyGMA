from django.urls import path
from .views import *

urlpatterns = [
    path('expensecategory', ExpenseCategoryList.as_view()), 
    path('expensecategory/<int:pk>/', ExpenseCategoryDetail.as_view()),
    path('expense', ExpenseList.as_view()), 
    path('expense/monthly/<int:monthNum>', getMonthlyExpenses), 
    path('expense/<int:pk>/', ExpenseDetail.as_view()),
    path('expense/update', updateExpenses), 
    path('pools', getPools), 
    path('errorView', errorView), 
]