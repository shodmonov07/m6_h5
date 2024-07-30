from django.contrib.auth.models import User
from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    description = models.TextField(max_length=150)
    image = models.ImageField(upload_to="uploads/product/")
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.IntegerField(default=1)
    phone = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    date = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    address = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return f"Order of {self.product} by {self.customer}"


class Comment(models.Model):
    text = models.TextField()
    filtered_text = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', default=1)

    def save(self, *args, **kwargs):
        bad_words = ['ahmoq', 'jin ursin', 'jinni3']
        comment_filter = Comment.CommentFilter(bad_words)
        self.filtered_text = comment_filter.filter_comment(self.text)
        super().save(*args, **kwargs)

    class CommentFilter:
        def __init__(self, bad_words):
            self.bad_words = set(bad_words)

        def filter_comment(self, comment):
            words = comment.split()
            filtered_words = [word if word.lower() not in self.bad_words else '*' * len(word) for word in words]
            return ' '.join(filtered_words)
