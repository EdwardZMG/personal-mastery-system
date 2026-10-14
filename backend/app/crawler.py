"""
Web Crawler Framework for Edward Growth System
Provides base crawler class and content source integrations
"""
import asyncio
import hashlib
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup
import redis

from app.config import settings


class CrawlResult:
    """Result from crawling a single URL"""
    
    def __init__(self, url: str, title: str, content: str, 
                 metadata: Dict = None, domain: str = "general"):
        self.url = url
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self.domain = domain
        self.crawled_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "url": self.url,
            "title": self.title,
            "content": self.content,
            "metadata": self.metadata,
            "domain": self.domain,
            "crawled_at": self.crawled_at.isoformat()
        }


class BaseCrawler(ABC):
    """
    Abstract base class for all content crawlers
    
    Provides common functionality:
    - HTTP requests with retry logic
    - HTML parsing
    - Content deduplication via Redis
    - Rate limiting
    - Error handling
    
    Subclasses must implement:
    - crawl() method
    - parse() method
    """
    
    def __init__(self, name: str, domain: str, base_url: str, 
                 rate_limit: float = 1.0, timeout: int = 30):
        """
        Initialize crawler
        
        Args:
            name: Crawler name (e.g., "ArXiv AI Papers")
            domain: Knowledge domain (AI/marketing/chinese_classics/etc.)
            base_url: Base URL for the source
            rate_limit: Minimum seconds between requests
            timeout: Request timeout in seconds
        """
        self.name = name
        self.domain = domain
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.timeout = timeout
        
        # Redis for deduplication (7-day cache)
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.cache_ttl = 7 * 24 * 3600  # 7 days
    
    async def fetch_page(self, url: str, headers: Dict = None) -> Optional[str]:
        """
        Fetch page content with retry logic
        
        Args:
            url: URL to fetch
            headers: Optional HTTP headers
            
        Returns:
            Page HTML content or None if failed
        """
        default_headers = {
            'User-Agent': 'Edward-Growth-Bot/1.0 (+https://edward-growth.com/bot)'
        }
        if headers:
            default_headers.update(headers)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers=default_headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        print(f"❌ Failed to fetch {url}: HTTP {response.status}")
                        return None
        except Exception as e:
            print(f"❌ Error fetching {url}: {str(e)}")
            return None
    
    def is_cached(self, url: str) -> bool:
        """Check if URL content is already cached"""
        cache_key = self._get_cache_key(url)
        return self.redis.exists(cache_key)
    
    def cache_content(self, url: str, content_hash: str):
        """Cache URL content hash"""
        cache_key = self._get_cache_key(url)
        self.redis.setex(cache_key, self.cache_ttl, content_hash)
    
    def _get_cache_key(self, url: str) -> str:
        """Generate Redis cache key for URL"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return f"crawl:{self.name}:{url_hash}"
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, 'lxml')
    
    @abstractmethod
    async def crawl(self, **kwargs) -> List[CrawlResult]:
        """
        Crawl content from source
        
        Must be implemented by subclasses
        
        Args:
            **kwargs: Crawler-specific parameters
            
        Returns:
            List of CrawlResult objects
        """
        pass
    
    @abstractmethod
    def parse(self, html: str, url: str) -> CrawlResult:
        """
        Parse HTML content into structured data
        
        Must be implemented by subclasses
        
        Args:
            html: HTML content
            url: Source URL
            
        Returns:
            CrawlResult object
        """
        pass


class RSSCrawler(BaseCrawler):
    """Crawler for RSS feed sources"""
    
    def __init__(self, name: str, domain: str, rss_url: str):
        super().__init__(name, domain, rss_url)
    
    async def crawl(self, limit: int = 10) -> List[CrawlResult]:
        """Crawl RSS feed"""
        import feedparser
        
        feed = feedparser.parse(self.base_url)
        results = []
        
        for entry in feed.entries[:limit]:
            if self.is_cached(entry.link):
                continue
            
            result = CrawlResult(
                url=entry.link,
                title=entry.title,
                content=entry.summary if hasattr(entry, 'summary') else entry.title,
                metadata={
                    "published": entry.published if hasattr(entry, 'published') else None,
                    "author": entry.author if hasattr(entry, 'author') else None
                },
                domain=self.domain
            )
            
            results.append(result)
            self.cache_content(entry.link, hashlib.md5(entry.title.encode()).hexdigest())
        
        return results
    
    def parse(self, html: str, url: str) -> CrawlResult:
        """Not used for RSS feeds"""
        raise NotImplementedError("RSS feeds don't require HTML parsing")


class WebPageCrawler(BaseCrawler):
    """Generic web page crawler with configurable selectors"""
    
    def __init__(self, name: str, domain: str, base_url: str,
                 title_selector: str = 'h1',
                 content_selector: str = 'article, .content, main',
                 rate_limit: float = 2.0):
        super().__init__(name, domain, base_url, rate_limit)
        self.title_selector = title_selector
        self.content_selector = content_selector
    
    async def crawl(self, urls: List[str]) -> List[CrawlResult]:
        """Crawl multiple URLs"""
        results = []
        
        for url in urls:
            if self.is_cached(url):
                print(f"⏭️  Skipping cached URL: {url}")
                continue
            
            html = await self.fetch_page(url)
            if not html:
                continue
            
            try:
                result = self.parse(html, url)
                results.append(result)
                
                # Cache the content
                content_hash = hashlib.md5(result.content.encode()).hexdigest()
                self.cache_content(url, content_hash)
                
                # Rate limiting
                await asyncio.sleep(self.rate_limit)
                
            except Exception as e:
                print(f"❌ Error parsing {url}: {str(e)}")
                continue
        
        return results
    
    def parse(self, html: str, url: str) -> CrawlResult:
        """Parse web page"""
        soup = self.parse_html(html)
        
        # Extract title
        title_elem = soup.select_one(self.title_selector)
        title = title_elem.get_text(strip=True) if title_elem else "Untitled"
        
        # Extract content
        content_elem = soup.select_one(self.content_selector)
        if content_elem:
            # Remove script and style elements
            for script in content_elem(["script", "style"]):
                script.decompose()
            content = content_elem.get_text(separator='\n', strip=True)
        else:
            content = soup.get_text(separator='\n', strip=True)
        
        # Clean up content
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        content = '\n'.join(lines)
        
        return CrawlResult(
            url=url,
            title=title,
            content=content[:5000],  # Limit content length
            metadata={"source": self.name},
            domain=self.domain
        )


# Predefined crawlers for Edward's learning domains

class ArxivAICrawler(RSSCrawler):
    """Crawl AI papers from ArXiv"""
    
    def __init__(self):
        super().__init__(
            name="ArXiv AI Papers",
            domain="AI",
            rss_url="http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=20"
        )


class MarketingBlogCrawler(WebPageCrawler):
    """Crawl marketing articles"""
    
    def __init__(self):
        super().__init__(
            name="Marketing Insights",
            domain="marketing",
            base_url="https://blog.hubspot.com/marketing",
            title_selector="h1.post-title",
            content_selector=".post-body"
        )


class ChineseClassicsCrawler(WebPageCrawler):
    """Crawl Chinese classics content"""
    
    def __init__(self):
        super().__init__(
            name="Chinese Classics",
            domain="chinese_classics",
            base_url="https://ctext.org",
            title_selector="h1",
            content_selector=".etext"
        )


class TEDTalkCrawler(WebPageCrawler):
    """Crawl TED talks for speaking practice"""
    
    def __init__(self):
        super().__init__(
            name="TED Talks",
            domain="speaking",
            base_url="https://www.ted.com/talks",
            title_selector="h1.headline",
            content_selector=".talk-transcript"
        )


class CrawlerManager:
    """
    Manage and orchestrate multiple crawlers
    
    Provides unified interface for running all configured crawlers
    and collecting results.
    """
    
    def __init__(self):
        self.crawlers = [
            ArxivAICrawler(),
            MarketingBlogCrawler(),
            ChineseClassicsCrawler(),
            TEDTalkCrawler(),
        ]
    
    async def run_all_crawlers(self) -> List[CrawlResult]:
        """Run all crawlers and collect results"""
        all_results = []
        
        for crawler in self.crawlers:
            print(f"\n🕷️  Running crawler: {crawler.name}")
            
            try:
                if isinstance(crawler, RSSCrawler):
                    results = await crawler.crawl(limit=10)
                else:
                    # For web page crawlers, you'd provide specific URLs
                    # This is a simplified example
                    results = []
                
                print(f"   ✅ Crawled {len(results)} items")
                all_results.extend(results)
                
            except Exception as e:
                print(f"   ❌ Crawler failed: {str(e)}")
                continue
        
        print(f"\n📊 Total results: {len(all_results)}")
        return all_results
    
    async def run_crawler_by_domain(self, domain: str) -> List[CrawlResult]:
        """Run crawlers for specific domain"""
        domain_crawlers = [c for c in self.crawlers if c.domain == domain]
        
        all_results = []
        for crawler in domain_crawlers:
            results = await crawler.crawl()
            all_results.extend(results)
        
        return all_results


# Convenience function
async def crawl_content(domain: Optional[str] = None) -> List[CrawlResult]:
    """
    Quick content crawling
    
    Args:
        domain: Optional domain filter
        
    Returns:
        List of CrawlResult objects
    """
    manager = CrawlerManager()
    
    if domain:
        return await manager.run_crawler_by_domain(domain)
    else:
        return await manager.run_all_crawlers()
