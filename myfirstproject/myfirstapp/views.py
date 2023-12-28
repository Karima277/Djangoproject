from django.shortcuts import render


def home(request):
    return render(request, 'myfirstapp/index.html')

def signup(request):
    return render(request, 'myfirstapp/signup.html')

def login(request):
    return render(request, 'myfirstapp/login.html')
