from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import Api.views as api
from datetime import date, datetime, timedelta
from .forms import * 
import json
from Api.serializers import *
from django.shortcuts import get_object_or_404

#TODO: Error, from 01-05-2022 goes to 31-05-2022 (does not skip month)

#AUXILIAR
def viewData()->dict:
    d = dict()
    d["viewShortTitle"]=""
    d["viewTitle"]=""
    d["formSubmit"]=""
    return d
def getMonthlyExpenses(year, monthNum):
    expenses = Expense.objects.filter(date__year=year,date__month=monthNum)
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
                color = "#E0D8B0"
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
    context["year"] = date.year
    context["month"] = date.month
    context["totalExpended"]=totalSum
    return context


#VIEWS

def index(request):
    template = "index.html"
    context = viewData(); context["viewShortTitle"]="MoneyGMA"; context["viewTitle"]="MoneyGMA"
    expenses = json.loads(getMonthlyExpenses(date.today().year, date.today().month))
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
        expenses = json.loads(getMonthlyExpenses(date.today().year, currentDate.month))
        context = context | getExpensesContext(expenses, currentDate)
        dateAsString = currentDate.strftime('%d-%m-%Y')
        return HttpResponseRedirect("/"+dateAsString)
    else:
        return redirect("index")

def viewExpenses(request, date:datetime):
    template = "index.html"
    context = viewData(); context["viewShortTitle"]="MoneyGMA"; context["viewTitle"]="MoneyGMA"
    expenses = json.loads(getMonthlyExpenses(date.year, date.month))
    context = context | getExpensesContext(expenses, date)
    return render(request, template, context)

def viewMonthlyExpenses(request, year, monthNum):
    expenses = json.loads(getMonthlyExpenses(year, monthNum))
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
            instance = form.save()
            for poolId in form["pools"].value():
                pool = MoneyPool.objects.get(pk=poolId)
                pool.expenses.add(Expense.objects.all().get(pk=instance.id))
            return redirect("index")
    else:
        context = viewData();context["viewShortTitle"]="Expenses"; context["formSubmit"]="Add"; context["viewTitle"]="Add new expense"
        form = ExpenseForm()
        context["form"] = form
        #return render(request, 'testForm.html', {'form': form})
        return render(request, 'expensesForm.html', context=context)

def editExpense(request, id):
    if request.method == 'POST':
        try:
            expense = Expense.objects.get(pk=id)
        except Expense.DoesNotExist:
            return redirect("index")
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            instance = form.save()
            poolIds = MoneyPool.objects.filter(expenses__in=[instance.id])
            newPoolIds = form["pools"].value()
            oldUnfound = [ins.id for ins in poolIds if ins.id not in newPoolIds]
            newUnfound = [id for id in newPoolIds if id not in poolIds]
            #Remove old
            for id in oldUnfound:
                MoneyPool.objects.all().get(pk=id).expenses.remove(instance)
            #Add new
            for id in newUnfound:
                MoneyPool.objects.all().get(pk=id).expenses.add(instance)
            return redirect("index")
        else:
            return JsonResponse(form.errors)
    else:
        try:
            expense = Expense.objects.get(pk=id)
        except Expense.DoesNotExist:
            return redirect("index")
        context = viewData();context["viewShortTitle"]="Expenses"; context["formSubmit"]="Edit"; context["viewTitle"]="Edit expense"
        form = ExpenseForm(instance=expense, id=id)
        context["form"] = form
        return render(request, 'expensesForm.html', context=context)

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

def moneyPools(request):
    template = "moneyPools.html"
    context = viewData(); context["viewShortTitle"]="Money Pools"; context["viewTitle"]="Money Pools"
    pools = list(MoneyPool.objects.all().values())
    for pool in pools:
        pool["expenses"] = list(MoneyPool.objects.get(pk=pool["id"]).expenses.values())
    context["pools"] = pools
    return render(request, template, context)


def viewPool(request, poolId):
    template = "moneyPools.html"
    context = viewData(); context["viewShortTitle"]="View pool"; context["viewTitle"]="View Pool"
    pool = MoneyPool.objects.get(pk=poolId)
    context["pool"] = pool
    return render(request, template, context)

def addPool(request):
    if request.method == 'POST':
        form = MoneyPoolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("moneyPools")
    else:
        context = viewData();context["viewShortTitle"]="Pools"; context["formSubmit"]="Create Pool"; context["viewTitle"]="Create a new pool"
        form = MoneyPoolForm()
        context["form"] = form
        return render(request, 'baseTemplates/genericForm.html', context=context)

def editPool(request, poolId):
    if request.method == 'POST':
        try:
            pool = MoneyPool.objects.get(pk=poolId)
        except MoneyPool.DoesNotExist:
            return redirect("moneyPools")
        form = MoneyPoolForm(request.POST, instance=pool)
        if form.is_valid():
            instance = form.save()
            return redirect("moneyPools")
        else:
            return JsonResponse(form.errors)
    else:
        try:
            pool = MoneyPool.objects.get(pk=poolId)
        except MoneyPool.DoesNotExist:
            return redirect("moneyPools")
        context = viewData();context["viewShortTitle"]="MoneyPools"; context["formSubmit"]="Edit"; context["viewTitle"]="Edit Pool"
        form = MoneyPoolForm(instance=pool)
        context["form"] = form
        return render(request, 'baseTemplates/genericForm.html', context=context)