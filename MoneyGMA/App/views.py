from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Sum
from django.shortcuts import redirect, render
import Api.views as api
from datetime import date, datetime, timedelta
from .forms import * 
import json
from Api.serializers import *
import hashlib
from decimal import *

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
    totalSum = Decimal(0)
    moneyPerCategory = dict()
    for i in expenses:
        totalSum+=Decimal(i["money"])
        if i["category"] in moneyPerCategory:
            moneyPerCategory[i["category"]]["percent"]+=Decimal(i["money"])
            
        else:
            if i["category"]==None:
                color = "#E0D8B0"
            else:
                color = ExpenseCategory.objects.get(pk=i["category"]).color
            moneyPerCategory[i["category"]] = {"percent":Decimal(i["money"]), "color":color}
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
def IsLogged(request):
    if "logged" in request.session and request.session["logged"]==True:
        return True
    else:
        request.session["logged"]=False
        return False
def HandleNonLog(request):
    request.session["logged"]=False
    return redirect("login")


#VIEWS

def login(request):
    if IsLogged(request):
        return redirect("index")
    else:
        template = "login.html"
        context = {}
        return render(request, template, context)

def unlog(request):
    request.session["logged"]=False
    return redirect("login")

def handleLogin(request):
    if request.method == "POST":
        password = request.POST.get("pass","")
        if hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855":
            request.session["logged"]=True
            return redirect("index")
    return redirect("login")


def index(request):
    print(IsLogged(request))
    if not IsLogged(request):
        return HandleNonLog(request)
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
    month = datetime.strptime(str(monthNum), "%m")
    context = viewData(); context["viewShortTitle"]="MoneyGMA"; context["viewTitle"]="Expenses "+month.strftime("%B")
    return partiallyViewExpenses(request, expenses, context)

def viewYearlyExpenses(request, year):
    template = "viewYearlyExpenses.html"
    monthlyData = []
    monthlylabels = []
    for monthNum in range(1,13):
        monthlyExpenses = Expense.objects.filter(date__year=year,date__month=monthNum).aggregate(Sum("money"))["money__sum"]
        if monthlyExpenses == None:
            monthlyExpenses = 0
        monthlyData.append(monthlyExpenses)
        monthlylabels.append(monthNum)
    categoryLabels = [tp[0] for tp in list(ExpenseCategory.objects.values_list("type"))]; categoryLabels.insert(0,None)
    categoryData = [Expense.objects.filter(category=cat).aggregate(Sum("money"))["money__sum"] if Expense.objects.filter(category=cat).aggregate(Sum("money"))["money__sum"]!=None else 0 for cat in categoryLabels]
    categoryLabels[0] = "None"
    context = viewData(); context["viewShortTitle"]="Yearly expenses"; context["viewTitle"]="YearlyExpenses"
    context["monthlyData"] = monthlyData
    context["monthlylabels"] = monthlylabels
    context["categoryData"] = categoryData
    context["categorylabels"] = categoryLabels
    return render(request, template, context)

def viewYearExpenses(request):
    return viewYearlyExpenses(request, date.today().year)

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
            #Delete expense
            if "deleteInstance" in request.POST:
                instance = form.save()
                instance.delete()
            #Edit expense
            else:
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
        context = viewData();context["viewShortTitle"]="Expenses"; context["formSubmit"]="Edit"; context["viewTitle"]="Editing expense "+expense.description
        form = ExpenseForm(instance=expense, id=id)
        context["form"] = form
        context["editing"] = True
        return render(request, 'expensesForm.html', context=context)

def viewCategories(request):
    template = "viewCategories.html"
    context = viewData(); context["viewShortTitle"]="Categories"; context["viewTitle"]="Categories"
    categories = ExpenseCategory.objects.all()
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
            #Delete
            if "deleteInstance" in request.POST:
                instance = form.save()
                instance.delete()
            #Edit
            else:
                form.save()
            return redirect("categories")
        else:
            return JsonResponse(form.errors)
    else:
        try:
            category = ExpenseCategory.objects.get(pk=name)
        except ExpenseCategory.DoesNotExist:
            return redirect("viewCategories")
        context = viewData();context["viewShortTitle"]="Categories"; context["formSubmit"]="Edit"; context["viewTitle"]="Edit category "+category.type
        form = ExpenseCategoryForm(instance=category)
        context["form"] = form
        return render(request, 'baseTemplates/genericForm.html', context=context)

def moneyPools(request):
    template = "moneyPools.html"
    context = viewData(); context["viewShortTitle"]="Money Pools"; context["viewTitle"]="Money Pools"
    pools = (MoneyPool.objects.all())
    context["pools"] = pools
    context["editing"] = True
    return render(request, template, context)

def viewPoolExpenses(request, poolId):
        context = viewData(); context["viewShortTitle"]="View pool Expenses"; context["viewTitle"]="Viewing Expenses From Pool "
        try:
            pool = MoneyPool.objects.get(pk=poolId)
            expenses = pool.expenses.all()
            for expense in expenses:
                expense["date"] = str(expense["date"])
            context["viewTitle"] += pool.name
            return partiallyViewExpenses(request,expenses,context)
        except MoneyPool.DoesNotExist:
            return redirect("viewCategories")

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
            #Delete
            if "deleteInstance" in request.POST:
                instance = form.save()
                instance.delete()
            #Edit
            else:
                instance = form.save()
            return redirect("moneyPools")
        else:
            return JsonResponse(form.errors)
    else:
        try:
            pool = MoneyPool.objects.get(pk=poolId)
        except MoneyPool.DoesNotExist:
            return redirect("moneyPools")
        context = viewData();context["viewShortTitle"]="MoneyPools"; context["formSubmit"]="Edit"; context["viewTitle"]="Editing Pool "+pool.name
        form = MoneyPoolForm(instance=pool)
        context["form"] = form
        context["editing"] = True
        return render(request, 'baseTemplates/genericForm.html', context=context)