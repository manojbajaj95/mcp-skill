"""Application for interacting with Buffer via MCP."""
from typing import Any
from fastmcp import Client
from mcp_skill.auth import BearerAuth
import json

class BufferApp:
    """
    Application for interacting with Buffer via MCP.
    Provides tools to interact with tools: get_account, list_channels, get_channel, list_posts, get_post and 6 more.
    """

    def __init__(self, url: str = "https://mcp.buffer.com/mcp", auth=None) -> None:
        self.url = url
        self._auth = BearerAuth(api_key=auth, server_url=url)

    def _get_client(self) -> Client:
        return Client(self.url, auth=self._auth)

    async def get_account(self) -> dict[str, Any]:
        """
        Retrieves the authenticated user account and organization details. Call this FIRST in any workflow to obtain your organization ID, which is required by most other tools. Returns account info (email, name, timezone) and organizations (id, name, plan limits, member count). If the user has multiple organizations, list them by name and confirm which one to use before proceeding with other operations.

        Returns:
            Tool execution result

        Tags:
            account
        """
        async with self._get_client() as client:
            call_args = {}
            result = await client.call_tool("get_account", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_channels(self, organizationId: str) -> dict[str, Any]:
        """
        Lists all social media channels connected to a Buffer organization. Returns summary info (id, name, displayName, service, type, avatar, connection status). Use get_channel for detailed information about a specific channel, including posting schedule. Call get_account first to obtain your organization ID.

        Args:
            organizationId: The ID of the organization to list channels for. Use get_account to retrieve your organization IDs. Tell the user which organization (by name) you are querying.

        Returns:
            Tool execution result

        Tags:
            list, channels
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["organizationId"] = organizationId
            result = await client.call_tool("list_channels", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_channel(self, channelId: str) -> dict[str, Any]:
        """
        Retrieves detailed information for a specific social media channel. Returns posting schedule, posting goals, queue status, timezone, link shortening config, and service-specific metadata (e.g., Pinterest boards, Mastodon server URL, Instagram reminder settings). Use list_channels first to discover available channel IDs.

        Args:
            channelId: The ID of the channel to retrieve. Use list_channels to see available channels.

        Returns:
            Tool execution result

        Tags:
            channel
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["channelId"] = channelId
            result = await client.call_tool("get_channel", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_posts(self, organizationId: str, after: str | None = None, channelIds: list[str] | None = None, createdAt: dict[str, Any] | None = None, dueAt: dict[str, Any] | None = None, first: int | None = None, sort: list[Any] | None = None, status: list[str] | None = None, tagIds: list[str] | None = None) -> dict[str, Any]:
        """
        Lists posts from a Buffer organization with filters for channels, status, tags, and dates. Returns post details including id, status, via, text, scheduled/sent times, channel info, tags, and errors. Supports pagination using Relay-style cursors. Call get_account first to obtain your organization ID, and list_channels to discover channel IDs.

        Args:
            organizationId: The ID of the organization to list posts for. Use get_account to retrieve your organization IDs. Tell the user which organization (by name) you are querying.
            after: Cursor for pagination
            channelIds: Filter posts by specific channel IDs. Use list_channels to discover available channel IDs.
            createdAt: Filter posts by the date they were created
            dueAt: Filter posts by their scheduled posting date
            first: Number of posts to return per page (default: 20, max: 100)
            sort: Sort order for results (e.g., [{field: "dueAt", direction: "asc"}])
            status: Filter posts by status (draft, needs_approval, scheduled, sending, sent, error)
            tagIds: Filter posts by tag IDs

        Returns:
            Tool execution result

        Tags:
            list, posts
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["organizationId"] = organizationId
            if after is not None:
                call_args["after"] = after
            if channelIds is not None:
                call_args["channelIds"] = channelIds
            if createdAt is not None:
                call_args["createdAt"] = createdAt
            if dueAt is not None:
                call_args["dueAt"] = dueAt
            if first is not None:
                call_args["first"] = first
            if sort is not None:
                call_args["sort"] = sort
            if status is not None:
                call_args["status"] = status
            if tagIds is not None:
                call_args["tagIds"] = tagIds
            result = await client.call_tool("list_posts", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_post(self, postId: str) -> dict[str, Any]:
        """
        Retrieves detailed information about a specific post by ID. Returns comprehensive post data including status, content, author, channel references, tags, notes, assets (images, videos, documents), and allowed actions. The metadata field contains service-specific data (e.g., Instagram geolocation, Twitter threads, YouTube privacy settings, Pinterest boards). Posts with status "error" include an error field with the failure message. Use list_posts to discover post IDs.

        Args:
            postId: The ID of the post to retrieve. Use list_posts to discover post IDs.

        Returns:
            Tool execution result

        Tags:
            post
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["postId"] = postId
            result = await client.call_tool("get_post", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def create_idea(self, content: dict[str, Any], organizationId: str) -> dict[str, Any]:
        """
        Create a new content idea in a Buffer organization. Ideas are drafts for future social media posts — use them to capture concepts, attach media, and tag with categories. Call get_account first to obtain your organization ID. Returns the created idea record. Do not use this tool to publish or schedule posts.

        Args:
            content: Content and metadata for the new idea.
            organizationId: The ID of the organization to create the idea in. Use get_account to retrieve your organization IDs. Confirm with the user which organization (by name) you are creating the idea in.

        Returns:
            Tool execution result

        Tags:
            create, idea
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["content"] = content
            call_args["organizationId"] = organizationId
            result = await client.call_tool("create_idea", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def create_post(self, channelId: str, schedulingType: str, assets: dict[str, Any] | None = None, draftId: str | None = None, dueAt: str | None = None, ideaId: str | None = None, metadata: dict[str, Any] | None = None, mode: str | None = None, saveToDraft: bool | None = None, tagIds: list[str] | None = None, text: str | None = None) -> dict[str, Any]:
        """
        Create and schedule a social media post to a Buffer channel. Supports all platforms: Instagram, Facebook, Twitter, LinkedIn, Pinterest, YouTube, Google Business, Mastodon, TikTok, Threads, Bluesky, and Start Page. Before calling create_post, call get_account to choose an organization, then call list_channels for that organization and use an exact returned channel ID. 

Minimum requirements by service:
- Twitter/Mastodon/Threads/Bluesky: text only
- Instagram/TikTok: requires image or video asset
- Pinterest: requires image + metadata.pinterest.boardServiceId (get from get_channel)
- YouTube: requires video + metadata.youtube.title + metadata.youtube.categoryId


Threaded posts (platforms with metadata.{platform}.thread support):
You must provide BOTH the outer text field AND the thread array. The outer text should match your first thread item's text (required for backend validation). Include ALL thread items in the array.

Returns the created post with id, status, and scheduling details.

        Args:
            channelId: Target channel ID. You must use an exact ID returned by list_channels for the selected organization. Do not guess or infer channel IDs. Confirm with the user which organization and channel you are posting to before calling create_post.
            schedulingType: Publishing method: notification (manual approval) or automatic (auto-publish).
            assets: Media attachments.
            draftId: Source draft ID if converting from draft.
            dueAt: Scheduled time in ISO 8601 format with timezone offset (e.g., "2025-03-15T17:00:00-05:00"). Required for customScheduled mode. Use the timezone from get_account to construct the correct offset for the user's local time.
            ideaId: Source idea ID if converting from idea.
            metadata: Service-specific options.
            mode: How to schedule: addToQueue (add to queue), shareNow (publish immediately), shareNext (publish at next scheduled slot), customScheduled (custom time via dueAt), recommendedTime (optimal time based on Buffer analytics). Use addToQueue unless the user explicitly specifies a different scheduling mode.
            saveToDraft: Save as draft instead of scheduling.
            tagIds: Tag IDs for categorization.
            text: Post text content.

        Returns:
            Tool execution result

        Tags:
            create, post
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["channelId"] = channelId
            call_args["schedulingType"] = schedulingType
            if assets is not None:
                call_args["assets"] = assets
            if draftId is not None:
                call_args["draftId"] = draftId
            if dueAt is not None:
                call_args["dueAt"] = dueAt
            if ideaId is not None:
                call_args["ideaId"] = ideaId
            if metadata is not None:
                call_args["metadata"] = metadata
            if mode is not None:
                call_args["mode"] = mode
            if saveToDraft is not None:
                call_args["saveToDraft"] = saveToDraft
            if tagIds is not None:
                call_args["tagIds"] = tagIds
            if text is not None:
                call_args["text"] = text
            result = await client.call_tool("create_post", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def delete_post(self, postId: str) -> dict[str, Any]:
        """
        Permanently delete a post from Buffer. This action is irreversible. Use list_posts or get_post to find the post ID before deleting.

        Args:
            postId: The ID of the post to delete. Use list_posts or get_post to find post IDs.

        Returns:
            Tool execution result

        Tags:
            delete, post
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["postId"] = postId
            result = await client.call_tool("delete_post", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def introspect_schema(self) -> dict[str, Any]:
        """
        Returns the complete GraphQL schema for Buffer API including all queries, mutations, types, and arguments. Call this ONLY when you need to use execute_query or execute_mutation for operations not covered by domain-specific tools (get_account, list_channels, get_channel). Do not call this for common operations — use the domain tools instead.

        Returns:
            Tool execution result

        Tags:
            introspect, schema
        """
        async with self._get_client() as client:
            call_args = {}
            result = await client.call_tool("introspect_schema", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def execute_query(self, query: str, summary: str, operationName: str | None = None, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Executes a read-only GraphQL query to fetch data from Buffer. PREREQUISITE: Call introspect_schema first to learn available queries and fields. Use this only for operations not covered by domain tools (get_account, list_channels, get_channel). Do not guess query or field names — use only names from the schema.

        Args:
            query: The GraphQL query to execute. Field and type names MUST match the schema returned by introspect_schema.
            summary: A brief, non-technical description of what this operation does and why. This is shown to users in permission prompts to help them understand the action.
            operationName: Name of the specific query to run if multiple are defined.
            variables: Variables for the query as a JSON object.

        Returns:
            Tool execution result

        Tags:
            execute, query
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["query"] = query
            call_args["summary"] = summary
            if operationName is not None:
                call_args["operationName"] = operationName
            if variables is not None:
                call_args["variables"] = variables
            result = await client.call_tool("execute_query", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def execute_mutation(self, mutation: str, summary: str, operationName: str | None = None, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Executes a GraphQL mutation to modify data in Buffer. PREREQUISITE: Call introspect_schema first to learn available mutations and fields. Use this only for operations not covered by domain tools. Do not guess mutation or field names — use only names from the schema.

        Args:
            mutation: The GraphQL mutation to execute. Field and type names MUST match the schema returned by introspect_schema.
            summary: A brief, non-technical description of what this operation does and why. This is shown to users in permission prompts to help them understand the action.
            operationName: Name of the specific mutation to run if multiple are defined.
            variables: Variables for the mutation as a JSON object.

        Returns:
            Tool execution result

        Tags:
            execute, mutation
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["mutation"] = mutation
            call_args["summary"] = summary
            if operationName is not None:
                call_args["operationName"] = operationName
            if variables is not None:
                call_args["variables"] = variables
            result = await client.call_tool("execute_mutation", call_args)
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
        return [self.get_account, self.list_channels, self.get_channel, self.list_posts, self.get_post, self.create_idea, self.create_post, self.delete_post, self.introspect_schema, self.execute_query, self.execute_mutation]
