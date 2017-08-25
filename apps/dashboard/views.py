from django.shortcuts import render, redirect
from django.contrib import messages
from models import *

def index(request):
    print User.objects.all()
    return render(request, 'dashboard/index.html')

def user_create(request):
    postData = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'confirm': request.POST['confirm'],
    }
    errors = User.objects.validate_register(postData)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)

    return redirect('/')
