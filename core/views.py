from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Avg, Sum

from .models import Product, Rating, Number, Feedback, Cart, Cart_item

import math

# Create your views here.
def home(request, *args, **kwargs):
    
    if request.user.username == '':
        return render(request, 'index.html', {})
    else:
        current_user = User.objects.get(username=request.user.username)
        
        all_products = Product.objects.all()
        sbrating = Product.objects.order_by('-rating')[:3]
        sbsales = Product.objects.order_by('-sales')[:3]
        sbdate = Product.objects.order_by('-date')[:8]
        
        context = {
            'current_user': current_user,
            'all_products': all_products,
            'sbsales': sbsales,
            'sbrating': sbrating,
            'sbdate': sbdate,
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
                
                new_cart = Cart.objects.create(user=name)
                new_cart.save()
                
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

@login_required(login_url='auth')
def cart(request, *args, **kwargs):
    return render(request, 'cart.html', {})

def products(request, pn, *args, **kwargs):
    all_products = Product.objects.all()
    value = 'Default'
    
    if request.method == 'POST':
        value = request.POST['order']
        
        if value == 'Price':
           all_products = Product.objects.order_by('-price')
        elif value == 'Popularity':
            all_products = Product.objects.order_by('-sales')
        elif value == 'Ratings':
            all_products = Product.objects.order_by('-rating')
        else:
            all_products = Product.objects.order_by('-date')
            
    chunks = [all_products[x:x+16] for x in range(0, len(all_products), 16)]
    
    nop = math.ceil(len(all_products)/16)
    plist = []
    
    for p in range(1, nop+1):
        plist.append(p)
    
    try:
        final_plist = chunks[pn - 1]
    except:
        return redirect('error')
    
    context = {
        'list': final_plist,
        'plist': plist,
        'value': value,
    }
    
    return render(request, 'product.html', context)

def productdetails(request, pk, *args, **kwargs):
    
    if request.method == 'POST':
        rating = request.POST['rating']
        number = request.POST['number']
        feedback = request.POST['feedback']
        
        product = Product.objects.get(pk=pk)
        
        if rating != 'default':
            new_rating = Rating.objects.create(user=request.user.username, rating=rating, product=product.name)
        else:
            new_rating = Rating.objects.create(user=request.user.username, rating=rating, product=product.name)
        
        if int(number) > 0:
            new_number = Number.objects.create(user=request.user.username, number=number, product=product.name)
        else:
            messages.info(request, 'The number entered is negative!')
            return redirect('productdetails')
        
        if feedback != '':
            new_feedback = Feedback.objects.create(user=request.user.username, feedback=feedback, product=product.name)
        
        new_rating.save()
        new_number.save()
        new_feedback.save()
        
        rating_number = Rating.objects.filter(product=product.name).aggregate(Avg('rating'))
        product.rating = rating_number
        print(rating_number)
        
        number_number = Rating.objects.filter(product=product.name).aggregate(Sum('rating'))
        product.sales = number_number
        print(number_number)
        
        new_cart_item = Cart_item.objects.create(user=request.user.username, product=product.name)
        new_cart_item.save()
        
        user_cart = Cart.objects.get(user=request.user.username)
        cil = Cart_item.objects.filter(user=request.user.username)
        
        count = 0
        
        for i in cil:
            count += 1
            
        user_cart.number = count
        
        return redirect('productdetails/' + pk)
        
    else:
        product = Product.objects.get(pk=pk)
        related = Product.objects.filter(type=product.type)
        cart_items = Cart_item.objects.filter(user=request.user.username, product=product.name)
        
        if len(cart_items) == 0:
            ici = False
        else:
            ici = True
        
        return render(request, 'productdetails.html', {'product': product, 'related': related, 'ici': ici})

def error(request, *args, **kwargs):
    return render(request, 'error.html', {})

def productsa(request, pn, type, *args, **kwargs):
    all_products = Product.objects.filter(type=type)
    value = 'Default'
    
    if request.method == 'POST':
        value = request.POST['order']
        
        if value == 'Price':
           all_products = Product.objects.filter(type=type).order_by('-price')
        elif value == 'Popularity':
            all_products = Product.objects.filter(type=type).order_by('-sales')
        elif value == 'Ratings':
            all_products = Product.objects.filter(type=type).order_by('-rating')
        else:
            all_products = Product.objects.filter(type=type).order_by('-date')
            
    chunks = [all_products[x:x+16] for x in range(0, len(all_products), 16)]
    
    nop = math.ceil(len(all_products)/16)
    plist = []
    
    for p in range(1, nop+1):
        plist.append(p)
    
    try:
        final_plist = chunks[pn - 1]
    except:
        return redirect('error')
    
    context = {
        'list': final_plist,
        'plist': plist,
        'value': value,
        'type': type,
    }
    
    return render(request, 'producta.html', context)
