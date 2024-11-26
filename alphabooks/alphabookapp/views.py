from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render
import random
from .models import * 
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings

# Create your views here.
CART_SESSION_KEY = 'cart'

QUOTES = [

        {"text": "A room without books is like a body without a soul.", "author": "Marcus Tullius Cicero"},
        {"text": "So many books, so little time.", "author": "Frank Zappa"},
        {"text": "Books are a uniquely portable magic.", "author": "Stephen King"},

    ]
API_KEY = "AIzaSyB_xVXmd4KYDY-xysB5fK3MUS80-uMX6zc"

def get_featured_books():
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:fiction&orderBy=relevance&key={API_KEY}&maxResults=8'
    response = requests.get(url)
    books = response.json().get('items', [])
    return books

# Fetch latest books
def get_latest_books():
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:fiction&orderBy=newest&key={API_KEY}&maxResults=8'
    response = requests.get(url)
    books = response.json().get('items', [])
    return books

def get_all_books():
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:fiction&key={API_KEY}&maxResults=40'
    response = requests.get(url)
    books = response.json().get('items', [])
    return books

# Index view
def index(request):
    quote = random.choice(QUOTES)

    featured_books = get_featured_books()
    for book in featured_books:
        sale_info = book.get('saleInfo', {})
        list_price = sale_info.get('listPrice', {})
        book['price'] = list_price.get('amount', 'Not available')

    latest_books = get_latest_books()

    for book in latest_books:
        sale_info = book.get('saleInfo', {})
        list_price = sale_info.get('listPrice', {})
        book['price'] = list_price.get('amount', 'Not available')

    return render(request, 'index.html', {
        'quote': quote,
        'featured_books': featured_books,
        'latest_books': latest_books,
    })

def books(request):
    
    all_books = get_all_books()
    for book in all_books:
        sale_info = book.get('saleInfo', {})
        list_price = sale_info.get('listPrice', {})
        book['price'] = list_price.get('amount', 'Not available')

    paginator = Paginator(all_books, 12) 
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)
        
    return render(request, 'books.html', {'all_books': books_page, 'paginator': paginator})

def get_book_detail(book_id):
    url = f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={API_KEY}'
    response = requests.get(url)
    book = response.json()
    return book

def book_details(request,book_id):
    

    book_details = get_book_detail(book_id)
    sale_info = book_details.get('saleInfo', {})
    list_price = sale_info.get('listPrice', {})
    price = list_price.get('amount', 0)
    book_details['price'] = list_price.get('amount', 'Not available')
    book_image = book_details.get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail', None)
    if request.method == "POST":
        if 'add_to_cart' in request.POST:
            user_id=request.session["userID"]
            reg_id=user_register.objects.get(user__id=user_id)
            qty = int(request.POST.get("qty", 1))
            try: 
                cart_item = Carts.objects.get(user_id=reg_id, book_id=book_id)
               
                cart_item.order_qty += qty  
                cart_item.save()
                created = False 
            except Carts.DoesNotExist:
              
                cart_item = Carts.objects.create(user_id=reg_id, book_id=book_id, 
                                                    book_title=book_details['volumeInfo']['title'],
                                                    book_cover=book_image, price=price, 
                                                    order_qty=qty)
                created = True

            if created:
                
                messages.success(request, f"{cart_item.book_title} has been added to your cart.")
                return redirect('cart')
            else:
                messages.info(request, f"{cart_item.book_title} already in your cart.")
                return redirect('cart')
                

    context={
        'book_details':book_details,
       
    }
    return render(request, 'book_details.html',context)

@login_required(login_url='account')
def cartlist(request):
    
    user_id=request.session["userID"]
    reg_id=user_register.objects.get(user__id=user_id)
    
    cartdata=Carts.objects.filter(user_id__id=reg_id.id)
    total_price = sum(item.price * item.order_qty for item in cartdata)

    cartdatas = []

    for item in (cartdata):
        book_total= item.price * item.order_qty
        
        cartdatas.append({
            'item':item,
            'book_total':book_total,
        })

    if request.method == "POST":
        
        full_name = request.POST['full_name']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zip_code = request.POST['zip_code']

        if not cartdata:
            messages.error(request, "Your cart is empty.")
            return redirect('cart')
        
        for d in (cartdata):
            Bookcover = d.book_cover
            Booktitle = d.book_title
            Bookprice = d.price
            orderprice = d.price * d.order_qty
            qty = d.order_qty

        
        
            order = Order.objects.create(
                user=reg_id,
                full_name=full_name,
                street=street,
                city=city,
                state=state,
                country=country,
                zip_code=zip_code,
                book_cover= Bookcover,
                book_title= Booktitle,
                price= Bookprice,
                order_amount= orderprice,
                order_qty= qty,

            )
            cartdata.delete()
            
        return redirect('orders')
        
        
    context={
        'cartdata':cartdatas,
        'total_price':total_price 
    }        
    
    return render(request, 'cart.html',context)

@login_required(login_url='account')
def cartremove(request,id):
    remove=Carts.objects.get(book_id=id)
        
    remove.delete()
    return redirect('cart')

@login_required(login_url='account')
def order(request):

    user_id=request.session["userID"]
    reg_id=user_register.objects.get(user__id=user_id)
    
    orders=Order.objects.filter(user_id__id=reg_id.id)

    context={
        'orders':orders,
    }


    return render(request, 'order.html',context)

@login_required(login_url='account')
def orderremove(request,id):
    remove=Order.objects.get(id=id) 
        
    remove.delete()
    return redirect('orders')

def account(request):
    
    if request.POST and 'reg' in request.POST:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("cpassword")

        errors = []

        if len(username) < 6:
            errors.append("Username must be at least 6 characters long.")
        
        if password != confirm_password:
            errors.append("Passwords do not match.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'account.html')
        
        if password == confirm_password:
            try:
                logine = Login.objects.create_user(username=username, password=password, userType='user', viewpassword=password)
                logine.save()
                obj = user_register.objects.create(user=logine,
                                                  user_email=email,
                                                  user_username=username,
                                                  user_password=password)
                obj.save()
                return redirect('account')
            
            except IntegrityError:
                messages.error(request, 'Username is already taken. Please choose a different one.')
            
    if request.POST and 'log' in request.POST:
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            request.session["userID"] = user.id
            return redirect('home')

    return render(request, 'account.html')

def signOut(request):
    logout(request)

    return redirect('home')