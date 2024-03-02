fetch("/config/")
    .then((request) => {
        return request.json();
    })
    .then((data) => {
        const stripe = Stripe(data.publicKey);

        document.querySelector("#submitBtn").addEventListener("click", () => {
            var currentUrl = window.location.href;
            fetch(`/order/${currentUrl[currentUrl.length - 2]}/`)
                .then((request) => {
                    return request.json();
                })
                .then((data) => {
                    return stripe.redirectToCheckout({ sessionId: data.sessionId })
                });
        });
    });