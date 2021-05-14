from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    return redirect('/')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['pw']):
        messages.error(request, "Invalid email/password")
        return redirect('/')
    user = User.objects.get(email= request.POST['email'])
    request.session['userid'] = user.id
    return redirect("/books")

def register(request):
    return render(request, "register.html")

def signup(request):
    if request.method == "GET":
        return redirect('/register')
    errors = User.objects.validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        new_user = User.objects.register(request.POST)
        request.session['userid'] = new_user.id
        return redirect("/books")

def dummi_login(request):
    request.session['userid'] = 0
    return redirect("/books")