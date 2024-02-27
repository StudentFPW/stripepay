from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=3)


class Discount(models.Model):
    order = models.ForeignKey(Order, related_name="discounts", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Tax(models.Model):
    order = models.ForeignKey(Order, related_name="taxes", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)


class StripeKeys(models.Model):
    currency = models.CharField(max_length=3)
    publishable_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)
