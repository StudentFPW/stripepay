import stripe

from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Item, OrderItem


@permission_classes([IsAuthenticated])
class SuccessView(TemplateView):
    """
    Простая вьюшка
    """

    template_name = "success.html"


@permission_classes([IsAuthenticated])
class CancelledView(TemplateView):
    """
    Простая вьюшка
    """

    template_name = "cancelled.html"


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def stripe_config(request):
    """
    Функция stripe_config возвращает публикуемый ключ Stripe в ответе JSON на запрос GET.
    """
    if request.method == "GET":
        return JsonResponse({"publicKey": settings.STRIPE_PUBLISHABLE_KEY}, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def buy_order(request, id):
    """
    Функция buy_order обрабатывает запрос GET для создания сеанса оформления заказа для определенного
    заказа с дополнительной проверкой кода купона.
    """
    if request.method == "GET":
        orders = OrderItem.objects.filter(order=id)
        total_amount = 0
        currency = ""
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        coupon_code = request.GET.get("coupon_code")

        if coupon_code:
            try:
                stripe.Coupon.retrieve(coupon_code)
            except stripe.error.InvalidRequestError as e:
                return JsonResponse({"error": "Invalid coupon code"})
            except stripe.error.StripeError as e:
                return JsonResponse({"error": str(e)})

        for order in orders:
            total_amount += order.item.price * order.quantity
            currency = order.item.currency

        line_items = [
            {
                "price_data": {
                    "currency": currency,
                    "product_data": {
                        "name": "payment",
                    },
                    "unit_amount": int(total_amount) * 100,
                },
                "quantity": 1,
            }
        ]

        try:
            if coupon_code:
                checkout_session = stripe.checkout.Session.create(
                    client_reference_id=(
                        request.user.id if request.user.is_authenticated else None
                    ),
                    payment_method_types=["card"],
                    line_items=line_items,
                    discounts=[{"coupon": coupon_code}],
                    mode="payment",
                    success_url=domain_url
                    + "success?session_id={CHECKOUT_SESSION_ID}/",
                    cancel_url=domain_url + "cancelled/",
                )
            else:
                checkout_session = stripe.checkout.Session.create(
                    client_reference_id=(
                        request.user.id if request.user.is_authenticated else None
                    ),
                    payment_method_types=["card"],
                    line_items=line_items,
                    mode="payment",
                    success_url=domain_url
                    + "success?session_id={CHECKOUT_SESSION_ID}/",
                    cancel_url=domain_url + "cancelled/",
                )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def view_orders(request, id):
    """
    Эта функция извлекает и отображает элементы заказа, связанные с определенным идентификатором заказа.
    """
    if request.method == "GET":
        try:
            orders = OrderItem.objects.filter(order=id)
            return render(request, "orders.html", {"orders": orders})
        except Item.DoesNotExist:
            return HttpResponse(status=404)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def buy_item(request, id):
    """
    Функция buy_item обрабатывает процесс создания сеанса оформления заказа для покупки товара
    с использованием интеграции платежей Stripe.
    """
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            item = Item.objects.get(id=id)
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=(
                    request.user.id if request.user.is_authenticated else None
                ),
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": item.currency,
                            "product_data": {
                                "name": item.name,
                            },
                            "unit_amount": int(item.price) * 100,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}/",
                cancel_url=domain_url + "cancelled/",
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def view_item(request, id):
    """
    Эта функция извлекает и отображает элемент с определенным идентификатором.
    """
    if request.method == "GET":
        try:
            item = Item.objects.get(id=id)
            return render(request, "item.html", {"item": item})
        except Item.DoesNotExist:
            return HttpResponse(status=404)


@permission_classes([IsAuthenticated])
@csrf_exempt
def stripe_webhook(request):
    """
    Функция stripe_webhook обрабатывает входящие события веб-перехватчика из Stripe, проверяет подпись и
    обрабатывает успешные события оплаты.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")

    return HttpResponse(status=200)
