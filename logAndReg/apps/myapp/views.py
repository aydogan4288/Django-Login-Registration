from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from .models import User
import bcrypt

def index(request):

    return render (request, 'myapp/index.html')

# Create your views here.
def register(request):
    print(request.POST)
    errors = User.objects.register_validator(request.POST)

    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags='register')
        return redirect('/')

    else:
        password = request.POST['password']
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name= request.POST['first_name'], last_name = request.POST['last_name'], email= request.POST['email'], password= password)
    return redirect('/success')

def success(request):
        context = {
        'users' : User.objects.all()
        }
        return render(request, 'myapp/success.html', context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    print(errors)
    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags= 'login')
        return redirect('/')

    else:
        user = User.objects.get(email=request.POST['emaillogin'])
        request.session['user_id'] = user.id
        return redirect('/logged')

def logged(request):
    context = {
    'users' : User.objects.all()
    }
    return render(request, 'myapp/logged.html')

def logout(request):
    request.session.clear()
    return redirect('/')
