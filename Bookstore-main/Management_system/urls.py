"""
URL configuration for Management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import settings
from django.conf.urls.static import static

from myapp import views as myapp_views
from myapp import views as login_user
from myapp import views as subscribed_user
from myapp import views as shop
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', myapp_views.home, name='home'),
    path('contacts/', myapp_views.contacts, name='contacts'),
    path('books/', myapp_views.books, name='books'),
    path('book/<uuid:book_id>/', views.books_details, name='books_details'),
    path('book/<uuid:book_id>/review/', views.submit_review, name='submit_review'),
    path('login/', myapp_views.login, name='login'),
    path('signup/', myapp_views.signup, name='signup'),

    path('subscription/', login_user.subscription, name='subscription'),
    path('forget_pass/', login_user.forget_pass, name='forget_pass'),
    path('payment/', login_user.payment, name='payment'),
    path('process-payment/', login_user.process_payment, name='process_payment'),

    path('log_base/', login_user.log_base, name='log_base'),
    path('log_navbar/', login_user.log_navbar, name='log_navbar'),
    path('log_book/', login_user.log_book, name='log_book'),
    path('log_books_details/<uuid:book_id>/', login_user.log_books_details, name='log_books_details'),
    path('log_help/', login_user.log_help, name='log_help'),
    path('log_profile/',login_user.log_profile, name='log_profile'),
    path('logout/', login_user.logout_view, name='logout'),
    path('update_profile/', login_user.update_profile, name='update_profile'),
    path('process_payment_for_book/<uuid:book_id>/', login_user.process_payment_for_book,name='process_payment_for_book'),
    path('payment_confirmation/<uuid:book_id>/', login_user.payment_confirmation,name='payment_confirmation'),

    path('sub_profile/', subscribed_user.sub_profile, name='sub_profile'),
    path('subscribed_user/sub_base/', subscribed_user.sub_base, name='sub_base'),
    path('sub_navbar/', subscribed_user.sub_navbar, name='sub_navbar'),
    path('sub_books/', subscribed_user.sub_books, name='sub_books'),
    path('sub_rent_books/', subscribed_user.sub_rent_books, name='sub_rent_books'),
    path('sub_rent_books_details/<uuid:book_id>/', subscribed_user.sub_rent_books_details, name='sub_rent_books_details'),
    path('sub_books_details/<uuid:book_id>/', subscribed_user.sub_books_details, name='sub_books_details'),
    path('confirm_payment/<uuid:book_id>/', subscribed_user.confirm_payment,name='confirm_payment'),
    path('rent_info/<uuid:book_id>/', subscribed_user.rent_info, name='rent_info'),
    path('rent_confirmation/<uuid:book_id>/', subscribed_user.rent_confirmation, name='rent_confirmation'),
    path('update_sub_profile/', login_user.update_sub_profile, name='update_sub_profile'),
    path('sub_help/', subscribed_user.sub_help, name='sub_help'),

    path('shop_base/', shop.shop_base, name='shop_base'),
    path('shop_navbar/', shop.shop_navbar, name='shop_navbar'),
    path('shop_book/', shop.shop_books, name='shop_books'),
    path('shop_book_details/<uuid:book_id>/', shop.shop_book_details, name='shop_book_details'),
    path('shop_help/', shop.shop_help, name='shop_help'),
    path('shop_profile/', shop.shop_profile, name='shop_profile'),
    path('shop_update_profile/', login_user.shop_update_profile, name='shop_update_profile'),

    path('sub_profile/<int:user_id>/', views.view_sub_profile, name='view_sub_profile'),
    path('upload_books/', shop.upload_books, name='upload_books'),
    path('update_books/<uuid:book_id>/', shop.update_books, name='update_books'),
    path('delete_books/<uuid:book_id>/', shop.delete_books, name='delete_books'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

