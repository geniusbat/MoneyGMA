from decimal import Decimal
import json
from unicodedata import category
from django.shortcuts import redirect, render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response as response
from rest_framework import status
from django.http import Http404
from rest_framework.decorators import api_view
import django.utils.timezone
from django.http import JsonResponse

from App.models import *

#DETAILED VIEWS STOPPED WORKING

class ExpenseCategoryList(APIView):
    def get(self, request):
        categories = ExpenseCategory.objects.all()
        serializer = ExpenseCategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)

class ExpenseCategoryDetail(APIView):
    def getObject(self, id):
        try:
            return ExpenseCategory.objects.get(pk=id)
        except ExpenseCategory.DoesNotExist:
            raise Http404

    def get(self, request, id):
        category = ExpenseCategory.objects.get(pk=id)
        serializer = ExpenseCategorySerializer(category, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        serializer = ExpenseCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False)
        
    def put(self, request, id):
        category = ExpenseCategory.objects.get(pk=id)
        serializer = ExpenseCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, safe=False)

    def delete(self, request):
        pass


class ExpenseList(APIView):
    def get(self, request):
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def getMonthlyExpenses(request, monthNum):
    expenses = Expense.objects.filter(date__month=monthNum)
    serializer = ExpenseSerializer(expenses, many=True)
    return JsonResponse(serializer.data, safe=False)

class ExpenseDetail(APIView):
    def getObject(self, id):
        #print("EXPENSEDETAILAAAAAAAAAAAAAAAAAAAA")
        try:
            return Expense.objects.get(pk=id)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, id):
        #print("EXPENSEDETAILFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        #expenses = Expense.objects.get(pk=id)
        expenses = Expense.objects.filter(pk=id)[0]
        serializer = ExpenseSerializer(expenses, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False)
        
    def put(self, request, id):
        expenses = Expense.objects.get(pk=id)
        serializer = ExpenseSerializer(expenses, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False)

    def delete(self, request):
        pass


@api_view(['GET'])
def getPools(request):
    pools = MoneyPool.objects.all()
    serializer = MoneyPoolSerializer(pools, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(["POST"])
def updateExpenses(request):
    data = json.loads(request.body.decode('utf-8'))
    #print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    #print(data)
    for expense in data:
        try:
            cat = ExpenseCategory.objects.filter(type=expense["category"]).first()
        except:
            #print("Failed to find category: " + expense["category"])
            cat = None
        if cat != None:
            ins = Expense(date = datetime.strptime(expense["date"],"%Y-%m-%d"), description=expense["description"], money = Decimal(expense["money"]), category = cat)
        else: 
            ins = Expense(date = datetime.strptime(expense["date"],"%Y-%m-%d"), description=expense["description"], money = Decimal(expense["money"]))
        ins.save()
    return JsonResponse("", safe=False)


@api_view(['GET'])
def errorView(request):
    pass
