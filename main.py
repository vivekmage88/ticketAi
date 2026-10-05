import json
from fastapi import FastAPI, Request, HTTPException, Header, Depends
from pydantic import BaseModel, Field, EmailStr, ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import Ticket
from webhooks import verify_signature
from tasks import process_ticket

app = FastAPI(title="Ticket AI Webhook Receiver", version="1.0")

class TicketPayload(BaseModel):
    external_id: str = Field(min_length=1, max_length=100)
    customer_email: EmailStr
    subject: str = Field(min_length=1, max_length=300)
    body: str = Field(min_length=1)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/webhooks/ticket", status_code=202)
async def receive_ticket(
    request: Request,
    x_signature: str | None = Header(default=""),
    db: Session = Depends(get_db)
    ):
    body = await request.body()
    
    if not verify_signature(body, x_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Malformed JSON")

    data = TicketPayload.model_validate(payload)

    ticket = Ticket(
        external_id=data.external_id,
        customer_email=data.customer_email,
        subject=data.subject,
        body=data.body,
        status="new",
    )
    db.add(ticket)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"status": "duplicate", "external_id": data.external_id}
    
    process_ticket.delay(ticket.id)
    
    return {"status": "accepted", "ticket_id": ticket.id}