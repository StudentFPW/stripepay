# Пример файла .env

```bash
SECRET_KEY = ''
DEBUG = 0
DJANGO_ALLOWED_HOSTS = '127.0.0.1 localhost'
ADMIN_PASSWORD = ''
ADMIN_EMAIL = ''
ADMIN_USERNAME = ''
STRIPE_PUBLISHABLE_KEY = ''
STRIPE_SECRET_KEY = ''
STRIPE_ENDPOINT_SECRET = ''
```

## Дополнительная информация

1. Для переменной `STRIPE_ENDPOINT_SECRET` необходимо выполнить определенные действия, указанные на этой странице [здесь](https://docs.stripe.com/stripe-cli#install).
После этого выполните команду `stripe listen --forward-to localhost:8000/webhook/`. В результате появится ключ, который нужно будет присвоить переменной `STRIPE_ENDPOINT_SECRET`.

2. Номера тестовых карт Stripe доступны на [этой странице](https://docs.stripe.com/testing#cards).

3. Для тестирования купонов в системе, необходимо выполнить определенные действия, указанные на [этой странице](https://docs.stripe.com/billing/subscriptions/coupons#create-a-coupon).

## Первоначальная Загрузка

```bash
```
