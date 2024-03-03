/* Этот фрагмент кода JavaScript выполняет серию запросов на выборку для получения данных и
взаимодействия со службой обработки платежей Stripe. */
fetch("/config/")
    .then((request) => {
        return request.json();
    })
    .then((data) => {
        const stripe = Stripe(data.publicKey);

        document.querySelector("#submitBtn").addEventListener("click", () => {
            var currentUrl = window.location.href;
            var coupon_code = document.getElementById('coupon_code').value
            if (coupon_code) {
                fetch(`/order/${currentUrl[currentUrl.length - 2]}/?coupon_code=${coupon_code}`)
                    .then((request) => {
                        return request.json();
                    })
                    .then((data) => {
                        return stripe.redirectToCheckout({ sessionId: data.sessionId })
                    })
                    .catch(() => {
                        alert("Invalid cupon!")
                    });
            } else {
                fetch(`/order/${currentUrl[currentUrl.length - 2]}/`)
                    .then((request) => {
                        return request.json();
                    })
                    .then((data) => {
                        return stripe.redirectToCheckout({ sessionId: data.sessionId })
                    })
                    .catch(() => {
                        alert("Try again!")
                    });
            }

        });
    });