from django.db import models
from django.utils import timezone
from colorfield.fields import ColorField

class ExpenseCategory(models.Model):
    type = models.CharField("Type", max_length=20)
    description = models.CharField("Description", max_length=100)
    color = ColorField("Color for category", format="hex", default='#FF0000')

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural =("Categories")

    def __str__(self):
        return self.type



class Expense(models.Model):
    date = models.DateTimeField("Date","date", default=timezone.now())
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    money = models.FloatField("Money expended", default=0.0)

    class Meta:
        verbose_name = ("Expense")
        verbose_name_plural =("Expenses")

    def __str__(self):
        return self.date
