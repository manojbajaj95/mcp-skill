"""Application for interacting with Parallelsearch via MCP."""
from typing import Any
from fastmcp import Client
from mcp_skill.auth import OAuth
import json

class ParallelsearchApp:
    """
    Application for interacting with Parallelsearch via MCP.
    Provides tools to interact with tools: web_search_preview, web_fetch.
    """

    def __init__(self, url: str = "https://search-mcp.parallel.ai/mcp", auth=None) -> None:
        self.url = url
        self._oauth_auth = auth

    def _get_client(self) -> Client:
        oauth = self._oauth_auth or OAuth()
        return Client(self.url, auth=oauth)

    async def web_search_preview(self, objective: str, search_queries: list[str]) -> dict[str, Any]:
        """
        Purpose: Perform web searches and return results in an LLM-friendly format and with parameters tuned for LLMs.


        Args:
            objective: Natural-language description of what the web search is trying to find.
Try to make the search objective atomic, looking for a specific piece of information. May include guidance about preferred sources or freshness.
            search_queries: (optional) List of keyword search queries of 1-6
 words, which may include search operators. The search queries should be related to the
 objective. Limited to 5 entries of 200 characters each.

        Returns:
            Tool execution result

        Tags:
            web, search, preview
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["objective"] = objective
            call_args["search_queries"] = search_queries
            result = await client.call_tool("web_search_preview", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def web_fetch(self, urls: list[str], objective: str | None = None) -> dict[str, Any]:
        """
        Purpose: Fetch and extract relevant content from
specific web URLs.

Ideal Use Cases:
- Extracting content from specific URLs you've already identified
- Exploring URLs returned by a web search in greater depth


        Args:
            urls: List of URLs to extract content from. Must be valid
HTTP/HTTPS URLs. Maximum 10 URLs per request.
            objective: Natural-language description of what
information you're looking for from the URLs. Limit to 200 characters.

        Returns:
            Tool execution result

        Tags:
            web, fetch
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["urls"] = urls
            if objective is not None:
                call_args["objective"] = objective
            result = await client.call_tool("web_fetch", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    def list_tools(self):
        return [self.web_search_preview, self.web_fetch]
