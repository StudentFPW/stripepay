from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import (
    ItemViewSet,
    OrderViewSet,
    OrderItemViewSet,
    DiscountViewSet,
    TaxViewSet,
)

from .views import (
    SuccessView,
    CancelledView,
    stripe_config as config,
    stripe_webhook as webhook,
    buy_item,
    view_item,
    buy_order,
    view_orders,
)

router = DefaultRouter()
router.register(r"item-api", ItemViewSet)
router.register(r"order-api", OrderViewSet)
router.register(r"previeworder-api", OrderItemViewSet)
router.register(r"discount-api", DiscountViewSet)
router.register(r"tax-api", TaxViewSet)

urlpatterns = [
    path("", include(router.urls)),
    #
    path("config/", config, name="config"),
    #
    path("buy/<int:id>/", buy_item, name="buy_item"),
    path("item/<int:id>/", view_item, name="view_item"),
    #
    path("order/<int:id>/", buy_order, name="buy_order"),
    path("previeworders/<int:id>/", view_orders, name="view_orders"),
    #
    path("success/", SuccessView.as_view(), name="success"),
    path("cancelled/", CancelledView.as_view(), name="cancelled"),
    #
    path("webhook/", webhook, name="webhook"),
]
