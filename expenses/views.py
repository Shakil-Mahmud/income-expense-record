from django.shortcuts import render

import expenses

# Create your views here.
def index(request):
    return render(request, 'expenses/index.html')

def add_expense(request):
    return render(request, 'expenses/add_expense.html')