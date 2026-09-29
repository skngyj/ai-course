import base64
import json
import os

import requests
from flask import Flask, render_template, request


app = Flask(__name__)

EXPECTED_AMOUNT = 1000
TOSS_CONFIRM_URL = "https://api.tosspayments.com/v1/payments/confirm"


def error_result(status, code, message):
    return {"status": status, "code": code, "message": message}


@app.get("/")
def index():
    return render_template("index.html", amount=EXPECTED_AMOUNT)


@app.get("/fail")
def fail():
    return render_template(
        "fail.html",
        code=request.args.get("code", ""),
        message=request.args.get("message", ""),
        order_id=request.args.get("orderId", ""),
    )


@app.get("/success")
def success():
    payment_key = request.args.get("paymentKey", "")
    order_id = request.args.get("orderId", "")
    amount = request.args.get("amount", "")

    if amount != str(EXPECTED_AMOUNT):
        return render_template(
            "success.html",
            payment=None,
            raw=None,
            error=error_result(
                "-",
                "AMOUNT_MISMATCH",
                f"결제 금액이 {EXPECTED_AMOUNT}원과 달라 승인하지 않았습니다.",
            ),
        )

    secret_key = os.environ.get("TOSS_SECRET_KEY")
    if not secret_key:
        return render_template(
            "success.html",
            payment=None,
            raw=None,
            error=error_result(
                "-",
                "MISSING_SECRET_KEY",
                "TOSS_SECRET_KEY 환경 변수가 설정되지 않았습니다.",
            ),
        )

    authorization = "Basic " + base64.b64encode(f"{secret_key}:".encode()).decode()
    body = {"paymentKey": payment_key, "orderId": order_id, "amount": EXPECTED_AMOUNT}

    try:
        response = requests.post(
            TOSS_CONFIRM_URL,
            headers={"Authorization": authorization, "Content-Type": "application/json"},
            json=body,
            timeout=30,
        )
    except requests.RequestException as exc:
        return render_template(
            "success.html",
            payment=None,
            raw=None,
            error=error_result("-", "NETWORK_ERROR", str(exc)),
        )

    try:
        data = response.json()
    except ValueError:
        data = {"code": "-", "message": response.text[:500]}

    if response.ok:
        return render_template(
            "success.html",
            payment=data,
            raw=json.dumps(data, ensure_ascii=False, indent=2),
            error=None,
        )

    return render_template(
        "success.html",
        payment=None,
        raw=None,
        error=error_result(
            response.status_code,
            data.get("code", "-"),
            data.get("message", "-"),
        ),
    )


if __name__ == "__main__":
    app.run(debug=True)
