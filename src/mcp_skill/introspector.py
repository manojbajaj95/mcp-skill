"""MCP server connection and tool discovery."""
import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport


async def connect_and_list_tools(
    url: str,
    auth: str | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[str, list]:
    """Connect to an MCP server and list its tools.
    
    Args:
        url: MCP server URL (HTTP/HTTPS)
        auth: Authentication - None for no auth, string for Bearer token
        headers: Custom headers dict (e.g. {"x-api-key": "..."}). When
                 provided, a StreamableHttpTransport is constructed directly
                 so that headers are sent on every request.
    
    Returns:
        Tuple of (server_name, list_of_tools)
    
    Raises:
        ConnectionError: If cannot connect to server
        RuntimeError: If auth fails or other error
    """
    try:
        if headers:
            transport = StreamableHttpTransport(url=url, headers=headers)
            client = Client(transport)
        elif auth and auth.lower() not in ("none", ""):
            client = Client(url, auth=auth)
        else:
            client = Client(url)
        
        async with client:
            # Get tools list
            tools = await client.list_tools()
            
            # Try to derive server name from URL
            from urllib.parse import urlparse
            parsed = urlparse(url)
            hostname = parsed.hostname or "unknown"
            # Extract meaningful name from hostname
            parts = hostname.split(".")
            skip = {"www", "api", "mcp", "com", "org", "net", "io", "co", "dev", "app", "127", "0", "1", "localhost"}
            candidates = [p for p in parts if p and p.lower() not in skip]
            server_name = candidates[0] if candidates else (parts[0] if parts and parts[0] else "mcp-server")
            
            return (server_name, tools)
    
    except Exception as e:
        error_msg = str(e).lower()
        if "refused" in error_msg or "connect" in error_msg or "timeout" in error_msg:
            raise ConnectionError(f"Cannot connect to {url}. Is the server running? Error: {e}") from e
        if "401" in error_msg or "403" in error_msg or "auth" in error_msg:
            raise RuntimeError(f"Authentication failed for {url}. Check your API key or OAuth configuration. Error: {e}") from e
        raise RuntimeError(f"Error connecting to {url}: {e}") from e
