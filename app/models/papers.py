from datetime import datetime
from sqlalchemy import String, DateTime, Text, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Paper(Base):
    __tablename__ = "papers"

    id: Mapped[int] = mapped_column(primary_key=True)
    arxiv_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    title: Mapped[str] = mapped_column(Text)
    abstract: Mapped[str] = mapped_column(Text)
    authors: Mapped[list[str]] = mapped_column(ARRAY(String))
    categories: Mapped[list[str]] = mapped_column(ARRAY(String))
    url: Mapped[str] = mapped_column(String(512))
    published_at: Mapped[datetime] = mapped_column(DateTime)
    ingested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    # embedding column added in Phase 2 via pgvector migration