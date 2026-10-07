import os
from embed import embed_text
from models import HelpDoc, DocChunk
from database import SessionLocal


def ingest_docs():
    titles = []
    info = []
    session = SessionLocal()
    try:
        for filename in os.listdir("help_docs"):
            if filename.endswith(".md"):
                path = os.path.join("help_docs", filename)
                with open(path, "r") as f:
                    text = f.read()
                    title, body = split_docs(text)
                    titles.append(title)
                    info.append(f"{title}\n\n {body}")
        vector = embed_text(info)
        for i in range(len(titles)):
            doc = HelpDoc(title=titles[i])
            session.add(doc)
            session.flush()
            chunk = DocChunk(
                doc_id=doc.id,
                heading=titles[i],
                content=info[i],
                embedding=vector[i],
            )
            session.add(chunk)
        session.commit()
    finally:
        session.close()
                
                
def split_docs(text: str):
    words = text.split("\n", 1)
    title = words[0].strip()
    body = words[1].strip() if len(words) > 1 else ""
    return title, body
                
if __name__ == "__main__":
    ingest_docs()