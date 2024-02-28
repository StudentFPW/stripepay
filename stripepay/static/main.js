fetch("/config/")
    .then((request) => {
        return request.json();
    })
    .then((data) => {
        const stripe = Stripe(data.publicKey);

        document.querySelector("#submitBtn").addEventListener("click", () => {
            fetch("/checkout/")
                .then((request) => {
                    return request.json();
                })
                .then((data) => {
                    return stripe.redirectToCheckout({ sessionId: data.sessionId })
                });
        });
    });