from django.shortcuts import redirect, render
import Api.views as api
from django.utils import timezone
from .forms import * 

def viewData()->dict:
    d = dict()
    d["viewShortTitle"]=""
    d["viewTitle"]=""
    d["formSubmit"]=""
    return d

def index(request):
    template = "index.html"
    context = viewData(); context["viewShortTitle"]="MoneyGMA"; context["viewTitle"]="MoneyGMA"
    expenses = api.getMonthlyExpenses(request, timezone.now().month)
    context["expenses"] = expenses
    return render(request, template, context)

def newExpense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        context = viewData();context["viewShortTitle"]="Expenses"; context["formSubmit"]="Add"; context["viewTitle"]="Add new expense"
        form = ExpenseForm()
        context["form"] = form
        #return render(request, 'testForm.html', {'form': form})
        return render(request, 'baseTemplates/genericForm.html', context=context)

def editExpense(request, id):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        Expense.objects.get_object_or_404(pk=id)
        context = viewData();context["viewShortTitle"]="Expenses"; context["formSubmit"]="Edit"; context["viewTitle"]="Edit expense"
        form = ExpenseForm()
        context["form"] = form
        return render(request, 'baseTemplates/genericForm.html', context=context)

def newCategory(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        context = viewData();context["viewShortTitle"]="Categories"; context["formSubmit"]="Create Category"; context["viewTitle"]="Create a new category"
        form = ExpenseCategoryForm()
        context["form"] = form
        #return render(request, 'testForm.html', {'form': form})
        return render(request, 'baseTemplates/genericForm.html', context=context)

def editCategory(request, id):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        ExpenseCategory.objects.get_object_or_404(pk=id)
        context = viewData();context["viewShortTitle"]="Categories"; context["formSubmit"]="Edit"; context["viewTitle"]="Edit category"
        form = ExpenseCategoryForm()
        context["form"] = form
        #return render(request, 'testForm.html', {'form': form})
        return render(request, 'baseTemplates/genericForm.html', context=context)