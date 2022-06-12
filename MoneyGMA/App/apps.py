from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'

    
    def ready(self) -> None:
        post_migrate.connect(AutoCreateInstances,sender=self)
        return super().ready()
    
#Autocreate some categories
def AutoCreateInstances(sender, **kwargs):
    categories = {
        "groceries" : {"description":"Money expended on groceries, such as food, cleaning...","color":"#B4EDD2"},
        "transport" : {"description":"Money expended on gasoline and public transport","color":"#9A7AA0"},
        "restaurants" : {"description":"Eating in restaurants and ordering food","color":"#EAF27C"},
        "hobbies" : {"description":"Expenses related to hobbies and entertainment","color":"#F4C095"},
    }
    from .models import ExpenseCategory
    for category in categories:
        if not ExpenseCategory.objects.filter(type=category).exists():
            instance = ExpenseCategory(type=category, description=categories[category]["description"], color=categories[category]["color"])
            instance.save()
