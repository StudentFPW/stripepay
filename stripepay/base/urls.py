from django.urls import path

from .views import (
    PayView,
    SuccessView,
    CancelledView,
    stripe_config as config,
    create_checkout_session as checkout,
    stripe_webhook as webhook,
)

urlpatterns = [
    path("stripe/", PayView.as_view(), name="pay"),
    path("config/", config, name="config"),
    path("checkout/", checkout, name="checkout"),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancelled/", CancelledView.as_view(), name="cancelled"),
    path("webhook/", webhook, name="webhook"),
]
