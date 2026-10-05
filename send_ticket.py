import json
import httpx
from webhooks import compute_signature

payload = {
    "external_id": "HD-9000010",
    "customer_email": "jane@example.com",
    "subject": "Order 55123 arrived damaged",
    "body": "The item in order 55123 arrived with a cracked screen. I'd like a replacement or a refund.",
}

body = json.dumps(payload).encode()
headers = {"X-Signature": compute_signature(body), "Content-Type": "application/json"}

r = httpx.post("http://127.0.0.1:8000/webhooks/ticket", content=body, headers=headers)
print(r.status_code, r.json())