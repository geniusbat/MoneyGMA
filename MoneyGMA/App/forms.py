from dataclasses import fields
from django import forms
from .models import *

class ExpenseCategoryForm(forms.ModelForm):
    color = forms.CharField(label='Color for category', max_length=7, widget=forms.TextInput(attrs={'type': 'color'}))
    class Meta:
        model = ExpenseCategory
        fields = "__all__"





class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"