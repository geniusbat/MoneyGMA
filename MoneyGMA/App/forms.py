from dataclasses import fields
from django import forms
from .models import *
from .widgets import *

class ExpenseCategoryForm(forms.ModelForm):
    color = forms.CharField(label='Color for category', max_length=7, widget=forms.TextInput(attrs={'type': 'color'}))
    class Meta:
        model = ExpenseCategory
        fields = "__all__"


class ExpenseForm(forms.ModelForm):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=DatePickerInput(),
        initial=date.today
        )
    pools = forms.ModelMultipleChoiceField(queryset=MoneyPool.objects.all())
    class Meta:
        model = Expense
        fields = "__all__"

class MoneyPoolForm(forms.ModelForm):
    class Meta:
        model = MoneyPool
        fields = "__all__"
        #fields = ["money", "description", "name"]