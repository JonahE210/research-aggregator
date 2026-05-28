"""Manual dev trigger for the ingestion pipeline.

Usage (from repo root):
    python scripts/run_ingest.py
"""
import asyncio

from app.config import settings
from app.db import init_db
from app.ingestion.pipeline import run_pipeline


def main() -> None:
    init_db()  # dev convenience; Alembic migrations replace this in Phase 5
    summary = asyncio.run(run_pipeline())
    print(f"Ingestion summary: {summary}")


if __name__ == "__main__":
    main()