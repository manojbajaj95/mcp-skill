---
name: notion
description: "MCP skill for notion. Provides 12 tools: notion-search, notion-fetch, notion-create-pages, notion-update-page, notion-move-pages, notion-duplicate-page, notion-create-database, notion-update-data-source, notion-create-comment, notion-get-comments, notion-get-teams, notion-get-users"
---

# notion

MCP skill for notion. Provides 12 tools: notion-search, notion-fetch, notion-create-pages, notion-update-page, notion-move-pages, notion-duplicate-page, notion-create-database, notion-update-data-source, notion-create-comment, notion-get-comments, notion-get-teams, notion-get-users

## Authentication

This MCP server uses **OAuth** authentication.
The OAuth flow is handled automatically by the MCP client. Tokens are persisted
to `~/.mcp-skill/notion/oauth-tokens/` so subsequent runs reuse the
same credentials without re-authenticating.

```python
app = NotionApp()  # uses default OAuth flow
```

To bring your own OAuth provider, pass it via the `auth` argument:

```python
app = NotionApp(auth=my_oauth_provider)
```

## Dependencies

This skill requires the following Python packages:

- `mcp-skill`

Install with uv:

```bash
uv pip install mcp-skill
```

Or with pip:

```bash
pip install mcp-skill
```

## How to Run

**Important:** Add `.agents/skills` to your Python path so imports resolve correctly:

```python
import sys
sys.path.insert(0, ".agents/skills")
from notion.app import NotionApp
```

Or set the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=".agents/skills:$PYTHONPATH"
```

**Preferred: use `uv run`** (handles dependencies automatically):

```bash
PYTHONPATH=.agents/skills uv run --with mcp-skill python -c "
import asyncio
from notion.app import NotionApp

async def main():
    app = NotionApp()
    result = await app.notion_search(query="example", query_type="example", content_search_mode="example")
    print(result)

asyncio.run(main())
"
```

**Alternative: use `python` directly** (install dependencies first):

```bash
pip install mcp-skill
PYTHONPATH=.agents/skills python -c "
import asyncio
from notion.app import NotionApp

async def main():
    app = NotionApp()
    result = await app.notion_search(query="example", query_type="example", content_search_mode="example")
    print(result)

asyncio.run(main())
"
```

## Available Tools

### notion-search

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

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | `str` | Yes | Semantic search query over your entire Notion workspace and connected sources (Slack, Google Drive, Github, Jira, Microsoft Teams, Sharepoint, OneDrive, or Linear). For best results, don't provide more than one question per tool call. Use a separate "search" tool call for each search you want to perform.
Alternatively, the query can be a substring or keyword to find users by matching against their name or email address. For example: "john" or "john@example.com" |
| query_type | `str` | No |  |
| content_search_mode | `str` | No |  |
| data_source_url | `str` | No | Optionally, provide the URL of a Data source to search. This will perform a semantic search over the pages in the Data Source. Note: must be a Data Source, not a Database. <data-source> tags are part of the Notion flavored Markdown format returned by tools like fetch. The full spec is available in the create-pages tool description. |
| page_url | `str` | No | Optionally, provide the URL or ID of a page to search within. This will perform a semantic search over the content within and under the specified page. Accepts either a full page URL (e.g. https://notion.so/workspace/Page-Title-1234567890) or just the page ID (UUIDv4) with or without dashes. |
| teamspace_id | `str` | No | Optionally, provide the ID of a teamspace to restrict search results to. This will perform a search over content within the specified teamspace only. Accepts the teamspace ID (UUIDv4) with or without dashes. |
| filters | `dict[str, Any]` | No | Optionally provide filters to apply to the search results. Only valid when query_type is 'internal'. |

**Example:**
```python
result = await app.notion_search(query="example", query_type="example", content_search_mode="example")
```

### notion-fetch

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

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | Yes | The ID or URL of the Notion page, database, or data source to fetch. Supports notion.so URLs, Notion Sites URLs (*.notion.site), raw UUIDs, and data source URLs (collection://...). |
| include_transcript | `bool` | No |  |
| include_discussions | `bool` | No |  |

**Example:**
```python
result = await app.notion_fetch(id="example", include_transcript=True, include_discussions=True)
```

### notion-create-pages

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

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| pages | `list[Any]` | Yes | The pages to create. |
| parent | `dict[str, Any]` | No | The parent under which the new pages will be created. This can be a page (page_id), a database page (database_id), or a data source/collection under a database (data_source_id). If omitted, the new pages will be created as private pages at the workspace level. Use data_source_id when you have a collection:// URL from the fetch tool. |

**Example:**
```python
result = await app.notion_create_pages(pages="value", parent="example")
```

### notion-update-page

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

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page_id | `str` | Yes | The ID of the page to update, with or without dashes. |
| command | `str` | Yes |  |
| properties | `dict[str, Any]` | No | Required for "update_properties" command. A JSON object that updates the page's properties. For pages in a database, use the SQLite schema definition shown in <database>. For pages outside of a database, the only allowed property is "title", which is the title of the page in inline markdown format. Use null to remove a property's value. |
| new_str | `str` | No | Required for "replace_content" command. The new content string to replace the entire page content with. |
| content_updates | `list[Any]` | No | Required for "update_content" command. An array of search-and-replace operations, each with old_str (content to find) and new_str (replacement content). |
| allow_deleting_content | `bool` | No |  |
| template_id | `str` | No | Required for "apply_template" command. The ID of a template to apply to this page. Template content is appended to any existing page content. |
| verification_status | `str` | No |  |
| verification_expiry_days | `int` | No | Optional for "update_verification" command when verification_status is "verified". Number of days until verification expires (e.g. 7, 30, 90). Omit for indefinite verification. |

**Example:**
```python
result = await app.notion_update_page(page_id="example", command="example", properties="value")
```

### notion-move-pages

Move one or more Notion pages or databases to a new parent.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page_or_database_ids | `list[str]` | Yes | An array of up to 100 page or database IDs to move. IDs are v4 UUIDs and can be supplied with or without dashes (e.g. extracted from a <page> or <database> URL given by the "search" or "fetch" tool). Data Sources under Databases can't be moved individually. |
| new_parent | `dict[str, Any]` | Yes | The new parent under which the pages will be moved. This can be a page, the workspace, a database, or a specific data source under a database when there are multiple. Moving pages to the workspace level adds them as private pages and should rarely be used. |

**Example:**
```python
result = await app.notion_move_pages(page_or_database_ids="value", new_parent="example")
```

### notion-duplicate-page

Duplicate a Notion page. The page must be within the current workspace, and you must have permission to access it. The duplication completes asynchronously, so do not rely on the new page identified by the returned ID or URL to be populated immediately. Let the user know that the duplication is in progress and that they can check back later using the 'fetch' tool or by clicking the returned URL and viewing it in the Notion app.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page_id | `str` | Yes | The ID of the page to duplicate. This is a v4 UUID, with or without dashes, and can be parsed from a Notion page URL. |

**Example:**
```python
result = await app.notion_duplicate_page(page_id="example")
```

### notion-create-database

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

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| schema | `str` | Yes | SQL DDL CREATE TABLE statement defining the database schema. Column names must be double-quoted, type options use single quotes. |
| parent | `dict[str, Any]` | No | The parent under which to create the new database. If omitted, the database will be created as a private page at the workspace level. |
| title | `str` | No | The title of the new database. |
| description | `str` | No | The description of the new database. |

**Example:**
```python
result = await app.notion_create_database(schema="example", parent="value", title="example")
```

### notion-update-data-source

Update a Notion data source's schema, title, or attributes using SQL DDL statements. Returns Markdown showing updated structure and schema.
Accepts a data source ID (collection ID from fetch response's <data-source> tag) or a single-source database ID. Multi-source databases require the specific data source ID.
The statements param accepts semicolon-separated DDL statements:
- ADD COLUMN "Name" <type> - add a new property
- DROP COLUMN "Name" - remove a property
- RENAME COLUMN "Old" TO "New" - rename a property
- ALTER COLUMN "Name" SET <type> - change type/options


*...additional tools omitted for brevity*
