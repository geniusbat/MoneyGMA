# Generated by Django 4.0.4 on 2022-10-06 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_alter_moneypool_expenses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='money',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=18, verbose_name='Money expended'),
        ),
    ]
