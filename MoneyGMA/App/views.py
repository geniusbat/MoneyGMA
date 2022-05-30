from multiprocessing import context
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import Api.views as api
from datetime import date, datetime, timedelta
from .forms import * 
import json
from Api.serializers import *

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
        if i["category"] in moneyPerCategory:
            moneyPerCategory[i["category"]]["percent"]+=i["money"]
            totalSum+=i["money"]
        else:
            if i["category"]==None:
                color = "#808080"
            else:
                color = ExpenseCategory.objects.get(pk=i["category"]).color
            moneyPerCategory[i["category"]] = {"percent":i["money"], "color":color}
            totalSum=i["money"]
    for i in moneyPerCategory:
        moneyPerCategory[i]["percent"]=(moneyPerCategory[i]["percent"]*100)/totalSum
    context["moneyPerCategory"] = moneyPerCategory
    context["expenses"] = expenses
    context["date"]= date.today()
    return context

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
        currentDate = datetime.strptime(aux, '%B %d, %Y').date()
        if "datePager-right" in request.POST:
            currentDate = currentDate + timedelta(1*365/12)
        else:
            currentDate = currentDate - timedelta(1*365/12)
        expenses = json.loads(getMonthlyExpenses(currentDate.month))
        context = context | getExpensesContext(expenses, currentDate)
        dateAsString = currentDate.strftime('%d-%m-%Y')
        return HttpResponseRedirect("/"+dateAsString)
        return render(request, template, context)
    else:
        return redirect("index")

def viewExpenses(request, date:datetime):
    template = "index.html"
    context = viewData(); context["viewShortTitle"]="MoneyGMA"; context["viewTitle"]="MoneyGMA"
    expenses = json.loads(getMonthlyExpenses(date.month))
    totalSum = 0
    moneyPerCategory = dict()
    for i in expenses:
        if i["category"] in moneyPerCategory:
            moneyPerCategory[i["category"]]["percent"]+=i["money"]
            totalSum+=i["money"]
        else:
            if i["category"]==None:
                color = "#808080"
            else:
                color = ExpenseCategory.objects.get(pk=i["category"]).color
            moneyPerCategory[i["category"]] = {"percent":i["money"], "color":color}
            totalSum=i["money"]
    for i in moneyPerCategory:
        moneyPerCategory[i]["percent"]=(moneyPerCategory[i]["percent"]*100)/totalSum
    context["moneyPerCategory"] = moneyPerCategory
    context["expenses"] = expenses
    context["date"]= date
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