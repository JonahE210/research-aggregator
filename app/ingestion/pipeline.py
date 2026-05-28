"""
=== YOUR TASK — Phase 1, Task 2 ===

Orchestrate the full pipeline: fetch -> parse -> dedup/upsert -> store.

Flow:
    1. pages = await fetch_recent(category, pages)        # from arxiv_client
    2. papers = [p for xml in pages for p in parse_papers(xml)]   # from parser
    3. upsert papers into Postgres, skipping ones already seen.

The dedup is the interesting part. Use an atomic Postgres upsert so reruns are
idempotent (running twice adds zero duplicates):

    from sqlalchemy.dialects.postgresql import insert
    rows = [{"arxiv_id": p.arxiv_id, "title": p.title, ...} for p in papers]
    stmt = insert(Paper).values(rows).on_conflict_do_nothing(index_elements=["arxiv_id"])
    with get_session() as session:
        result = session.execute(stmt)
        session.commit()

Return a summary dict so run_ingest.py can print it:
    {"fetched": ..., "parsed": ..., "inserted": ..., "skipped": ...}

Acceptance test:
- Run once -> table fills, summary shows inserted > 0.
- Run again immediately -> inserted == 0 (everything skipped). THIS is the demo.
"""


async def run_pipeline() -> dict:
    raise NotImplementedError("Implement me. Write the dedup logic yourself — it's the whole point.")

