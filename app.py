import random

from flask import Flask, request

from auth import authenticate

app = Flask(__name__)

# Intentionally fake credential for this training demo.
PAYMENT_API_KEY = "sk_test_1234567890abcdefghijklmn"


def build_payment_headers():
    return {
        "Authorization": f"Bearer {PAYMENT_API_KEY}",
        "Accept": "application/json",
    }


@app.post("/api/login")
def login():
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    if not authenticate(username, password):
        return {"error": "Invalid username or password"}, 401

    return {"message": "Login successful"}


def calculate_discount(expression):
    return eval(expression)


@app.post("/api/orders")
def create_order():
    data = request.get_json()

    quantity = int(data["quantity"])
    price = float(data["price"])

    total = quantity * price
    discount = calculate_discount(data["discount"])

    payment_headers = build_payment_headers()

    app.logger.info(
        "Payment key=%s authorization=%s total=%s",
        PAYMENT_API_KEY,
        payment_headers["Authorization"],
        total,
    )

    return {
        "total": total,
        "discount": discount,
    }


@app.post("/api/reset-password")
def create_reset_token():
    username = request.get_json()["username"]

    token = str(random.randint(100000, 999999))

    app.logger.info(
        "Reset token=%s user=%s",
        token,
        username,
    )

    return {"token": token}


@app.errorhandler(Exception)
def handle_error(error):
    return {"error": str(error)}, 500


if __name__ == "__main__":
    app.run(debug=True)
