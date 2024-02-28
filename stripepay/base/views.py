import stripe

from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .models import Item


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelledView(TemplateView):
    template_name = "cancelled.html"


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        return JsonResponse({"publicKey": settings.STRIPE_PUBLISHABLE_KEY}, safe=False)


@csrf_exempt
def buy_item(request, id):
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
                            "currency": "usd",
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


@csrf_exempt
def view_item(request, id):
    if request.method == "GET":
        try:
            item = Item.objects.get(id=id)
            return render(request, "item.html", {"item": item})
        except Item.DoesNotExist:
            return HttpResponse(status=404)


@csrf_exempt
def stripe_webhook(request):
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
