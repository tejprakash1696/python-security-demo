import os
import secrets
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Flask, g, request
from werkzeug.exceptions import HTTPException

from auth import authenticate

app = Flask(__name__)

PAYMENT_API_KEY = os.environ.get("PAYMENT_API_KEY")

MIN_QUANTITY = 1
MAX_QUANTITY = 999
MAX_PRICE = 10_000.00

reset_requests = {}

ORDERS = {
    101: {
        "owner": "alice",
        "total": 200,
    },
    102: {
        "owner": "bob",
        "total": 350,
    },
}


def build_payment_headers():
    if not PAYMENT_API_KEY:
        raise RuntimeError("Payment API key is missing")

    return {
        "Authorization": f"Bearer {PAYMENT_API_KEY}",
        "Accept": "application/json",
    }


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        credentials = request.authorization

        if (
                not credentials
                or not credentials.username
                or not credentials.password
                or not authenticate(
            credentials.username,
            credentials.password,
        )
        ):
            return {"error": "Authentication required"}, 401

        g.current_user = credentials.username
        return view(*args, **kwargs)

    return wrapper


@app.get("/api/login")
@login_required
def login():
    return {
        "message": "Login successful",
        "username": g.current_user,
    }


def calculate_discount(discount_type, total):
    if discount_type == "standard":
        return total * 0.10

    if discount_type == "premium":
        return total * 0.20

    raise ValueError("Unsupported discount type")


@app.post("/api/orders")
@login_required
def create_order():
    data = request.get_json(silent=True) or {}

    try:
        quantity = int(data["quantity"])
        price = float(data["price"])
        discount_type = data["discount"]
    except (KeyError, TypeError, ValueError):
        return {"error": "Invalid order input"}, 400

    if not MIN_QUANTITY <= quantity <= MAX_QUANTITY:
        return {"error": "Invalid quantity"}, 400

    if not 0 < price <= MAX_PRICE:
        return {"error": "Invalid price"}, 400

    total = quantity * price

    try:
        discount = calculate_discount(discount_type, total)
    except ValueError:
        return {"error": "Invalid discount type"}, 400

    build_payment_headers()

    app.logger.info("Order processed for user=%s", g.current_user)

    return {
        "total": total,
        "discount": discount,
        "final_total": total - discount,
    }


@app.get("/api/orders/<int:order_id>")
@login_required
def get_order(order_id):
    order = ORDERS.get(order_id)

    if not order:
        return {"error": "Order not found"}, 404

    if order["owner"] != g.current_user:
        return {"error": "Access denied"}, 403

    return order


@app.post("/api/reset-password")
@login_required
def create_reset_token():
    username = g.current_user

    token = secrets.token_urlsafe(32)

    reset_requests[username] = {
        "token": token,
        "expires_at": (
                datetime.now(timezone.utc)
                + timedelta(minutes=15)
        ),
    }
    # In production, deliver the reset token through a trusted channel such as email.
    # Do not return or log the token.

    app.logger.info(
        "Password reset requested for user=%s",
        username,
    )

    return {
        "message": "Password reset requested"
    }


@app.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, HTTPException):
        return {
            "error": error.name
        }, error.code

    app.logger.exception(
        "Unhandled application error"
    )

    return {
        "error": "Internal server error"
    }, 500
