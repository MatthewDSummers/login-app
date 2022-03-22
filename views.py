from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from quote_dash_app.models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register_user(request):
    errors = User.objects.validator(request.POST)

    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        request.session['message_status'] = "error"
        return redirect('/')
        
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        messages.info(request, "Welcome to the User Registration and Login app!  Please login! ")
        request.session['message_status'] = "success"

    return redirect('/')

def login(request):
    try:
        user = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, "Incorrect email address or password")
        return redirect('/')
    
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        request.session['user_first_name'] = user.first_name
        request.session['user_last_name'] = user.last_name
        request.session['user_email'] = user.email
        return redirect('/quotes')
    
    messages.error(request, "Incorrect email address or password")

    return redirect('/')

def logout(request):
    # request.sessions.clear()
    # the above would work, but the below is specific (maybe I don't wanna end ALL sessions)
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_first_name' in request.session:
        del request.session['user_first_name']
    if 'user_last_name' in request.session:
        del request.session['user_last_name']
    if 'user_email' in request.session:
        del request.session['user_email']
    
    return redirect('/')


def profile(request, quote_user_id):
    user = User.objects.get(id=request.session['user_id'])
    poster = User.objects.get(id=quote_user_id)
    context = {
        'all_quotes':poster.quotes.all(),
        'poster':poster,
        'user':user
    }
    return render(request, 'profile.html', context)

def delete_quote(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    quote.delete()
    return redirect('/quotes')

def edit_page(request, user_id):
    user_id = request.session['user_id']

    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request,'edit.html', context)

def update_user(request, user_id):
    errors = User.objects.update_validator(request.POST)
    user = User.objects.get(id=user_id)

    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        request.session['message_status'] = "error"
        return redirect(f'/myaccount/{user.id}')

    else:
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.email=request.POST['email']
        user.save()
        messages.info(request, "Thanks for updating your info!")
        request.session['message_status'] = "success"

        return redirect(f'/myaccount/{user.id}')