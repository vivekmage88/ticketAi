from embed import embed_text
from models import DocChunk
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import SessionLocal

def search_docs(db : Session,
    query: str,
    k: int = 3,
    max_distance: float = 0.6) -> list[tuple[DocChunk,  float]]:
    
    search_vector = embed_text([query])[0]
    distance = DocChunk.embedding.cosine_distance(search_vector)
    stmt = select(DocChunk, distance.label("distance")).order_by(distance).limit(k)
    rows = db.execute(stmt).all()
    
    matches = []
    for row in rows:
        chunk, dist = row
        if dist <= max_distance:
            matches.append((chunk, dist))
    return matches

if __name__ == "__main__":
    db = SessionLocal()    
    for q in [
        "my package arrived broken",
        "how long until I get my money back",
        "charged twice for one order",
        "what is the capital of France",
    ]:
        print(f"\n{q}")
        for chunk, dist in search_docs(db, q, k=3, max_distance=2.0):
            print(f"  {round(dist, 3)}  {chunk.heading}")
    db.close()
    