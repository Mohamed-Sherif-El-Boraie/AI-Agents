from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]))

import requests
from typing import  List, Any
import traceback

from bs4 import BeautifulSoup
from typing import List
from tavily import TavilyClient

from src.models import Finding

from config.config import *
from config.logger import get_logger

log = get_logger("web_search_tool")

# Tavily Search Client Setup
def get_search_client() -> TavilyClient:
    api_key = TAVILY_API_KEY
    return TavilyClient(api_key=api_key)


def web_search(query: str,  max_items: int = 1) -> List[Finding]:
    """
    Perform a web search using the Tavily API.

    Args:
        query: The search query string.
        max_itmes: Maximum number of search results to return.

    Returns:
        The search results or an error message.
    """
    search_client = get_search_client()

    if search_client:
            try:
                # Perform search using Tavily
                res = search_client.search(query=query, max_results=max_items)
                
                findings: List[Finding] = []
                # Parsing through search's performed output
                for item in (res.get("results") or [])[:max_items]:
                    url = item.get("url")
                    snippet = item.get("content") or item.get("title") or ""
                    if snippet:
                        findings.append(Finding(topic=query, source_url=url, snippet=snippet.strip()))
                if findings:
                    return findings
                log.info("No results found")
            except Exception as e:
                log.error(f"Tavily search error: {e}")
                log.debug(traceback.format_exc())



