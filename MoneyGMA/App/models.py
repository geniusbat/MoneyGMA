from django.db import models
from datetime import date, datetime
from colorfield.fields import ColorField

class ExpenseCategory(models.Model):
    type = models.CharField("Type", max_length=20, primary_key=True)
    description = models.CharField("Description", max_length=100)
    color = ColorField("Color for category", format="hex", default='#FF0000')

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural =("Categories")
        ordering = ['type']

    def __str__(self):
        return self.type


class Expense(models.Model):
    date = models.DateField("Date","date", default=datetime.now)
    description = models.CharField("Description", max_length=90, blank=True, default="")
    category = models.ForeignKey(ExpenseCategory, to_field="type", on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    money = models.FloatField("Money expended", default=0.0)

    class Meta:
        ordering = ['date']
        verbose_name = ("Expense")
        verbose_name_plural =("Expenses")

    def __str__(self):
        return str(self.description) + " " + str(self.money)  + "$ " + datetime.strftime(self.date, "%d %B, %Y")

class MoneyPool(models.Model):
    name = models.CharField("Name", max_length=15)
    description = models.CharField("Description", max_length=90, blank=True, default="")
    money = models.IntegerField("Pool of Money")
    expenses = models.ManyToManyField(Expense, blank=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name + ": " + self.description