from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

# DELIBERATE DECISION (worth saying in an interview):
# The engine is SYNC even though the API layer is async. Phase 1 ingestion is a
# rate-limited batch job — the bottleneck is the external arXiv API (~1 req / 3s),
# not the database. Sync SQLAlchemy keeps the batch code simple. We introduce
# async DB sessions in the API layer (Phase 2+) where request concurrency
# actually matters. Pick complexity where it pays off, not everywhere.
engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session() -> Session:
    """Return a new session. Caller owns the commit/close (use a `with` block)."""
    return SessionLocal()


def init_db() -> None:
    """Create tables from the models.

    Dev convenience only. In Phase 5 this gets replaced by Alembic migrations,
    which is what you'd use in any real codebase. create_all is fine for now.
    """
    from app.models.papers import Base

    Base.metadata.create_all(engine)
