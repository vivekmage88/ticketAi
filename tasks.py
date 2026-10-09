from celery_app import celery_app
from database import SessionLocal
from models import Ticket
from classify import classify

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff= 2, retry_backoff_max=600, max_retries=5, retry_jitter=True)
def process_ticket(self, ticket_id: int):
    db = SessionLocal()
    try:
        ticket = db.get(Ticket, ticket_id)
        if ticket is None:
            print(f"Ticket with ID {ticket_id} not found.")
            return

        # Simulate processing the ticket (e.g., categorization, urgency assessment)
        result = classify(ticket.subject, ticket.body)
        ticket.category = result.category
        ticket.urgency = result.urgency
        ticket.status = "processed"
        ticket.search_query = result.search_query
        ticket.classification_reason = result.reason
        db.commit()
        print(f"Ticket {ticket_id} processed successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error processing ticket {ticket_id}: {e}")
        raise
    finally:
        db.close()