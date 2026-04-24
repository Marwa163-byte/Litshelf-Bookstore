from django.contrib.auth import authenticate,logout, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .Books_Forms import BooksForm, ReviewForm
from .User_form import SignupForm, ProfileUpdateForm, LoginForm, Sub_LoginForm, shop_ProfileUpdateForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Order, Subscription


def home(request):
    return render(request, template_name='bmHome/home.html')


def books(request):
    genre_filter = request.GET.get('genre', None)
    if genre_filter:
        allbooks = Book.objects.filter(genre__iexact=genre_filter)
    else:
        allbooks = Book.objects.all()

    item = {
        'allbooks': allbooks,
        'genre': genre_filter,
    }
    return render(request, template_name='bmHome/books.html', context=item)
def books_details(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = book.reviews.all().order_by('-created_at')

    # Handle review submission (only for authenticated users)
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('books_details', book_id=book_id)
    else:
        form = ReviewForm() if request.user.is_authenticated else None

    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'bmHome/books_details.html', context)

@login_required
def submit_review(request, book_id):

    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
    return redirect('books_details', book_id=book_id)

def contacts(request):
    return render(request, template_name='bmHome/contacts.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.user_type == 'shopowner':

                Shop.objects.create(
                    username=user,
                    shop_email=user.email,
                    shop_name=f"{user.username}'s Shop"
                )
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'bmHome/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.user_type == 'normal':
                    return redirect('log_profile')
                elif user.user_type == 'shopowner':
                    return redirect('shop_profile')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'bmHome/login.html', {'form': form})

####################################################################
@login_required
def subscription(request):
    if request.method == 'POST':
        form = Sub_LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = authenticate(request, username=username, password=password)

            if user is None:
                user = authenticate(request, username=email, password=password)

            if user is not None:

                return redirect('sub_profile')
            else:
                form.add_error(None, 'Invalid login credentials')
    else:
        form = Sub_LoginForm()
    return render(request, 'login_user/subscription.html', {'form': form})


def forget_pass(request):
    return render(request, template_name='login_user/forget_pass.html')

def payment(request):
    return render(request, template_name='login_user/payment.html')
def process_payment(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        transaction_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')

        if phone and transaction_id and amount:
            messages.success(request, "Payment processed successfully!")
            return redirect('payment')
        else:
            messages.error(request, "Invalid payment details. Please try again.")
            return redirect('payment')

    return redirect('payment')

#######################################################################################
def log_base(request):
    return render(request, template_name='login_user/log_base.html')
def log_navbar(request):
    return render(request, template_name='login_user/log_navbar.html')
def log_book(request):
    genre_filter = request.GET.get('genre', None)
    if genre_filter:
        allbooks = Book.objects.filter(genre__iexact=genre_filter)
    else:
        allbooks = Book.objects.all()

    item = {
        'all_books': allbooks,
        'genre': genre_filter,
    }
    return render(request, template_name='login_user/log_book.html', context=item)


def log_books_details(request, book_id):
    allbooks = get_object_or_404(Book, book_id =book_id)
    reviews = Review.objects.filter(book=allbooks).order_by('-created_at')

    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment = request.POST.get('comment')
        if comment:  # Basic validation
            Review.objects.create(
                book=allbooks,
                user=request.user,
                comment=comment,
            )
            messages.success(request, 'Your review has been submitted!')
            return redirect('log_books_details', book_id=book_id)

    context = {
        'allbooks': allbooks,
        'reviews': reviews
    }
    return render(request, 'login_user/log_books_details.html', context)



@login_required
def process_payment_for_book(request, book_id):
    allbooks = get_object_or_404(Book, book_id = book_id)

    if request.method == 'POST':
        phone = request.POST.get('phone')
        transaction_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')

        if phone and transaction_id and amount:
            # Create order record for purchase
            Order.objects.create(
                username =request.user,
                book_name = allbooks,
                status='buy',
                payment_status=True
            )
            allbooks.stock_quantity -= 1
            allbooks.is_sold = True
            allbooks.save()
            messages.success(request, f"Payment successful for {allbooks.book_name}. Transaction ID: {transaction_id}.")
            return redirect('payment_confirmation', book_id=allbooks.book_id)
        else:
            messages.error(request, "Please provide all the required details.")
            return redirect('payment_confirmation', book_id=allbooks.book_id)

    return render(request, 'login_user/process_payment_for_book.html', {'allbooks': allbooks})


@login_required
def payment_confirmation(request, book_id):
    allbooks = get_object_or_404(Book, book_id=book_id)
    return render(request, 'login_user/payment_confirmation.html', {'allbooks': allbooks})

def log_help(request):
    return render(request, template_name='login_user/log_help.html')

@login_required
def log_profile(request):
    return render(request, template_name='login_user/log_profile.html',context= {'user': request.user})
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('log_profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'login_user/profile_form.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')
def sub_help(request):
    return render(request, template_name='subscribed_user/sub_help.html')

@login_required
def sub_profile(request):
    return render(request, template_name='subscribed_user/sub_profile.html',context={'user': request.user})

def update_sub_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('sub_profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'subscribed_user/sub_profile_form.html', {'form': form})

def sub_navbar(request):
    return render(request, template_name='subscribed_user/sub_navbar.html')
def sub_base(request):
    return render(request, template_name='subscribed_user/sub_base.html')
def sub_books(request):
    allbooks = Book.objects.all()
    item = {
        'allbooks': allbooks,
    }
    return render(request, template_name='subscribed_user/sub_books.html',context=item)


def sub_rent_books(request):
    allbooks = Book.objects.filter(rentable= 'yes')
    item = {
        'allbooks': allbooks,
    }
    return render(request, 'subscribed_user/sub_rent_books.html', context= item)

def sub_books_details(request,book_id):
    allbooks = get_object_or_404(Book, book_id=book_id)
    reviews = Review.objects.filter(book=allbooks).order_by('-created_at')

    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment = request.POST.get('comment')
        if comment:  # Basic validation
            Review.objects.create(
                book=allbooks,
                user=request.user,
                comment=comment,
            )
            messages.success(request, 'Your review has been submitted!')
            return redirect('sub_books_details', book_id=allbooks.book_id)

    item = {
        'allbooks': allbooks,
        'reviews': reviews
    }
    return render(request, template_name='subscribed_user/sub_books_details.html',context= item)

def confirm_payment(request, book_id):
    allbooks = get_object_or_404(Book, book_id = book_id)

    if request.method == 'POST':
        phone = request.POST.get('phone')
        transaction_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')

        if phone and transaction_id and amount:
            # Create order record for purchase
            Order.objects.create(
                username =request.user,
                book_name = allbooks,
                status='buy',
                payment_status=True
            )
            allbooks.stock_quantity -= 1
            allbooks.is_sold = True
            allbooks.save()
            messages.success(request, f"Payment successful for {allbooks.book_name}. Transaction ID: {transaction_id}.")
            return redirect('confirm_payment', book_id=allbooks.book_id)
        else:
            messages.error(request, "Please provide all the required details.")
            return redirect('confirm_payment', book_id=allbooks.book_id)

    return render(request, 'subscribed_user/confirm_payment.html', {'allbooks': allbooks})

def sub_rent_books_details(request,book_id):
    allbooks = get_object_or_404(Book, book_id=book_id)
    reviews = Review.objects.filter(book=allbooks).order_by('-created_at')

    # Handle review submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment = request.POST.get('comment')
        if comment:  # Basic validation
            Review.objects.create(
                book=allbooks,
                user=request.user,
                comment=comment,
            )
            messages.success(request, 'Your review has been submitted!')
            return redirect('sub_rent_books_details', book_id=allbooks.book_id)

    item = {
        'allbooks': allbooks,
        'reviews': reviews
    }
    return render(request, template_name='subscribed_user/sub_rent_books_details.html',context= item)


@login_required
def rent_info(request, book_id):
    allbooks = get_object_or_404(Book, book_id=book_id)
    if request.method == "POST":
        email = request.POST.get('email')
        address = request.POST.get('address')
        duration = request.POST.get('duration')
        if email and address and duration:
            # Create order record for purchase
            Order.objects.create(
                username =request.user,
                book_name = allbooks,
                status='rent',
                payment_status=True
            )
            allbooks.stock_quantity -= 1
            allbooks.is_rented = True
            allbooks.save()

            messages.success(request, "Book rental confirmed!")
            return redirect('rent_confirmation', book_id=allbooks.book_id)
        else:
            messages.error(request, "Please provide all the required details.")
            return redirect('confirm_payment', book_id=allbooks.book_id)

    return render(request, 'subscribed_user/rent_info.html', {'allbooks': allbooks})


@login_required
def rent_confirmation(request, book_id):
    allbooks = get_object_or_404(Book, book_id=book_id)
    return render(request, 'subscribed_user/rent_confirmation.html', {'allbooks': allbooks})


###########################################################################################################################
def shop_base(request):
    return render(request, template_name='shop_owner/shop_base.html')

def shop_navbar(request):
    return render(request, template_name='shop_owner/shop_navbar.html')

def shop_books(request):
    genre_filter = request.GET.get('genre', None)
    if genre_filter:
        all_books = Book.objects.filter(genre__iexact=genre_filter)
    else:
        all_books = Book.objects.all()

    item = {
        'all_books': all_books,
        'genre': genre_filter,
    }
    return render(request, template_name='shop_owner/shop_books.html', context=item)

def shop_help(request):
    return render(request, template_name='shop_owner/shop_help.html')

@login_required
def shop_profile(request):
    return render(request, 'shop_owner/shop_profile.html', {'user': request.user})

@login_required
def shop_update_profile(request):
    if request.method == 'POST':
        form = shop_ProfileUpdateForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

            return redirect('shop_profile')
    else:
        form = shop_ProfileUpdateForm(instance=request.user)
    return render(request, 'shop_owner/shop_profile_form.html', {'form': form})


def shop_book_details(request, book_id):
    allbooks = get_object_or_404(Book, book_id=book_id)
    item = {
        'allbooks': allbooks,
    }
    return render(request, template_name='shop_owner/shop_book_details.html', context=item)


def upload_books(request):
    form = BooksForm()
    if request.method == 'POST':
        form = BooksForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop_books')
    context = {'form': form}
    return render(request, template_name='shop_owner/books_form.html', context=context)

def update_books(request, book_id):
    allbooks = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        form = BooksForm(request.POST, request.FILES, instance=allbooks)
        if form.is_valid():
            form.save()
            return redirect('shop_books')
    else:
        form = BooksForm(instance=allbooks)
    context = {'form': form}
    return render(request, template_name='shop_owner/books_form.html', context=context)

def delete_books(request, book_id):
    allbooks = get_object_or_404(Book, book_id=book_id)
    if request.method == 'POST':
        allbooks.delete()
        messages.success(request, f"'{allbooks.book_name}' has been deleted successfully.")
        return redirect('shop_books')
    return render(request, 'shop_owner/delete_books.html', {'allbooks': allbooks})

def view_sub_profile(request, user_id):
    sub_profile = get_object_or_404(SubProfile, user_id=user_id)
    return render(request, 'sub_profile.html', {'sub_profile': sub_profile})


