import os
import hmac
import hashlib
import base64
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dev-secret")


def compute_signature(body: bytes) -> str:
    digest = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def verify_signature(body: bytes, received: str) -> bool:
    if not received:
        return False
    return hmac.compare_digest(compute_signature(body), received)