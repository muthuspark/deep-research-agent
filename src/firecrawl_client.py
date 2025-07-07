import os
import requests
from dotenv import load_dotenv
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from asyncio_throttle import Throttler

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
    
    async def search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Search using Firecrawl API"""
        async with self.throttler:
            url = f"{self.base_url}/v1/search"
            
            payload = {
                "query": query,
                "limit": limit,
                "scrapeOptions": {
                    "formats": ["markdown"]
                }
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

# Global instance
firecrawl = FirecrawlClient()