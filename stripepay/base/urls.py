from django.urls import path

from .views import (
    SuccessView,
    CancelledView,
    stripe_config as config,
    stripe_webhook as webhook,
    buy_item,
    view_item,
)

urlpatterns = [
    path("config/", config, name="config"),
    path("buy/<int:id>/", buy_item, name="buy_item"),
    path("item/<int:id>/", view_item, name="view_item"),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancelled/", CancelledView.as_view(), name="cancelled"),
    path("webhook/", webhook, name="webhook"),
]
