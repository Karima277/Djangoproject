from django.shortcuts import render
from .models import Travel

def home(request):
    return render(request, 'myfirstapp/index.html')

def signup(request):
    return render(request, 'myfirstapp/signup.html')

def login(request):
    return render(request, 'myfirstapp/login.html')
def travels(request):
    context={'Travels': Travel.objects.all()}
    return render(request, 'myfirstapp/travels.html',context)