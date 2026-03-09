"""Application for interacting with Context7 via MCP."""
from typing import Any
from fastmcp import Client
import json
import warnings

class Context7App:
    """
    Application for interacting with Context7 via MCP.
    Provides tools to interact with tools: resolve-library-id, query-docs.
    """

    def __init__(self, url: str = "https://mcp.context7.com/mcp", auth=None) -> None:
        self.url = url
        if auth is not None:
            warnings.warn(
                "This server requires no authentication; the 'auth' argument will be ignored.",
                UserWarning,
                stacklevel=2,
            )

    def _get_client(self) -> Client:
        return Client(self.url)

    async def resolve_library_id(self, libraryName: str, query: str) -> dict[str, Any]:
        """
        Resolves a package/product name to a Context7-compatible library ID and returns matching libraries.

You MUST call this function before 'Query Documentation' tool to obtain a valid Context7-compatible library ID UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

Each result includes:
- Library ID: Context7-compatible identifier (format: /org/project)
- Name: Library or package name
- Description: Short summary
- Code Snippets: Number of available code examples
- Source Reputation: Authority indicator (High, Medium, Low, or Unknown)
- Benchmark Score: Quality indicator (100 is the highest score)
- Versions: List of versions if available. Use one of those versions if the user provides a version in their query. The format of the version is /org/project/version.

For best results, select libraries based on name match, source reputation, snippet coverage, benchmark score, and relevance to your use case.

Selection Process:
1. Analyze the query to understand what library/package the user is looking for
2. Return the most relevant match based on:
- Name similarity to the query (exact matches prioritized)
- Description relevance to the query's intent
- Documentation coverage (prioritize libraries with higher Code Snippet counts)
- Source reputation (consider libraries with High or Medium reputation more authoritative)
- Benchmark Score: Quality indicator (100 is the highest score)

Response Format:
- Return the selected library ID in a clearly marked section
- Provide a brief explanation for why this library was chosen
- If multiple good matches exist, acknowledge this but proceed with the most relevant one
- If no good matches exist, clearly state this and suggest query refinements

For ambiguous queries, request clarification before proceeding with a best-guess match.

IMPORTANT: Do not call this tool more than 3 times per question. If you cannot find what you need after 3 calls, use the best result you have.

        Args:
            libraryName: Library name to search for and retrieve a Context7-compatible library ID.
            query: The question or task you need help with. This is used to rank library results by relevance to what the user is trying to accomplish. The query is sent to the Context7 API for processing. Do not include any sensitive or confidential information such as API keys, passwords, credentials, personal data, or proprietary code in your query.

        Returns:
            Tool execution result

        Tags:
            resolve, library, id
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["libraryName"] = libraryName
            call_args["query"] = query
            result = await client.call_tool("resolve-library-id", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def query_docs(self, libraryId: str, query: str) -> dict[str, Any]:
        """
        Retrieves and queries up-to-date documentation and code examples from Context7 for any programming library or framework.

You must call 'Resolve Context7 Library ID' tool first to obtain the exact Context7-compatible library ID required to use this tool, UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

IMPORTANT: Do not call this tool more than 3 times per question. If you cannot find what you need after 3 calls, use the best information you have.

        Args:
            libraryId: Exact Context7-compatible library ID (e.g., '/mongodb/docs', '/vercel/next.js', '/supabase/supabase', '/vercel/next.js/v14.3.0-canary.87') retrieved from 'resolve-library-id' or directly from user query in the format '/org/project' or '/org/project/version'.
            query: The question or task you need help with. Be specific and include relevant details. Good: 'How to set up authentication with JWT in Express.js' or 'React useEffect cleanup function examples'. Bad: 'auth' or 'hooks'. The query is sent to the Context7 API for processing. Do not include any sensitive or confidential information such as API keys, passwords, credentials, personal data, or proprietary code in your query.

        Returns:
            Tool execution result

        Tags:
            query, docs
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["libraryId"] = libraryId
            call_args["query"] = query
            result = await client.call_tool("query-docs", call_args)
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
        return [self.resolve_library_id, self.query_docs]
