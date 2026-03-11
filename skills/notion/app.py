"""Application for interacting with Notion via MCP."""
from typing import Any
from fastmcp import Client
from mcp_skill.auth import OAuth
import json

class NotionApp:
    """
    Application for interacting with Notion via MCP.
    Provides tools to interact with tools: notion-search, notion-fetch, notion-create-pages, notion-update-page, notion-move-pages and 9 more.
    """

    def __init__(self, url: str = "https://mcp.notion.com/mcp", auth=None) -> None:
        self.url = url
        self._oauth_auth = auth

    def _get_client(self) -> Client:
        oauth = self._oauth_auth or OAuth()
        return Client(self.url, auth=oauth)

    async def notion_search(self, query: str, content_search_mode: str = None, data_source_url: str = None, filters: dict[str, Any] = None, page_url: str = None, query_type: str = None, teamspace_id: str = None) -> dict[str, Any]:
        """
        Perform a search over:
- "internal": Semantic search over Notion workspace and connected sources (Slack, Google Drive, Github, Jira, Microsoft Teams, Sharepoint, OneDrive, Linear). Supports filtering by creation date and creator.
- "user": Search for users by name or email.

Auto-selects AI search (with connected sources) or workspace search (workspace-only, faster) based on user's access to Notion AI. Use content_search_mode to override.
Use "fetch" tool for full page/database contents after getting search results.
To search within a database: First fetch the database to get the data source URL (collection://...) from <data-source url="..."> tags, then use that as data_source_url. For multi-source databases, match by view ID (?v=...) in URL or search all sources separately.
Don't combine database URL/ID with collection:// prefix for data_source_url. Don't use database URL as page_url.
		<example description="Search with date range filter (only documents created in 2024)">
		{
			"query": "quarterly revenue report",
			"query_type": "internal",
			"filters": {
				"created_date_range": {
					"start_date": "2024-01-01",
					"end_date": "2025-01-01"
				}
			}
		}
		</example>
		<example description="Teamspace + creator filter">
		{"query": "project updates", "query_type": "internal", "teamspace_id": "f336d0bc-b841-465b-8045-024475c079dd", "filters": {"created_by_user_ids": ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"]}}
		</example>
		<example description="Database with date + creator filters">
		{"query": "design review", "data_source_url": "collection://f336d0bc-b841-465b-8045-024475c079dd", "filters": {"created_date_range": {"start_date": "2024-10-01"}, "created_by_user_ids": ["a1b2c3d4-e5f6-7890-abcd-ef1234567890", "b2c3d4e5-f6a7-8901-bcde-f12345678901"]}}
		</example>
		<example description="User search">
		{"query": "john@example.com", "query_type": "user"}
		</example>

        Args:
            query: Semantic search query over your entire Notion workspace and connected sources (Slack, Google Drive, Github, Jira, Microsoft Teams, Sharepoint, OneDrive, or Linear). For best results, don't provide more than one question per tool call. Use a separate "search" tool call for each search you want to perform.
Alternatively, the query can be a substring or keyword to find users by matching against their name or email address. For example: "john" or "john@example.com"
            content_search_mode: No description
            data_source_url: Optionally, provide the URL of a Data source to search. This will perform a semantic search over the pages in the Data Source. Note: must be a Data Source, not a Database. <data-source> tags are part of the Notion flavored Markdown format returned by tools like fetch. The full spec is available in the create-pages tool description.
            filters: Optionally provide filters to apply to the search results. Only valid when query_type is 'internal'.
            page_url: Optionally, provide the URL or ID of a page to search within. This will perform a semantic search over the content within and under the specified page. Accepts either a full page URL (e.g. https://notion.so/workspace/Page-Title-1234567890) or just the page ID (UUIDv4) with or without dashes.
            query_type: No description
            teamspace_id: Optionally, provide the ID of a teamspace to restrict search results to. This will perform a search over content within the specified teamspace only. Accepts the teamspace ID (UUIDv4) with or without dashes.

        Returns:
            Tool execution result

        Tags:
            notion, search
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["query"] = query
            if content_search_mode is not None:
                call_args["content_search_mode"] = content_search_mode
            if data_source_url is not None:
                call_args["data_source_url"] = data_source_url
            if filters is not None:
                call_args["filters"] = filters
            if page_url is not None:
                call_args["page_url"] = page_url
            if query_type is not None:
                call_args["query_type"] = query_type
            if teamspace_id is not None:
                call_args["teamspace_id"] = teamspace_id
            result = await client.call_tool("notion-search", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_fetch(self, id: str, include_discussions: bool = None, include_transcript: bool = None) -> dict[str, Any]:
        """
        Retrieves details about a Notion entity (page, database, or data source) by URL or ID.
Provide URL or ID in `id` parameter. Make multiple calls to fetch multiple entities.
Pages use enhanced Markdown format. For the complete specification, fetch the MCP resource at `notion://docs/enhanced-markdown-spec`.
Databases return all data sources (collections). Each data source has a unique ID shown in `<data-source url="collection://...">` tags. You can pass a data source ID directly to this tool to fetch details about that specific data source, including its schema and properties. Use data source IDs with update_data_source and query_data_sources tools. Multi-source databases (e.g., with linked sources) will show multiple data sources.
Set `include_discussions` to true to see discussion counts and inline discussion markers that correlate with the `get_comments` tool. The page output will include a `<page-discussions>` summary tag with discussion count, preview snippets, and `discussion://` URLs that match the discussion IDs returned by `get_comments`.
<example>{"id": "https://notion.so/workspace/Page-a1b2c3d4e5f67890"}</example>
<example>{"id": "12345678-90ab-cdef-1234-567890abcdef"}</example>
<example>{"id": "https://myspace.notion.site/Page-Title-abc123def456"}</example>
<example>{"id": "page-uuid", "include_discussions": true}</example>
<example>{"id": "collection://12345678-90ab-cdef-1234-567890abcdef"}</example>

        Args:
            id: The ID or URL of the Notion page, database, or data source to fetch. Supports notion.so URLs, Notion Sites URLs (*.notion.site), raw UUIDs, and data source URLs (collection://...).
            include_discussions: No description
            include_transcript: No description

        Returns:
            Tool execution result

        Tags:
            notion, fetch
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["id"] = id
            if include_discussions is not None:
                call_args["include_discussions"] = include_discussions
            if include_transcript is not None:
                call_args["include_transcript"] = include_transcript
            result = await client.call_tool("notion-fetch", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_create_pages(self, pages: list[Any], parent: dict[str, Any] = None) -> dict[str, Any]:
        """
        ## Overview
Creates one or more Notion pages, with the specified properties and content.
## Parent
All pages created with a single call to this tool will have the same parent. The parent can be a Notion page ("page_id") or data source ("data_source_id"). If the parent is omitted, the pages are created as standalone, workspace-level private pages, and the person that created them can organize them later as they see fit.
If you have a database URL, ALWAYS pass it to the "fetch" tool first to get the schema and URLs of each data source under the database. You can't use the "database_id" parent type if the database has more than one data source, so you'll need to identify which "data_source_id" to use based on the situation and the results from the fetch tool (data source URLs look like collection://<data_source_id>).
If you know the pages should be created under a data source, do NOT use the database ID or URL under the "page_id" parameter; "page_id" is only for regular, non-database pages.
## Content
Notion page content is a string in Notion-flavored Markdown format.
Don't include the page title at the top of the page's content. Only include it under "properties".
**IMPORTANT**: For the complete Markdown specification, always first fetch the MCP resource at `notion://docs/enhanced-markdown-spec`. Do NOT guess or hallucinate Markdown syntax. This spec is also applicable to other tools like update-page and fetch.
## Properties
Notion page properties are a JSON map of property names to SQLite values.
When creating pages in a database:
- Use the correct property names from the data source schema shown in the fetch tool results.
- Always include a title property. Data sources always have exactly one title property, but it may not be named "title", so, again, rely on the fetched data source schema.

For pages outside of a database:
- The only allowed property is "title",	which is the title of the page in inline markdown format. Always include a "title" property.

**IMPORTANT**: Some property types require expanded formats:
- Date properties: Split into "date:{property}:start", "date:{property}:end" (optional), and "date:{property}:is_datetime" (0 or 1)
- Place properties: Split into "place:{property}:name", "place:{property}:address", "place:{property}:latitude", "place:{property}:longitude", and "place:{property}:google_place_id" (optional)
- Number properties: Use JavaScript numbers (not strings)
- Checkbox properties: Use "__YES__" for checked, "__NO__" for unchecked

**Special property naming**: Properties named "id" or "url" (case insensitive) must be prefixed with "userDefined:" (e.g., "userDefined:URL", "userDefined:id")
## Templates
When creating a page in a database, you can apply a template to pre-populate it with content and property values. Use the "fetch" tool on a database to see available templates in the <templates> section of each data source.
When using a template:
- Pass the template's ID as "template_id" in the page object.
- Do NOT include "content" when using a template, as the template provides it.
- You can still set "properties" alongside the template to override template defaults.
- Template application is asynchronous. The page is created immediately but starts blank; the template content will appear shortly after.

## Examples
		<example description="Create a page from a database template">
		{
			"parent": {"data_source_id": "f336d0bc-b841-465b-8045-024475c079dd"},
			"pages": [
				{
					"template_id": "a5da15f6-b853-455d-8827-f906fb52db2b",
					"properties": {
						"Task Name": "New urgent bug"
					}
				}
			]
		}
		</example>
		<example description="Create a standalone page with a title and content">
		{
			"pages": [
				{
					"properties": {"title": "Page title"},
					"content": "# Section 1 {color="blue"}
Section 1 content
<details>
<summary>Toggle block</summary>
	Hidden content inside toggle
</details>"
				}
			]
		}
		</example>
		<example description="Create a page under a database's data source">
		{
			"parent": {"data_source_id": "f336d0bc-b841-465b-8045-024475c079dd"},
			"pages": [
				{
					"properties": {
						"Task Name": "Task 123",
						"Status": "In Progress",
						"Priority": 5,
						"Is Complete": "__YES__",
						"date:Due Date:start": "2024-12-25",
						"date:Due Date:is_datetime": 0
					}
				}
			]
		}
		</example>
		<example description="Create a page with an existing page as a parent">
		{
			"parent": {"page_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"},
			"pages": [
				{
					"properties": {"title": "Page title"},
					"content": "# Section 1
Section 1 content
# Section 2
Section 2 content"
				}
			]
		}
		</example>

        Args:
            pages: The pages to create.
            parent: The parent under which the new pages will be created. This can be a page (page_id), a database page (database_id), or a data source/collection under a database (data_source_id). If omitted, the new pages will be created as private pages at the workspace level. Use data_source_id when you have a collection:// URL from the fetch tool.

        Returns:
            Tool execution result

        Tags:
            notion, create, pages
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["pages"] = pages
            if parent is not None:
                call_args["parent"] = parent
            result = await client.call_tool("notion-create-pages", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_update_page(self, command: str, page_id: str, allow_deleting_content: bool = None, content_updates: list[Any] = None, new_str: str = None, properties: dict[str, Any] = None, template_id: str = None, verification_expiry_days: int = None, verification_status: str = None) -> dict[str, Any]:
        """
        ## Overview
Update a Notion page's properties or content.
## Properties
Notion page properties are a JSON map of property names to SQLite values.
For pages in a database:
- ALWAYS use the "fetch" tool first to get the data source schema and the	exact property names.
- Provide a non-null value to update a property's value.
- Omitted properties are left unchanged.

**IMPORTANT**: Some property types require expanded formats:
- Date properties: Split into "date:{property}:start", "date:{property}:end" (optional), and "date:{property}:is_datetime" (0 or 1)
- Place properties: Split into "place:{property}:name", "place:{property}:address", "place:{property}:latitude", "place:{property}:longitude", and "place:{property}:google_place_id" (optional)
- Number properties: Use JavaScript numbers (not strings)
- Checkbox properties: Use "__YES__" for checked, "__NO__" for unchecked

**Special property naming**: Properties named "id" or "url" (case insensitive) must be prefixed with "userDefined:" (e.g., "userDefined:URL", "userDefined:id")
For pages outside of a database:
- The only allowed property is "title",	which is the title of the page in inline markdown format.

## Content
Notion page content is a string in Notion-flavored Markdown format.
**IMPORTANT**: For the complete Markdown specification, first fetch the MCP resource at `notion://docs/enhanced-markdown-spec`. Do NOT guess or hallucinate Markdown syntax.
Before updating a page's content with this tool, use the "fetch" tool first to get the existing content to find out the Markdown snippets to use in the "update_content" command's old_str fields.
### Preserving Child Pages and Databases
When using "replace_content", the operation will check if any child pages or databases would be deleted. If so, it will fail with an error listing the affected items.
To preserve child pages/databases, include them in new_str using `<page url="...">` or `<database url="...">` tags. Get the exact URLs from the "fetch" tool output.
**CRITICAL**: To intentionally delete child content: if the call failed with validation and requires `allow_deleting_content` to be true, DO NOT automatically assume the content should be deleted. ALWAYS show the list of pages to be deleted and ask for user confirmation before proceeding.
## Examples
		<example description="Update page properties">
		{
			"page_id": "f336d0bc-b841-465b-8045-024475c079dd",
			"command": "update_properties",
			"properties": {
				"title": "New Page Title",
				"status": "In Progress",
				"priority": 5,
				"checkbox": "__YES__",
				"date:deadline:start": "2024-12-25",
				"date:deadline:is_datetime": 0,
				"place:office:name": "HQ",
				"place:office:latitude": 37.7749,
				"place:office:longitude": -122.4194
			}
		}
		</example>
		<example description="Replace the entire content of a page">
		{
			"page_id": "f336d0bc-b841-465b-8045-024475c079dd",
			"command": "replace_content",
			"new_str": "# New Section
Updated content goes here"
		}
		</example>
		<example description="Update specific content in a page (search-and-replace)">
		{
			"page_id": "f336d0bc-b841-465b-8045-024475c079dd",
			"command": "update_content",
			"content_updates": [
				{
					"old_str": "# Old Section
Old content here",
					"new_str": "# New Section
Updated content goes here"
				}
			]
		}
		</example>
		<example description="Insert content after a specific location">
		{
			"page_id": "f336d0bc-b841-465b-8045-024475c079dd",
			"command": "update_content",
			"content_updates": [
				{
					"old_str": "## Previous section
Existing content",
					"new_str": "## Previous section
Existing content

## New Section
Content to insert goes here"
				}
			]
		}
		</example>
		<example description="Multiple content updates in a single call">
		{
			"page_id": "f336d0bc-b841-465b-8045-024475c079dd",
			"command": "update_content",
			"content_updates": [
				{
					"old_str": "Old text 1",
					"new_str": "New text 1"
				},
				{
					"old_str": "Old text 2",
					"new_str": "New text 2"
				}
			]
		}
		</example>
## Templates
You can apply a template to an existing page using the "apply_template" command. The template content is appended to the page asynchronously. Get template IDs from the <templates> section in the fetch tool results for a database, or use any page ID as a template.
		<example description="Apply a template to an existing page">
		{
			"page_id": "f336d0bc-b841-465b-8045-024475c079dd",
			"command": "apply_template",
			"template_id": "a5da15f6-b853-455d-8827-f906fb52db2b"
		}
		</example>
## Verification
You can verify or unverify a page using the "update_verification" command. Verification marks a page as reviewed and up-to-date. Requires a Business or Enterprise plan (or the page must be in a wiki).
		<example description="Verify a page for 90 days">
		{
			"page_id": "f336d0bc-b841-465b-8045-024475c079dd",
			"command": "update_verification",
			"verification_status": "verified",
			"verification_expiry_days": 90
		}
		</example>
		<example description="Verify a page indefinitely">
		{
			"page_id": "f336d0bc-b841-465b-8045-024475c079dd",
			"command": "update_verification",
			"verification_status": "verified"
		}
		</example>
		<example description="Remove verification from a page">
		{
			"page_id": "f336d0bc-b841-465b-8045-024475c079dd",
			"command": "update_verification",
			"verification_status": "unverified"
		}
		</example>

        Args:
            command: No description
            page_id: The ID of the page to update, with or without dashes.
            allow_deleting_content: No description
            content_updates: Required for "update_content" command. An array of search-and-replace operations, each with old_str (content to find) and new_str (replacement content).
            new_str: Required for "replace_content" command. The new content string to replace the entire page content with.
            properties: Required for "update_properties" command. A JSON object that updates the page's properties. For pages in a database, use the SQLite schema definition shown in <database>. For pages outside of a database, the only allowed property is "title", which is the title of the page in inline markdown format. Use null to remove a property's value.
            template_id: Required for "apply_template" command. The ID of a template to apply to this page. Template content is appended to any existing page content.
            verification_expiry_days: Optional for "update_verification" command when verification_status is "verified". Number of days until verification expires (e.g. 7, 30, 90). Omit for indefinite verification.
            verification_status: No description

        Returns:
            Tool execution result

        Tags:
            notion, update, page
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["command"] = command
            call_args["page_id"] = page_id
            if allow_deleting_content is not None:
                call_args["allow_deleting_content"] = allow_deleting_content
            if content_updates is not None:
                call_args["content_updates"] = content_updates
            if new_str is not None:
                call_args["new_str"] = new_str
            if properties is not None:
                call_args["properties"] = properties
            if template_id is not None:
                call_args["template_id"] = template_id
            if verification_expiry_days is not None:
                call_args["verification_expiry_days"] = verification_expiry_days
            if verification_status is not None:
                call_args["verification_status"] = verification_status
            result = await client.call_tool("notion-update-page", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_move_pages(self, new_parent: dict[str, Any], page_or_database_ids: list[str]) -> dict[str, Any]:
        """
        Move one or more Notion pages or databases to a new parent.

        Args:
            new_parent: The new parent under which the pages will be moved. This can be a page, the workspace, a database, or a specific data source under a database when there are multiple. Moving pages to the workspace level adds them as private pages and should rarely be used.
            page_or_database_ids: An array of up to 100 page or database IDs to move. IDs are v4 UUIDs and can be supplied with or without dashes (e.g. extracted from a <page> or <database> URL given by the "search" or "fetch" tool). Data Sources under Databases can't be moved individually.

        Returns:
            Tool execution result

        Tags:
            notion, move, pages
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["new_parent"] = new_parent
            call_args["page_or_database_ids"] = page_or_database_ids
            result = await client.call_tool("notion-move-pages", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_duplicate_page(self, page_id: str) -> dict[str, Any]:
        """
        Duplicate a Notion page. The page must be within the current workspace, and you must have permission to access it. The duplication completes asynchronously, so do not rely on the new page identified by the returned ID or URL to be populated immediately. Let the user know that the duplication is in progress and that they can check back later using the 'fetch' tool or by clicking the returned URL and viewing it in the Notion app.

        Args:
            page_id: The ID of the page to duplicate. This is a v4 UUID, with or without dashes, and can be parsed from a Notion page URL.

        Returns:
            Tool execution result

        Tags:
            notion, duplicate, page
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["page_id"] = page_id
            result = await client.call_tool("notion-duplicate-page", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_create_database(self, schema: str, description: str = None, parent: dict[str, Any] = None, title: str = None) -> dict[str, Any]:
        """
        Creates a new Notion database using SQL DDL syntax.
If no title property provided, "Name" is auto-added. Returns Markdown with schema, SQLite definition, and data source ID in <data-source> tag for use with update_data_source and query_data_sources tools.
The schema param accepts a CREATE TABLE statement defining columns.
Type syntax:
- Simple: TITLE, RICH_TEXT, DATE, PEOPLE, CHECKBOX, URL, EMAIL, PHONE_NUMBER, STATUS, FILES
- SELECT('opt':color, ...) / MULTI_SELECT('opt':color, ...)
- NUMBER [FORMAT 'dollar'] / FORMULA('expression')
- RELATION('data_source_id') — one-way relation
- RELATION('data_source_id', DUAL) — two-way relation
- RELATION('data_source_id', DUAL 'synced_name') — two-way with synced property name
- RELATION('data_source_id', DUAL 'synced_name' 'synced_id') — two-way with synced name and ID (for self-relations)
- ROLLUP('rel_prop', 'target_prop', 'function')
- UNIQUE_ID [PREFIX 'X'] / CREATED_TIME / LAST_EDITED_TIME
- Any column: COMMENT 'description text' Colors: default, gray, brown, orange, yellow, green, blue, purple, pink, red

<example description="Minimal">{"schema": "CREATE TABLE ("Name" TITLE)"}</example>
<example description="Task DB">{"title": "Tasks", "schema": "CREATE TABLE ("Task Name" TITLE, "Status" SELECT('To Do':red, 'Done':green), "Due Date" DATE)"}</example>
<example description="With parent and options">{"parent": {"page_id": "f336d0bc-b841-465b-8045-024475c079dd"}, "title": "Projects", "schema": "CREATE TABLE ("Name" TITLE, "Budget" NUMBER FORMAT 'dollar', "Tags" MULTI_SELECT('eng':blue, 'design':pink), "Task ID" UNIQUE_ID PREFIX 'PRJ')"}</example>
<example description="Self-relation (two-step: create database first, then use its data source ID with update_data_source to add self-relations)">{"title": "Tasks", "schema": "CREATE TABLE ("Name" TITLE, "Parent" RELATION('ds_id', DUAL 'Children' 'children'), "Children" RELATION('ds_id', DUAL 'Parent' 'parent'))"}</example>

        Args:
            schema: SQL DDL CREATE TABLE statement defining the database schema. Column names must be double-quoted, type options use single quotes.
            description: The description of the new database.
            parent: The parent under which to create the new database. If omitted, the database will be created as a private page at the workspace level.
            title: The title of the new database.

        Returns:
            Tool execution result

        Tags:
            notion, create, database
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["schema"] = schema
            if description is not None:
                call_args["description"] = description
            if parent is not None:
                call_args["parent"] = parent
            if title is not None:
                call_args["title"] = title
            result = await client.call_tool("notion-create-database", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_update_data_source(self, data_source_id: str, description: str = None, in_trash: bool = None, is_inline: bool = None, statements: str = None, title: str = None) -> dict[str, Any]:
        """
        Update a Notion data source's schema, title, or attributes using SQL DDL statements. Returns Markdown showing updated structure and schema.
Accepts a data source ID (collection ID from fetch response's <data-source> tag) or a single-source database ID. Multi-source databases require the specific data source ID.
The statements param accepts semicolon-separated DDL statements:
- ADD COLUMN "Name" <type> - add a new property
- DROP COLUMN "Name" - remove a property
- RENAME COLUMN "Old" TO "New" - rename a property
- ALTER COLUMN "Name" SET <type> - change type/options

Same type syntax as create_database. Key types:
- SELECT('opt':color, ...) / MULTI_SELECT('opt':color, ...)
- NUMBER [FORMAT 'dollar'] / FORMULA('expression')
- RELATION('ds_id') / RELATION('ds_id', DUAL) / RELATION('ds_id', DUAL 'synced_name' 'synced_id')
- ROLLUP('rel_prop', 'target_prop', 'function') / UNIQUE_ID [PREFIX 'X']
- Simple: TITLE, RICH_TEXT, DATE, PEOPLE, CHECKBOX, URL, EMAIL, PHONE_NUMBER, STATUS, FILES

<example description="Add properties">{"data_source_id": "f336d0bc-b841-465b-8045-024475c079dd", "statements": "ADD COLUMN "Priority" SELECT('High':red, 'Medium':yellow, 'Low':green); ADD COLUMN "Due Date" DATE"}</example>
<example description="Rename property">{"data_source_id": "f336d0bc-b841-465b-8045-024475c079dd", "statements": "RENAME COLUMN "Status" TO "Project Status""}</example>
<example description="Remove property">{"data_source_id": "f336d0bc-b841-465b-8045-024475c079dd", "statements": "DROP COLUMN "Old Property""}</example>
<example description="Add self-relation">{"data_source_id": "f336d0bc-b841-465b-8045-024475c079dd", "statements": "ADD COLUMN "Parent" RELATION('f336d0bc-b841-465b-8045-024475c079dd', DUAL 'Children' 'children'); ADD COLUMN "Children" RELATION('f336d0bc-b841-465b-8045-024475c079dd', DUAL 'Parent' 'parent')"}</example>
<example description="Update title">{"data_source_id": "f336d0bc-b841-465b-8045-024475c079dd", "title": "Project Tracker 2024"}</example>
<example description="Trash data source">{"data_source_id": "f336d0bc-b841-465b-8045-024475c079dd", "in_trash": true}</example>
Notes: Cannot delete/create title properties. Max one unique_id property. Cannot update synced databases. Use "fetch" first to see current schema and get the data source ID from <data-source url="collection://..."> tags.

        Args:
            data_source_id: The data source to update. Accepts a collection:// URI from <data-source> tags, a bare UUID, or a database ID (only if the database has a single data source).
            description: The new description of the data source.
            in_trash: No description
            is_inline: No description
            statements: Semicolon-separated SQL DDL statements to update the schema. Supports ADD COLUMN, DROP COLUMN, RENAME COLUMN, ALTER COLUMN SET.
            title: The new title of the data source.

        Returns:
            Tool execution result

        Tags:
            notion, update, data, source
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["data_source_id"] = data_source_id
            if description is not None:
                call_args["description"] = description
            if in_trash is not None:
                call_args["in_trash"] = in_trash
            if is_inline is not None:
                call_args["is_inline"] = is_inline
            if statements is not None:
                call_args["statements"] = statements
            if title is not None:
                call_args["title"] = title
            result = await client.call_tool("notion-update-data-source", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_create_comment(self, page_id: str, rich_text: list[Any], discussion_id: str = None, selection_with_ellipsis: str = None) -> dict[str, Any]:
        """
        Add a comment to a page or specific content.
Creates a new comment. Provide `page_id` to identify the page, then choose ONE targeting mode:
- `page_id` alone: Page-level comment on the entire page
- `page_id` + `selection_with_ellipsis`: Comment on specific block content
- `discussion_id`: Reply to an existing discussion thread (page_id is still required)

For content targeting, use `selection_with_ellipsis` with ~10 chars from start and end: "# Section Ti...tle content"
<example description="Page-level comment">
{"page_id": "uuid", "rich_text": [{"text": {"content": "Comment"}}]}
</example>
<example description="Comment on specific content">
{"page_id": "uuid", "selection_with_ellipsis": "# Meeting No...es heading",
 "rich_text": [{"text": {"content": "Comment on this section"}}]}
</example>
<example description="Reply to discussion">
{"page_id": "uuid", "discussion_id": "discussion://pageId/blockId/discussionId",
 "rich_text": [{"text": {"content": "Reply"}}]}
</example>

        Args:
            page_id: The ID of the page to comment on (with or without dashes).
            rich_text: An array of rich text objects that represent the content of the comment.
            discussion_id: The ID or URL of an existing discussion to reply to (e.g., discussion://pageId/blockId/discussionId).
            selection_with_ellipsis: Unique start and end snippet of the content to comment on. DO NOT provide the entire string. Instead, provide up to the first ~10 characters, an ellipsis, and then up to the last ~10 characters. Make sure you provide enough of the start and end snippet to uniquely identify the content. For example: "# Section heading...last paragraph."

        Returns:
            Tool execution result

        Tags:
            notion, create, comment
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["page_id"] = page_id
            call_args["rich_text"] = rich_text
            if discussion_id is not None:
                call_args["discussion_id"] = discussion_id
            if selection_with_ellipsis is not None:
                call_args["selection_with_ellipsis"] = selection_with_ellipsis
            result = await client.call_tool("notion-create-comment", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_get_comments(self, page_id: str, discussion_id: str = None, include_all_blocks: bool = None, include_resolved: bool = None) -> dict[str, Any]:
        """
        Get comments and discussions from a Notion page.
Returns discussions with full comment content in XML format. By default, returns page-level discussions only.
Tip: Use the `fetch` tool with `include_discussions: true` first to see where discussions are anchored in the page content, then use this tool to retrieve full discussion threads. The `discussion://` URLs in the fetch output match the discussion IDs returned here.
Parameters:
- `include_all_blocks`: Include discussions on child blocks (default: false)
- `include_resolved`: Include resolved discussions (default: false)
- `discussion_id`: Fetch a specific discussion by ID or URL

<example>{"page_id": "page-uuid"}</example>
<example>{"page_id": "page-uuid", "include_all_blocks": true}</example>
<example>{"page_id": "page-uuid", "discussion_id": "discussion://pageId/blockId/discussionId"}</example>

        Args:
            page_id: Identifier for a Notion page.
            discussion_id: Fetch a specific discussion by ID or discussion URL (e.g., discussion://pageId/blockId/discussionId).
            include_all_blocks: No description
            include_resolved: No description

        Returns:
            Tool execution result

        Tags:
            notion, comments
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["page_id"] = page_id
            if discussion_id is not None:
                call_args["discussion_id"] = discussion_id
            if include_all_blocks is not None:
                call_args["include_all_blocks"] = include_all_blocks
            if include_resolved is not None:
                call_args["include_resolved"] = include_resolved
            result = await client.call_tool("notion-get-comments", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_get_teams(self, query: str = None) -> dict[str, Any]:
        """
        Retrieves a list of teams (teamspaces) in the current workspace. Shows which teams exist, user membership status, IDs, names, and roles.
Teams are returned split by membership status and limited to a maximum of 10 results.
<examples>
1. List all teams (up to the limit of each type): {}
2. Search for teams by name: {"query": "engineering"}
3. Find a specific team: {"query": "Product Design"}
</examples>

        Args:
            query: Optional search query to filter teams by name (case-insensitive).

        Returns:
            Tool execution result

        Tags:
            notion, teams
        """
        async with self._get_client() as client:
            call_args = {}
            if query is not None:
                call_args["query"] = query
            result = await client.call_tool("notion-get-teams", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_get_users(self, page_size: int = None, query: str = None, start_cursor: str = None, user_id: str = None) -> dict[str, Any]:
        """
        Retrieves a list of users in the current workspace. Shows workspace members and guests with their IDs, names, emails (if available), and types (person or bot).
Supports cursor-based pagination to iterate through all users in the workspace.
<examples>
1. List all users (first page): {}
2. Search for users by name or email: {"query": "john"}
3. Get next page of results: {"start_cursor": "abc123"}
4. Set custom page size: {"page_size": 20}
5. Fetch a specific user by ID: {"user_id": "00000000-0000-4000-8000-000000000000"}
6. Fetch the current user: {"user_id": "self"}
</examples>

        Args:
            page_size: Number of users to return per page (default: 100, max: 100).
            query: Optional search query to filter users by name or email (case-insensitive).
            start_cursor: Cursor for pagination. Use the next_cursor value from the previous response to get the next page.
            user_id: Return only the user matching this ID. Pass "self" to fetch the current user.

        Returns:
            Tool execution result

        Tags:
            notion, users
        """
        async with self._get_client() as client:
            call_args = {}
            if page_size is not None:
                call_args["page_size"] = page_size
            if query is not None:
                call_args["query"] = query
            if start_cursor is not None:
                call_args["start_cursor"] = start_cursor
            if user_id is not None:
                call_args["user_id"] = user_id
            result = await client.call_tool("notion-get-users", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_create_view(self, data_source_id: str, database_id: str, name: str, type: str, configure: str = None) -> dict[str, Any]:
        """
        Create a new view on a Notion database.
Use "fetch" first to get the database_id and data_source_id (from <data-source> tags in the response).
Supported types: table, board, list, calendar, timeline, gallery, dashboard.
The optional "configure" param accepts a DSL for filters, sorts, grouping,
and display options. See the notion://docs/view-dsl-spec resource for full
syntax. Key directives:
- FILTER "Property" = "value" — filter rows
- SORT BY "Property" ASC — sort rows
- GROUP BY "Property" — group by property (required for board views)
- CALENDAR BY "Property" — date property (required for calendar views)
- TIMELINE BY "Start" TO "End" — date range (required for timeline views)
- SHOW "Prop1", "Prop2" — set visible properties
- COVER "Property" — cover image property

<example description="Table view">{"database_id": "abc123", "data_source_id": "def456", "name": "All Tasks", "type": "table"}</example>
<example description="Board grouped by Status">{"database_id": "abc123", "data_source_id": "def456", "name": "Task Board", "type": "board", "configure": "GROUP BY "Status""}</example>
<example description="Filtered + sorted table">{"database_id": "abc123", "data_source_id": "def456", "name": "Active", "type": "table", "configure": "FILTER "Status" = "In Progress"; SORT BY "Due Date" ASC"}</example>
<example description="Calendar view">{"database_id": "abc123", "data_source_id": "def456", "name": "Calendar", "type": "calendar", "configure": "CALENDAR BY "Due Date""}</example>
<example description="Dashboard">{"database_id": "abc123", "data_source_id": "def456", "name": "Overview", "type": "dashboard"}</example>

        Args:
            data_source_id: The data source (collection) ID. Accepts a collection:// URI from <data-source> tags or a bare UUID.
            database_id: The database to create a view in. Accepts a Notion URL or a bare UUID.
            name: The name of the view.
            type: No description
            configure: View configuration DSL string. Supports FILTER, SORT BY, GROUP BY, CALENDAR BY, TIMELINE BY, SHOW, HIDE, COVER, WRAP CELLS, and FREEZE COLUMNS directives. See notion://docs/view-dsl-spec for full syntax.

        Returns:
            Tool execution result

        Tags:
            notion, create, view
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["data_source_id"] = data_source_id
            call_args["database_id"] = database_id
            call_args["name"] = name
            call_args["type"] = type
            if configure is not None:
                call_args["configure"] = configure
            result = await client.call_tool("notion-create-view", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def notion_update_view(self, view_id: str, configure: str = None, name: str = None) -> dict[str, Any]:
        """
        Update a view's name, filters, sorts, or display configuration.
Use "fetch" to get view IDs from database responses. Only include fields
you want to change. The "configure" param uses the same DSL as create_view.
Use CLEAR to remove settings:
- CLEAR FILTER — remove all filters
- CLEAR SORT — remove all sorts
- CLEAR GROUP BY — remove grouping

See notion://docs/view-dsl-spec resource for full syntax.
<example description="Rename">{"view_id": "abc123", "name": "Sprint Board"}</example>
<example description="Update filter">{"view_id": "abc123", "configure": "FILTER "Status" = "Done""}</example>
<example description="Clear filter, add sort">{"view_id": "abc123", "configure": "CLEAR FILTER; SORT BY "Created" DESC"}</example>
<example description="Update grouping">{"view_id": "abc123", "configure": "GROUP BY "Priority"; SHOW "Name", "Status""}</example>

        Args:
            view_id: The view to update. Accepts a view:// URI, a Notion URL with ?v= parameter, or a bare UUID.
            configure: View configuration DSL string. Supports FILTER, SORT BY, GROUP BY, CALENDAR BY, TIMELINE BY, SHOW, HIDE, COVER, WRAP CELLS, FREEZE COLUMNS, and CLEAR directives. See notion://docs/view-dsl-spec for full syntax.
            name: New name for the view.

        Returns:
            Tool execution result

        Tags:
            notion, update, view
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["view_id"] = view_id
            if configure is not None:
                call_args["configure"] = configure
            if name is not None:
                call_args["name"] = name
            result = await client.call_tool("notion-update-view", call_args)
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
        return [self.notion_search, self.notion_fetch, self.notion_create_pages, self.notion_update_page, self.notion_move_pages, self.notion_duplicate_page, self.notion_create_database, self.notion_update_data_source, self.notion_create_comment, self.notion_get_comments, self.notion_get_teams, self.notion_get_users, self.notion_create_view, self.notion_update_view]
