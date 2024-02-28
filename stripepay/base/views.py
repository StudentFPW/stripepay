import stripe

from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


class PayView(TemplateView):
    template_name = "pay.html"


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelledView(TemplateView):
    template_name = "cancelled.html"


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
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
                                "name": "Apple headsets - AirPods",
                            },
                            "unit_amount": 2000,
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
