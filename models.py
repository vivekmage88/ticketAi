from datetime import datetime
from sqlalchemy import Text, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from database import Base


class Ticket(Base):
    __tablename__ = "tickets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(100), unique = True, index=True)
    customer_email: Mapped[str] = mapped_column(String(200), index=True)
    subject: Mapped[str] = mapped_column(String(300))
    body: Mapped[str] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(20), default = "new", index=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    urgency: Mapped[str | None] = mapped_column(String(20), nullable=True)
    team: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    drafts: Mapped[list["Draft"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")
    
    
    
class Draft(Base):
    __tablename__ = "drafts"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete= "CASCADE"), index=True)
    body: Mapped[str] = mapped_column(Text)
    sources: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    ticket: Mapped["Ticket"] = relationship(back_populates="drafts")
    
class HelpDoc(Base):
    __tablename__ = "help_docs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    chunks: Mapped[list["DocChunk"]] = relationship(
        back_populates="doc", cascade="all, delete-orphan"
    )
    
class DocChunk(Base):
    __tablename__ = "doc_chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(
        ForeignKey("help_docs.id", ondelete="CASCADE"), index=True
    )
    heading: Mapped[str | None] = mapped_column(String(300), nullable=True)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))

    doc: Mapped["HelpDoc"] = relationship(back_populates="chunks")