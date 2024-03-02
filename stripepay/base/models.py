from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Created by: {self.user.username}, At: {self.created_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orders", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order id: {self.order.id}, Item: {self.item.name}"


class Discount(models.Model):
    order = models.ForeignKey(Order, related_name="discounts", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}"


class Tax(models.Model):
    order = models.ForeignKey(Order, related_name="taxes", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}"


class StripeKeys(models.Model):
    currency = models.CharField(max_length=3)
    publishable_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.currency}"
