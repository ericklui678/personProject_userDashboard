from django.shortcuts import render, redirect
from django.contrib import messages
from models import *

def index(request):
    print User.objects.all()
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
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    user = User.objects.get(email=postData['email'])
    request.session['id'] = user.id
    request.session['name'] = user.first_name
    return redirect('/dashboard')

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

    context = {
        'curr_user': User.objects.get(id=request.session['id']),
        'users': User.objects.all()
    }

    return render(request, 'dashboard/dashboard.html', context)

def user_logoff(request):
    del request.session['id']
    del request.session['name']

    return redirect('/')

def user_edit(request, id):
    # If logged on user is not an admin, redirect back to dashboard
    if (User.objects.get(id=request.session['id']).admin_level == False):
        return redirect('/dashboard')

    context = {'user': User.objects.get(id=id)}

    return render(request, 'dashboard/edit_user.html', context)

def update(request, id):
    errors = {}
    if 'change_info' in request.POST:
        if request.POST['admin_level'] == '1':
            admin_level = True
        else:
            admin_level = False

        postData = {
            'email': request.POST['email'].lower(),
            'first_name': request.POST['first_name'].title(),
            'last_name': request.POST['last_name'].title(),
            'admin_level': admin_level,
            'prev_email': User.objects.get(id=id).email,
        }
        errors = User.objects.validate_info(postData)

    elif 'change_pw' in request.POST:
        postData = {
            'password': request.POST['password'],
            'confirm': request.POST['confirm'],
            'prev_email': User.objects.get(id=id).email,
        }
        errors = User.objects.validate_password(postData)

    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
            print error
        return redirect('/users/edit/' + id)

    return redirect('/dashboard')

def profile(request):
    context = {'user': User.objects.get(id=request.session['id'])}
    print context['user'].description
    return render(request, 'dashboard/profile.html', context)

def profile_update(request):
    errors = {}
    if 'change_info' in request.POST:
        postData = {
            'email': request.POST['email'].lower(),
            'first_name': request.POST['first_name'].title(),
            'last_name': request.POST['last_name'].title(),
            'description': request.POST['description'],
            'prev_email': User.objects.get(id=request.session['id']).email,
        }
        print postData
        errors = User.objects.validate_profile(postData)

    elif 'change_pw' in request.POST:
        postData = {
            'password': request.POST['password'],
            'confirm': request.POST['confirm'],
            'prev_email': User.objects.get(id=request.session['id']).email,
        }
        errors = User.objects.validate_password(postData)

    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
            print error
        return redirect('/users/profile/update')

    return redirect('/dashboard')
