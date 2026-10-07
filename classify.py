from enum import Enum
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Category(str, Enum):
    BILLING = "billing"
    SHIPPING = "shipping"
    TECHNICAL = "technical"
    RETURNS = "returns"
    ACCOUNT = "account"
    
class Urgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    
    
class Classification(BaseModel):
    category: Category
    urgency: Urgency
    reason: str
    search_query: str
    
    
def classify(subject: str, body:str) -> Classification:
    INSTRUCTIONS = """You are a customer support ticket classifier.

Classify the ticket into one of: billing, shipping, technical, returns, account.
Judge the urgency as low, medium, high or urgent.
Give a one-sentence reason for your classification.

Also write a short search query — three to eight words — that would find the
help-documentation article answering this customer's problem. Describe the
problem itself. Do not include order numbers, dates, names or courier names."""

    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": INSTRUCTIONS},
                  {"role": "user", "content": f"Subject: {subject}\nBody: {body}"}],
        response_format= Classification
    )
    
    return response.choices[0].message.parsed


if __name__ == "__main__":
    result = classify(
        "Order 27597 hasn't arrived",
        "Order 27597 hasn't arrived and tracking hasn't updated in days.",
    )
    print(result)