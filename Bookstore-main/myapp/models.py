import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('normal', 'User'),
        ('shopowner', 'Shop Owner'),
    )
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    u_image = models.ImageField(upload_to='User/', blank=True, null=True,default='static/image/default.png',)
    groups = models.ManyToManyField(
        Group,
        related_name='user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions',
        blank=True
    )

    def __str__(self):
        return self.username

class Book(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book_name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    genre = models.CharField(max_length=200)
    stock_quantity = models.IntegerField(default=0)
    rentable = models.CharField(max_length=200, blank=True, null=True)
    availability = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='Books/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.book_name

    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0


class Review(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.book.book_name} by {self.user.username}"

# Author model
class Author(models.Model):
    author_name = models.CharField(max_length=200)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='Author', blank=True, null=True)

    def __str__(self):
        return self.author_name


# Shop model
class Shop(models.Model):
    shop_id = models.IntegerField(blank=True, null=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE,related_name='shop_owner', blank=True, null=True)
    shop_email =models.EmailField(unique=True, blank=True, null=True)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    shop_name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    contact_number = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return self.shop_id if self.shop_id is not None else "Unnamed id"

# Order model
class Order(models.Model):
    order_id =  models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_name')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = (
        ('buy', 'Buy'),
        ('rent', 'Rent'),
    )
    status = models.CharField(max_length=200, choices=order_status, blank=True, null=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book_name} (Ordered on: {self.order_date})"


# Payment model
class Payment(models.Model):
    payment_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_payments'  # Unique related_name for Payment
    )
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=200)
    amount = models.IntegerField()

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Subscription"