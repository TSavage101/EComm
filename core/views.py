from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request, *args, **kwargs):
    
    if request.user.username == '':
        return render(request, 'index.html', {})
    else:
        current_user = User.objects.get(username=request.user.username)
        
        context = {
            'current_user': current_user,
        }
        
        return render(request, 'index.html', context)

def authe(request, *args, **kwargs):
    
    if request.method == 'POST':
        if 'semail' in request.POST:
            name = request.POST['name']
            email = request.POST['semail']
            tel = request.POST['tel']
            password = request.POST['spassword']
            
            if User.objects.filter(email=email).exists():
                messages.info(request, 'This account already exists.')
                return redirect('auth')
            else:
                new_user = User.objects.create_user(username=name, email=email, password=password)
                new_user.save()
                
                user = auth.authenticate(username=name, email=email, password=password)
                auth.login(request, user)
                return redirect('home')
            
        else:
            email = request.POST['email']
            password = request.POST['password']
            
            the_username = User.objects.get(email=email).username
            
            user = auth.authenticate(username=the_username, email=email, password=password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'This account does not exists.')
    else:
        return render(request, 'auth.html', {})

@login_required(login_url='auth')
def logout(request, *args, **kwargs):
    auth.logout(request)
    return redirect('auth')

def cart(request, *args, **kwargs):
    return render(request, 'cart.html', {})

def product(request, *args, **kwargs):
    return render(request, 'product.html', {})

def productdetails(request, *args, **kwargs):
    return render(request, 'productdetails.html', {})
