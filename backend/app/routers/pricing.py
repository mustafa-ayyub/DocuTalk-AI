import os
import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/pricing", tags=["pricing"])

stripe.api_key = os.getenv("STRIPE_API_KEY")


class CheckoutSessionRequest(BaseModel):
    success_url: str | None = None
    cancel_url: str | None = None


class CheckoutSessionResponse(BaseModel):
    url: str


@router.post("/checkout", response_model=CheckoutSessionResponse)
def create_checkout_session(req: CheckoutSessionRequest):
    try:
        environment = os.getenv("ENVIRONMENT", "local")
        if not req.success_url or not req.cancel_url:
            if environment == "local":
                success_url = os.getenv("LOCAL_SUCCESS_URL")
                cancel_url = os.getenv("LOCAL_CANCEL_URL")
            else:
                success_url = os.getenv("DEPLOYED_SUCCESS_URL")
                cancel_url = os.getenv("DEPLOYED_CANCEL_URL")
        else:
            success_url = req.success_url
            cancel_url = req.cancel_url

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "recurring": {"interval": "month"},
                        "product_data": {
                            "name": "Premium Subscription",
                            "description": "Get unlimited access to all advanced features.",
                        },
                        "unit_amount": 1500,
                    },
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return CheckoutSessionResponse(url=session.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

