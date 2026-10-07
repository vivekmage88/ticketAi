import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
chat_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_text(text: str) -> list[float]:
    response = chat_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    vectors = []
    for item in response.data:
        vectors.append(item.embedding)
    return vectors