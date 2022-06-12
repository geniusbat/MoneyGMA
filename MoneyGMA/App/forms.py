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
    def __init__(self, *args, **kwargs):
        if "id" in kwargs:
            self.id = kwargs.pop("id")
            super(ExpenseForm, self).__init__(*args, **kwargs)
            self.fields["pools"] = forms.ModelMultipleChoiceField(queryset=MoneyPool.objects.all(), required=False, initial=MoneyPool.objects.filter(expenses__in=[self.id]).values_list('id', flat=True))
        else:
            super(ExpenseForm, self).__init__(*args, **kwargs)
            self.fields["pools"] = forms.ModelMultipleChoiceField(queryset=MoneyPool.objects.all(), required=False)
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y'],
        widget=DatePickerInput(),
        initial=date.today
        )
    class Meta:
        model = Expense
        fields = "__all__"


class MoneyPoolForm(forms.ModelForm):
    class Meta:
        model = MoneyPool
        fields = "__all__"
        #fields = ["money", "description", "name"]