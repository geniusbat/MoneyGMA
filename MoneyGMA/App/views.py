from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import Api.views as api
from datetime import date, datetime, timedelta
from .forms import * 
import json
from Api.serializers import *
from django.shortcuts import get_object_or_404

#AUXILIAR
def viewData()->dict:
    d = dict()
    d["viewShortTitle"]=""
    d["viewTitle"]=""
    d["formSubmit"]=""
    return d
def getMonthlyExpenses(monthNum):
    expenses = Expense.objects.filter(date__month=monthNum)
    serializer = ExpenseSerializer(expenses, many=True)
    return JsonResponse(serializer.data, safe=False).content
def getExpensesContext(expenses, date):
    context = {}
    totalSum = 0
    moneyPerCategory = dict()
    for i in expenses:
        totalSum+=i["money"]
        if i["category"] in moneyPerCategory:
            moneyPerCategory[i["category"]]["percent"]+=i["money"]
            
        else:
            if i["category"]==None:
                color = "#808080"
            else:
                color = ExpenseCategory.objects.get(pk=i["category"]).color
            moneyPerCategory[i["category"]] = {"percent":i["money"], "color":color}
    for i in moneyPerCategory:
        moneyPerCategory[i]["expended"]=moneyPerCategory[i]["percent"]
        moneyPerCategory[i]["percent"]=(moneyPerCategory[i]["percent"]*100)/totalSum
    context["moneyPerCategory"] = moneyPerCategory
    context["expenses"] = expenses
    context["prettyDate"] = datetime.strftime(date,"%B, %Y")
    context["date"]= date
    context["month"] = date.month
    context["totalExpended"]=totalSum
    return context


#VIEWS

def index(request):
    template = "index.html"
    context = viewData(); context["viewShortTitle"]="MoneyGMA"; context["viewTitle"]="MoneyGMA"
    expenses = json.loads(getMonthlyExpenses(date.today().month))
    context = context | getExpensesContext(expenses, date.today())
    return render(request, template, context)

def changeMonth(request):
    if request.method == "POST":
        template = "index.html"
        context = viewData(); context["viewShortTitle"]="MoneyGMA"; context["viewTitle"]="MoneyGMA"
        aux = request.POST.get("currentDate", date.today())
        currentDate = datetime.strptime(aux, '%Y-%m-%d').date()
        if "datePager-right" in request.POST:
            currentDate = currentDate + timedelta(1*365/12)
        else:
            currentDate = currentDate - timedelta(1*365/12)
        expenses = json.loads(getMonthlyExpenses(currentDate.month))
        context = context | getExpensesContext(expenses, currentDate)
        dateAsString = currentDate.strftime('%d-%m-%Y')
        return HttpResponseRedirect("/"+dateAsString)
    else:
        return redirect("index")

def viewExpenses(request, date:datetime):
    template = "index.html"
    context = viewData(); context["viewShortTitle"]="MoneyGMA"; context["viewTitle"]="MoneyGMA"
    expenses = json.loads(getMonthlyExpenses(date.month))
    context = context | getExpensesContext(expenses, date)
    return render(request, template, context)

def viewMonthlyExpenses(request, monthNum):
    expenses = json.loads(getMonthlyExpenses(monthNum))
    context = viewData(); context["viewShortTitle"]="MoneyGMA"; context["viewTitle"]="MoneyGMA"
    context["viewing"] = "This month's expenses"
    return partiallyViewExpenses(request, expenses, context)

def partiallyViewExpenses(request, expenses, context):
    template = "partiallyViewExpenses.html"
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
        try:
            expense = Expense.objects.get(pk=id)
        except Expense.DoesNotExist:
            return redirect("index")
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            return JsonResponse(form.errors)
    else:
        try:
            expense = Expense.objects.get(pk=id)
        except Expense.DoesNotExist:
            return redirect("index")
        context = viewData();context["viewShortTitle"]="Expenses"; context["formSubmit"]="Edit"; context["viewTitle"]="Edit expense"
        form = ExpenseForm(instance=expense)
        context["form"] = form
        return render(request, 'baseTemplates/genericForm.html', context=context)

def viewCategories(request):
    template = "viewCategories.html"
    context = viewData(); context["viewShortTitle"]="Categories"; context["viewTitle"]="Categories"
    categories = list(ExpenseCategory.objects.all().values())
    context["categories"] = categories
    return render(request, template, context)

def newCategory(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories")
    else:
        context = viewData();context["viewShortTitle"]="Categories"; context["formSubmit"]="Create Category"; context["viewTitle"]="Create a new category"
        form = ExpenseCategoryForm()
        context["form"] = form
        #return render(request, 'testForm.html', {'form': form})
        return render(request, 'baseTemplates/genericForm.html', context=context)

def editCategory(request, name):
    if request.method == 'POST':
        try:
            category = ExpenseCategory.objects.get(pk=name)
        except ExpenseCategory.DoesNotExist:
            return redirect("viewCategories")
        form = ExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories")
        else:
            return JsonResponse(form.errors)
    else:
        try:
            category = ExpenseCategory.objects.get(pk=name)
        except ExpenseCategory.DoesNotExist:
            return redirect("viewCategories")
        context = viewData();context["viewShortTitle"]="Categories"; context["formSubmit"]="Edit"; context["viewTitle"]="Edit category"
        form = ExpenseCategoryForm(instance=category)
        context["form"] = form
        return render(request, 'baseTemplates/genericForm.html', context=context)