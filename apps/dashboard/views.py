from django.shortcuts import render, redirect
from django.contrib import messages
from models import *

def index(request):
    if request.session.get('id') != None:
        return redirect('/dashboard')

    return render(request, 'dashboard/index.html')

def user_create(request):
    postData = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'].lower(),
        'password': request.POST['password'],
        'confirm': request.POST['confirm'],
    }
    errors = User.objects.validate_register(postData)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)

    return redirect('/')

def user_login(request):
    postData = {
        'email': request.POST['email'].lower(),
        'password': request.POST['password'],
    }
    errors = User.objects.validate_login(postData)
    print errors
    if len(errors) == 0:
        user = User.objects.get(email=postData['email'])
        request.session['id'] = user.id
        request.session['name'] = user.first_name
        return redirect('/dashboard')

    return redirect('/')

def dashboard(request):
    if request.session.get('id') == None:
        return redirect('/')

    return render(request, 'dashboard/dashboard.html')

def user_logoff(request):
    del request.session['id']
    del request.session['name']
    return redirect('/')
