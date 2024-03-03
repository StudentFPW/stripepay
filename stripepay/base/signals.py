import stripe

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

from .models import Order, Discount


@receiver(post_save, sender=User)
def create_order(sender, instance, created, **kwargs):
    """
    Эта функция создает объект Order для экземпляра User после его сохранения.
    """
    if created:
        Order.objects.create(user=instance)


@receiver(post_save, sender=Discount)
def create_cupon(sender, instance, created, **kwargs):
    """
    Эта функция создает купон в Stripe на основе экземпляра модели Discount.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if created:
        if instance.duration == 0:
            cupon = stripe.Coupon.create(
                percent_off=instance.percent_off,
                duration="once",
            )
        else:
            cupon = stripe.Coupon.create(
                percent_off=instance.percent_off,
                duration="forever",
            )
        instance.cupon_id = cupon["id"]
        instance.save()
