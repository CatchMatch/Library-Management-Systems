from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import *

# Home Page
def home(request):
    return render(request, 'home.html')

# Login
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Signup.objects.get(email=email)
            if user.password == password:
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                messages.error(request, 'Incorrect password')
        except Signup.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('signup')

    return render(request, 'login.html')

# Signup
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_num = request.POST.get('phone_num')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if not Signup.objects.filter(email=email).exists():
            user = Signup.objects.create(username=username, email=email, phone_num=phone_num,
                                         password=password, password2=password2)
            request.session['user_id'] = user.id
            return redirect('home')
        else:
            messages.error(request, 'Email already registered')
            return redirect('login')

    return render(request, 'signup.html')

# Dashboard
def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = Signup.objects.get(id=user_id)
    borrowed_books = Borrow.objects.filter(user=user)
    return render(request, 'dashboard.html', {'borrowed_books': borrowed_books})

# Secret Page (Admin View)
def secret(request):
    borrowed_books = Borrow.objects.all()
    stocks = Stock.objects.select_related('book').all()
    return render(request, 'secret.html', {'borrowed_books': borrowed_books, 'stocks': stocks})

# Catalog
def catalog(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = Signup.objects.get(id=user_id)
    books = Book.objects.all().select_related('stock')
    borrowed_book_ids = Borrow.objects.filter(user=user).values_list('book_id', flat=True)
    return render(request, 'catalog.html', {
        'books': books,
        'borrowed_book_ids': set(borrowed_book_ids)
    })

# Borrow a book
def borrow_book(request, book_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        user = Signup.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        stock = Stock.objects.get(book=book)

        if stock.available_copies > 0:
            stock.available_copies -= 1
            stock.save()

            due_date = timezone.now().date() + timedelta(days=14)
            Borrow.objects.create(user=user, book=book, borrow_date=timezone.now().date(), due_date=due_date)
            messages.success(request, f"You borrowed '{book.title}'")
        else:
            messages.error(request, f"'{book.title}' is out of stock")

        return redirect('catalog')

# Return a book
def return_book(request, book_id):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')

        user = Signup.objects.get(id=user_id)
        book = get_object_or_404(Book, id=book_id)
        stock = Stock.objects.get(book=book)

        Borrow.objects.filter(user=user, book=book).delete()

        if stock.available_copies < stock.total_copies:
            stock.available_copies += 1
            stock.save()

        messages.success(request, f"You returned '{book.title}'")

        return redirect('catalog')

# Logout
def logout(request):
    request.session.flush()
    return redirect('home')
