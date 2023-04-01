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
        all_products = Product.objects.all()
        sbrating = Product.objects.order_by('-rating')[:3]
        sbsales = Product.objects.order_by('-sales')[:3]
        sbdate = Product.objects.order_by('-date')[:8]
        
        context = {
            'all_products': all_products,
            'sbsales': sbsales,
            'sbrating': sbrating,
            'sbdate': sbdate,
        }
        
        return render(request, 'index.html', context)
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
    users_cart = Cart.objects.get(user=request.user.username)
    users_cart_items = Cart_item.objects.filter(user=request.user.username)
    
    subtotal_price = 0
    total_price = 0
    
    uci = []
    ucin = []
    
    for b in users_cart_items:
        gpr = Product.objects.get(name=b.product)
        gpr.commission = 0.07 * float(gpr.price)
        gpr.save()
    
    for a in users_cart_items:
        gp = Product.objects.get(name=a.product)
        ucinum = Number.objects.filter(user=request.user.username, product=a.product).first()
        uci.append((gp))
        ucin.append((ucinum))
    
    commission = 200
    
    il = []
    
    for i in users_cart_items:
        get_product = Product.objects.get(name=i.product)
        uci_num = Number.objects.filter(user=request.user.username, product=i.product).first()
        subtotal_price = float(get_product.price) * float(uci_num.number)
        il.append(subtotal_price)
    
    stp = 0
    
    for price in il:
        stp += price
        comm = 0.7 * float(price)
        total_price = float(stp) + (float(comm) * len(il))
    
    context = {
        'users_cart': users_cart,
        'users_cart_items': users_cart_items,
        'total_price': total_price,
        'uci': uci,
        'ucin': ucin,
        'commission': commission,
        'subtotal_price': subtotal_price,
    }
    
    return render(request, 'cart.html', context)

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
        context = {
            'list': final_plist,
            'plist': plist,
            'value': value,
        }
        
        return render(request, 'product.html', context)
    
    context = {
        'list': final_plist,
        'plist': plist,
        'value': value,
    }
    
    return render(request, 'product.html', context)

def productdetails(request, pk, *args, **kwargs):
    
    if request.method == 'POST':
        if 'seecomments' in request.POST:
            return redirect('/comments/' + str(pk))
        
        if request.user.username != '':
            if 'rating' in request.POST:
                rating = request.POST.get('rating')

                product = Product.objects.get(pk=pk)
                
                if Rating.objects.filter(user=request.user.username, product=product.name).exists():
                    r = Rating.objects.get(user=request.user.username, product=product.name)
                    r.rating = rating
                    r.save()
                    
                    if Feedback.objects.filter(user=request.user.username, product=product.name).exists():
                        f = Feedback.objects.get(user=request.user.username, product=product.name)
                        f.rating = rating
                        f.save()
                    
                    rating_number = Rating.objects.filter(product=product.name).aggregate(Avg('rating'))['rating__avg']
                    product.arating = rating_number
                    product.rating = round(rating_number)
                    
                    product.save()
                    
                    return redirect('./' + str(pk))
                else:
                    new_rating = Rating.objects.create(user=request.user.username, rating=rating, product=product.name)
                    new_rating.save()
                    
                    rating_number = Rating.objects.filter(product=product.name).aggregate(Avg('rating'))['rating__avg']
                    product.arating = rating_number
                    product.rating = round(rating_number)
                    
                    product.save()
                    
                    return redirect('./' + str(pk))
                
            elif 'number' in request.POST:
                number = request.POST['number']
                
                product = Product.objects.get(pk=pk)
                
                if int(number) > 0:
                    new_number = Number.objects.create(user=request.user.username, number=number, product=product.name)
                else:
                    messages.info(request, 'The number entered is negative!')
                    return redirect('productdetails')
                    
                new_number.save()
                
                number_number = Number.objects.filter(product=product.name).aggregate(Sum('number'))['number__sum']
                product.sales = number_number
            
                product.save()
                
                new_cart_item = Cart_item.objects.create(user=request.user.username, product=product.name)
                new_cart_item.save()
                
                user_cart = Cart.objects.get(user=request.user.username)
                cil = Cart_item.objects.filter(user=request.user.username)
                
                count = 0
                
                for i in cil:
                    count += 1
                    
                user_cart.number = count
                user_cart.save()
                
                return redirect('../productdetails/' + str(pk))
            elif 'feedback' in request.POST:
                feedback = request.POST['feedback']
                product = Product.objects.get(pk=pk)
                
                if Rating.objects.filter(user=request.user.username, product=product.name).exists():
                    if Feedback.objects.filter(user=request.user.username, product=product.name):
                        fbg = Feedback.objects.get(user=request.user.username, product=product.name)
                        rbg = Rating.objects.get(user=request.user.username, product=product.name)
                        
                        if feedback != '':
                            fbg.feedback = feedback
                            fbg.rating = rbg.rating
                            fbg.save()
                        else:
                            fbg.delete()
                            
                        return redirect('./' + str(pk))
                    else:
                        if feedback != '':
                            gfr = Rating.objects.get(user=request.user.username, product=product.name)
                            new_feedback = Feedback.objects.create(user=request.user.username, feedback=feedback, product=product.name, rating=gfr.rating)
                            new_feedback.save()
                        
                            return redirect('./' + str(pk))
                        else:
                            messages.info(request, 'Please tell us what you think.')
                            return redirect('./' + str(pk))
                else:
                    messages.info(request, 'Please rate this item before commenting.')
                    return redirect('./' + str(pk))
            else:
                messages.info(request, 'Please select rating for this product')
                return redirect('./' + str(pk))
        else:
            messages.info(request, 'Login to access these features.')
            return redirect('auth')
            
    else:
         
        product = Product.objects.get(pk=pk)
        related = Product.objects.filter(type=product.type)
        cart_items = Cart_item.objects.filter(user=request.user.username, product=product.name)
        is_rated = Rating.objects.filter(user=request.user.username, product=product.name)
        is_feedback = Feedback.objects.filter(user=request.user.username, product=product.name)
        feedbackqs = Feedback.objects.filter(user=request.user.username, product=product.name).first()
        user_rating = Rating.objects.filter(user=request.user.username, product=product.name).first()
        
        if len(is_rated) == 0:
            rated = False
        else:
            rated = True
            
        if len(is_feedback) == 0:
            is_feedback = False
        else:
            is_feedback = True
        
        if len(cart_items) == 0:
            ici = False
        else:
            ici = True
        
        context = {
            'product': product,
            'related': related,
            'ici': ici,
            'rated': rated,
            'is_feedback': is_feedback,
            'feedbackqs': feedbackqs,
            'user_rating': user_rating,
        }
        
        return render(request, 'productdetails.html', context)

def search(request, *args, **kwargs):
    if request.method == 'POST':
        if 'search' in request.POST:
            search = request.POST.get('search')
            
            if search == '':
                return redirect('home')
            else:
                return redirect('../products/search_'+ str(search) +'/all')
    else:
        return redirect('home')

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
        context = {
        'plist': plist,
        'value': value,
        'type': type,
        }
        
        return render(request, 'producta.html', context)
    
    context = {
        'list': final_plist,
        'plist': plist,
        'value': value,
        'type': type,
    }
    
    return render(request, 'producta.html', context)

def about(request, *args, **kwargs):
    return render(request, 'about.html', {})

def remove(request, *args, **kwargs):
    if request.method == 'GET':
        product = request.GET['product']
        
        instance = Cart_item.objects.get(user=request.user.username, product=product)
        instance.delete()
        
        return redirect('cart')

def comments(request, prodid, *args, **kwargs):
    product = Product.objects.get(id=prodid)
    feedback_list = Feedback.objects.filter(product=product.name)

    context = {
        'feedback_list': feedback_list,
        'prodid': prodid,
    }
    
    return render(request, 'comments.html', context)

def productsearch(request, search, type, *args, **kwargs):
    if type == 'all':
        search_list = Product.objects.filter(name__icontains=search)
        
        value = 'Default'
        
        if request.method == 'POST':
            value = request.POST['order']
            
            if value == 'Price':
                search_list = Product.objects.filter(name__icontains=search).order_by('-price')
            elif value == 'Popularity':
                search_list = Product.objects.filter(name__icontains=search).order_by('-sales')
            elif value == 'Ratings':
                search_list = Product.objects.filter(name__icontains=search).order_by('-rating')
            else:
                search_list = Product.objects.filter(name__icontains=search)
    else:
        search_list = Product.objects.filter(name__icontains=search, type=type)
        
        value = 'Default'
        
        if request.method == 'POST':
            value = request.POST['order']
            
            if value == 'Price':
                search_list = Product.objects.filter(name__icontains=search, type=type).order_by('-price')
            elif value == 'Popularity':
                search_list = Product.objects.filter(name__icontains=search, type=type).order_by('-sales')
            elif value == 'Ratings':
                search_list = Product.objects.filter(name__icontains=search, type=type).order_by('-rating')
            else:
                search_list = Product.objects.filter(name__icontains=search, type=type)
                
    context = {
        'search_list': search_list,
        'value': value,
        'search': search,
        'type': type,
    }
    
    return render(request, 'error.html', context)

