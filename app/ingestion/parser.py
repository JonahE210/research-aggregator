"""
=== YOUR TASK — Phase 1, Task 1 ===

Turn raw arXiv Atom XML into a list[Paper].

Recommended tool: feedparser
    feed = feedparser.parse(xml)   # feed.entries is a list of entries

For each entry you'll want:
    entry.title                    -> title
    entry.summary                  -> abstract
    entry.authors                  -> list of {'name': ...} dicts -> authors
    entry.published                -> ISO string -> parse to datetime -> published_at
    entry.link                     -> url
    entry.tags                     -> list of {'term': ...} dicts -> categories
    entry.id                       -> 'http://arxiv.org/abs/2401.01234v1'
                                      -> strip to '2401.01234' for arxiv_id

Rules:
- Be defensive. A single malformed entry should be skipped (log it), not crash
  the whole batch. Wrap per-entry parsing in try/except.
- Return real Paper objects (don't set id or ingested_at — the DB handles those).

Acceptance test:
- Feed it one page of XML -> get back a list[Paper], every field populated.
- Feed it XML with one broken entry -> that entry is skipped, the rest parse.
"""
import asyncio

import feedparser

from app.ingestion.arxiv_client import fetch_recent
from app.models.papers import Paper
from logging import getLogger
import datetime
logger = getLogger(__name__)


def parse_papers(xml: str) -> list[Paper]:

    feed = feedparser.parse(xml)
    res = []
    for entry in feed.entries:
        try:
            paper = Paper()

            #Paper id truncation and split since we need to return the id at the end of url without the suffix
            full_id_with_suffix = entry.get('id', '')
            paper_suffix = full_id_with_suffix.split('/abs/')[-1]
            paper.arxiv_id = paper_suffix.rsplit('v', 1)[0]

            #These are fine
            paper.title = entry.get('title', '')
            paper.abstract = entry.get('summary', '')
            paper.url = entry.get('link', '')

            #Since entry.get returns a list of dicts, we need to iterate over list and extract dict values from keys
            author_dict_list = entry.get('authors', [])
            authors = []
            for author_dict in author_dict_list:
                authors.append(author_dict['name'])
            paper.authors = authors

            #Same logic as above ^^
            categories_dict_list = entry.get('tags', [])
            categories = []
            for categories_dict in categories_dict_list:
                categories.append(categories_dict['term'])
            paper.categories = categories

            #Parsing date requires a datetime.datetime object
            iso = entry.get('published', '')
            paper.published_at = datetime.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")

            res.append(paper)
        except Exception as e:
            logger.error(e)
    return res

if __name__ == "__main__":
    papers_list = asyncio.run(fetch_recent('cs.AI', 1))
    for p in papers_list:
        pages = parse_papers(p)
        for t in pages:
            print(t)