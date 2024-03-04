# <span style="color:lightgreen">Пример файла .env</span>

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

Для удобства, рекомендуется разместить файл `.env` в той же директории, что и файл `requirements.txt`.

## <span style="color:lightgreen">Первоначальная Загрузка</span>

### 1. Настройка ключей Stripe

Для использования Stripe необходимо установить соответствующие ключи. В файле `.env` присвойте значения ключей переменным:

```bash
STRIPE_PUBLISHABLE_KEY = 'Ваш_публичный_ключ'
STRIPE_SECRET_KEY = 'Ваш_секретный_ключ'
STRIPE_ENDPOINT_SECRET = 'Ваш_секретный_ключ_для_веб-хуков' ← Эта переменная необязательна и не требуется в режиме тестирования.
```

Вы можете найти документацию Stripe по генерации ключей API на их официальном сайте [здесь](https://docs.stripe.com/keys).

### 2. Настройка административных данных

Для определения административных данных в файле `.env` укажите значения переменных:

```bash
ADMIN_PASSWORD = 'Ваш_пароль_администратора'
ADMIN_EMAIL = 'Ваш_адрес_электронной_почты_администратора'
ADMIN_USERNAME = 'Ваше_имя_пользователя_администратора'
```

### 3. Настройка секретного ключа Django

Для генерации секретного ключа Django и его установки в файле `.env` выполните следующие действия:

1. Сгенерируйте секретный ключ, с помощью Python:

```bash
python -c "import secrets; print(secrets.token_hex(58))"
```

2. Присвойте сгенерированный ключ переменной в файле .env:

```bash
SECRET_KEY = 'Ваш_секретный_ключ_Django'
```

## <span style="color:lightgreen">Установка зависимостей</span>

Для удобства, рекомендуется разместить файл `venv` в той же директории, что и файл `requirements.txt`.

```bash
pip install virtualenv
virtualenv venv
```

На Windows:

```bash
venv\Scripts\activate
```

На macOS и Linux:

```bash
source venv/bin/activate
```

Установка зависимостей из файла в виртуальное окружение:

```bash
pip install -r requirements.txt
```

## <span style="color:lightgreen">Установка и запуск проекта StripePay</span>

1. Перейдите в директорию \stripepay\stripepay:

```bash
cd ./stripepay
```

2. Выполните следующие команды для создания миграций базы данных:

```bash
py manage.py makemigrations
```

3. Примените миграции:

```bash
py manage.py migrate
```

4. Чтобы инициализировать учетную запись администратора, используйте следующую команду:

```bash
py manage.py initadmin
```

5. Запустите сервер:

```bash
py manage.py runserver
```

## <span style="color:lightgreen">Гайд по использованию</span>

1. Все последующие действия производятся в панели администратора. Вы можете создать товары (items) и затем добавить их в корзину (order items). Также вы можете создать купон в разделе (discounts). Созданный вами купон также автоматически создается в системе Stripe.

2. Для выполнения последующих действий с URL-адресами необходимо авторизоваться. Например, если вы перейдете по адресу <http://127.0.0.1:8000/swagger/>, вы получите подробную документацию по всем API. Если перейти по адресу <http://127.0.0.1:8000/item/1/>, вы сможете просмотреть детали продукта и сделать заказ. А по адресу <http://127.0.0.1:8000/previeworders/1/> вы сможете оплатить несколько товаров и применить ранее созданные купоны.

## <span style="color:lightgreen">Дополнительная информация</span>

1. Для переменной `STRIPE_ENDPOINT_SECRET` необходимо выполнить определенные действия, указанные на этой странице [здесь](https://docs.stripe.com/stripe-cli#install).
После этого выполните команду `stripe listen --forward-to localhost:8000/webhook/`. В результате появится ключ, который нужно будет присвоить переменной `STRIPE_ENDPOINT_SECRET`.

2. Номера тестовых карт Stripe доступны на [этой странице](https://docs.stripe.com/testing#cards).

3. Для тестирования купонов в системе, вы можете выполнить определенные действия, указанные на [этой странице](https://docs.stripe.com/billing/subscriptions/coupons#create-a-coupon). Также можно создать купон через панель администратора во вкладке 'Discount'.

```bash
На остальной функционал просто времени не хватило. Основная логика приложения и его работоспособность соответствуют тестовому заданию.
```
