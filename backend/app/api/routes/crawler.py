"""Crawler management API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.crawler import CrawlerManager

router = APIRouter(prefix="/api/v1/crawler", tags=["crawler"])


# Pydantic schemas
class CrawlerRunRequest(BaseModel):
    """Request schema for triggering a crawler run"""
    domain: Optional[str] = Field(None, description="Specific domain to crawl (e.g. AI, marketing, chinese_classics, speaking). If omitted, all crawlers run.")


class CrawlResultItem(BaseModel):
    """A single crawl result"""
    url: str
    title: str
    content: str
    domain: str
    metadata: Optional[dict]
    crawled_at: Optional[str]


class CrawlerRunResponse(BaseModel):
    """Response after triggering a crawler run"""
    status: str
    domain: Optional[str]
    results_count: int
    results: List[CrawlResultItem]
    triggered_at: datetime


class CrawlerStatusResponse(BaseModel):
    """Response schema for crawler status"""
    available_crawlers: List[dict]
    is_running: bool
    last_run: Optional[str]


class CrawlerResultsResponse(BaseModel):
    """Response schema for recent crawl results"""
    results: List[CrawlResultItem]
    total: int


# Module-level state for tracking crawler runs
_crawler_state = {
    "is_running": False,
    "last_run": None,
    "last_results": [],
}


@router.post("/run", response_model=CrawlerRunResponse)
async def trigger_crawler_run(
    request: CrawlerRunRequest = CrawlerRunRequest(),
    db: Session = Depends(get_db),
):
    """
    Trigger a crawler run.

    Can run all crawlers (when domain is omitted) or a specific domain's
    crawler.  Returns the crawl results.

    Only one crawl run is allowed at a time; concurrent requests receive
    a 409 Conflict response.
    """
    if _crawler_state["is_running"]:
        raise HTTPException(status_code=409, detail="A crawler run is already in progress")

    _crawler_state["is_running"] = True

    try:
        manager = CrawlerManager()

        if request.domain:
            results = await manager.run_crawler_by_domain(request.domain)
        else:
            results = await manager.run_all_crawlers()

        crawl_items = [
            CrawlResultItem(
                url=r.url,
                title=r.title,
                content=r.content[:500],  # Truncate for response
                domain=r.domain,
                metadata=r.metadata,
                crawled_at=r.crawled_at.isoformat() if r.crawled_at else None,
            )
            for r in results
        ]

        _crawler_state["last_run"] = datetime.now().isoformat()
        _crawler_state["last_results"] = crawl_items

        return CrawlerRunResponse(
            status="completed",
            domain=request.domain,
            results_count=len(crawl_items),
            results=crawl_items,
            triggered_at=datetime.now(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crawler run failed: {str(e)}")
    finally:
        _crawler_state["is_running"] = False


@router.get("/status", response_model=CrawlerStatusResponse)
async def get_crawler_status():
    """
    Get the current crawler system status.

    Returns a list of available crawlers and whether a run is in
    progress.
    """
    manager = CrawlerManager()
    crawlers_info = [
        {
            "name": c.name,
            "domain": c.domain,
            "type": c.__class__.__name__,
        }
        for c in manager.crawlers
    ]

    return CrawlerStatusResponse(
        available_crawlers=crawlers_info,
        is_running=_crawler_state["is_running"],
        last_run=_crawler_state["last_run"],
    )


@router.get("/results", response_model=CrawlerResultsResponse)
async def get_crawler_results(
    domain: Optional[str] = None,
    limit: int = 20,
):
    """
    Get results from the most recent crawler run.

    Query parameters:
    - domain: Filter results by domain
    - limit: Maximum results to return (default 20, max 100)
    """
    results = _crawler_state["last_results"]

    if domain:
        results = [r for r in results if r.domain == domain]

    return CrawlerResultsResponse(
        results=results[:limit],
        total=len(results),
    )
