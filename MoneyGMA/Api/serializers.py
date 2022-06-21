from App.models import *
from rest_framework import serializers


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class MoneyPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyPool
        fields = '__all__'