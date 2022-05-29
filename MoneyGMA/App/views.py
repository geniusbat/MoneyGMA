from django.shortcuts import redirect, render
from .forms import * 

def viewData()->dict:
    d = dict()
    d["viewShortTitle"]=""
    d["viewTitle"]=""
    d["formSubmit"]=""
    return d

def index(request):
    template = "index.html"
    context = {}
    return render(request, template, context)

def form(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            return redirect("index")
    else:
        context = viewData();context["viewTitle"]="Categories"; context["formSubmit"]="Create Category"; context["viewTitle"]="Create a new category"
        form = ExpenseCategoryForm()
        context["form"] = form
        #return render(request, 'testForm.html', {'form': form})
        return render(request, 'baseTemplates/genericForm.html', context=context)