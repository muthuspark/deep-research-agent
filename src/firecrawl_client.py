import os
import requests
from dotenv import load_dotenv
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from asyncio_throttle import Throttler
from datetime import datetime, timedelta

load_dotenv()

class FirecrawlClient:
    def __init__(self):
        self.api_key = os.getenv("FIRECRAWL_KEY", "")
        self.base_url = os.getenv("FIRECRAWL_BASE_URL", "https://api.firecrawl.dev")
        self.concurrency_limit = int(os.getenv("CONCURRENCY_LIMIT", "2"))
        self.throttler = Throttler(rate_limit=self.concurrency_limit)
        
        if not self.api_key:
            raise ValueError("FIRECRAWL_KEY environment variable is required")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _add_date_filters(self, query: str, days_back: Optional[int] = None) -> str:
        """Add date filters to the search query"""
        if days_back:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Add date range to query
            date_filter = f" after:{start_date.strftime('%Y-%m-%d')}"
            return f"{query}{date_filter}"
        
        return query
    
    async def search(
        self, 
        query: str, 
        limit: int = 5,
        prioritize_recent: bool = True,
        days_back: Optional[int] = None
    ) -> Dict[str, Any]:
        """Search using Firecrawl API with optional date filtering"""
        async with self.throttler:
            url = f"{self.base_url}/v1/search"
            
            # Enhance query with date filters if needed
            enhanced_query = query
            if prioritize_recent or days_back:
                if days_back:
                    enhanced_query = self._add_date_filters(query, days_back)
                else:
                    # Default to last 2 years for recent content
                    enhanced_query = self._add_date_filters(query, 730)
            
            payload = {
                "query": enhanced_query,
                "limit": limit,
                "scrapeOptions": {
                    "formats": ["markdown"],
                    "onlyMainContent": True,
                    "includeTags": ["time", "date", "published", "updated"]
                }
            }
            
            # Add search parameters for freshness
            if prioritize_recent:
                payload["searchOptions"] = {
                    "freshness": "recent",
                    "sortBy": "date"
                }
            
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(
                        url,
                        json=payload,
                        headers=self._get_headers(),
                        timeout=aiohttp.ClientTimeout(total=15)
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            # Sort results by freshness if available
                            if prioritize_recent and "data" in data:
                                data["data"] = self._sort_by_freshness(data["data"])
                            
                            return data
                        else:
                            print(f"Search failed with status {response.status}: {await response.text()}")
                            return {"data": []}
                except asyncio.TimeoutError:
                    print(f"Search timeout for query: {query}")
                    return {"data": []}
                except Exception as e:
                    print(f"Search error for query {query}: {e}")
                    return {"data": []}
    
    def _sort_by_freshness(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort search results by freshness/recency"""
        def extract_date_score(result: Dict[str, Any]) -> float:
            """Extract and score date information from result"""
            score = 0.0
            
            # Check for date in URL
            url = result.get("url", "")
            current_year = datetime.now().year
            
            for year in range(current_year, current_year - 5, -1):
                if str(year) in url:
                    score += (year - 2020) * 10  # More recent years get higher scores
                    break
            
            # Check for date keywords in title or content
            title = result.get("title", "").lower()
            content = result.get("markdown", "").lower()
            
            recent_keywords = ["2024", "2023", "latest", "recent", "new", "updated", "current"]
            for keyword in recent_keywords:
                if keyword in title:
                    score += 5
                elif keyword in content:
                    score += 1
            
            return score
        
        try:
            # Sort by date score (higher is more recent)
            sorted_results = sorted(results, key=extract_date_score, reverse=True)
            return sorted_results
        except Exception as e:
            print(f"Error sorting results by freshness: {e}")
            return results

# Global instance
firecrawl = FirecrawlClient()