# Generated by Django 4.0.4 on 2022-06-10 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_alter_expense_options_alter_expensecategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneypool',
            name='expenses',
            field=models.ManyToManyField(blank=True, null=True, to='App.expense'),
        ),
    ]
