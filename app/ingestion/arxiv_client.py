import asyncio
import httpx

ARXIV_API = "https://export.arxiv.org/api/query"
MIN_INTERVAL = 3.0  # arXiv courtesy limit: ~1 req / 3s

async def fetch_page(client: httpx.AsyncClient, category: str,
                     start: int, max_results: int = 100) -> str:
    params = {
        "search_query": f"cat:{category}",
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    for attempt in range(4):
        try:
            resp = await client.get(ARXIV_API, params=params, timeout=30)
            resp.raise_for_status()
            return resp.text  # raw Atom XML, parsed in parser.py
        except (httpx.HTTPStatusError, httpx.TransportError):
            if attempt == 3:
                raise
            await asyncio.sleep(2 ** attempt)  # exponential backoff
    raise RuntimeError("unreachable")

async def fetch_recent(category: str, pages: int = 3) -> list[str]:
    pages_xml = []
    async with httpx.AsyncClient() as client:
        for i in range(pages):
            xml = await fetch_page(client, category, start=i * 100)
            pages_xml.append(xml)
            await asyncio.sleep(MIN_INTERVAL)  # respect the limit
    return pages_xml