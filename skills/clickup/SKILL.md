---
name: clickup
description: "MCP skill for clickup. Provides 32 tools: clickup_search, clickup_get_workspace_hierarchy, clickup_create_task, clickup_get_task, clickup_update_task, clickup_get_task_comments, clickup_create_task_comment, clickup_attach_task_file, clickup_get_task_time_entries, clickup_start_time_tracking, clickup_stop_time_tracking, clickup_add_time_entry, clickup_get_current_time_entry, clickup_create_list, clickup_create_list_in_folder, clickup_get_list, clickup_update_list, clickup_create_folder, clickup_get_folder, clickup_update_folder, clickup_add_tag_to_task, clickup_remove_tag_from_task, clickup_get_workspace_members, clickup_find_member_by_name, clickup_resolve_assignees, clickup_get_chat_channels, clickup_send_chat_message, clickup_create_document, clickup_list_document_pages, clickup_get_document_pages, clickup_create_document_page, clickup_update_document_page"
---

# clickup

MCP skill for clickup. Provides 32 tools: clickup_search, clickup_get_workspace_hierarchy, clickup_create_task, clickup_get_task, clickup_update_task, clickup_get_task_comments, clickup_create_task_comment, clickup_attach_task_file, clickup_get_task_time_entries, clickup_start_time_tracking, clickup_stop_time_tracking, clickup_add_time_entry, clickup_get_current_time_entry, clickup_create_list, clickup_create_list_in_folder, clickup_get_list, clickup_update_list, clickup_create_folder, clickup_get_folder, clickup_update_folder, clickup_add_tag_to_task, clickup_remove_tag_from_task, clickup_get_workspace_members, clickup_find_member_by_name, clickup_resolve_assignees, clickup_get_chat_channels, clickup_send_chat_message, clickup_create_document, clickup_list_document_pages, clickup_get_document_pages, clickup_create_document_page, clickup_update_document_page

## Authentication

This MCP server uses **OAuth** authentication.
The OAuth flow is handled automatically by the MCP client. Tokens are persisted
to `~/.mcp-skill/clickup/oauth-tokens/` so subsequent runs reuse the
same credentials without re-authenticating.

```python
app = ClickupApp()  # uses default OAuth flow
```

To bring your own OAuth provider, pass it via the `auth` argument:

```python
app = ClickupApp(auth=my_oauth_provider)
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
from clickup.app import ClickupApp
```

Or set the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=".agents/skills:$PYTHONPATH"
```

**Preferred: use `uv run`** (handles dependencies automatically):

```bash
PYTHONPATH=.agents/skills uv run --with mcp-skill python -c "
import asyncio
from clickup.app import ClickupApp

async def main():
    app = ClickupApp()
    result = await app.clickup_search(keywords="example", sort="value", filters="value")
    print(result)

asyncio.run(main())
"
```

**Alternative: use `python` directly** (install dependencies first):

```bash
pip install mcp-skill
PYTHONPATH=.agents/skills python -c "
import asyncio
from clickup.app import ClickupApp

async def main():
    app = ClickupApp()
    result = await app.clickup_search(keywords="example", sort="value", filters="value")
    print(result)

asyncio.run(main())
"
```

## Available Tools

### clickup_search

Universal search across your entire ClickUp workspace. This is a powerful global search tool that finds ANY type of content - tasks, documents, dashboards, attachments, whiteboards, chat messages, and forms.

Use this tool when:
- You need to find something but don't know exactly where it is or what type it is
- You want to search across multiple asset types at once
- You're looking for items by keyword, content, or partial name matches
- You need to find all items assigned to specific users or created by certain people
- You want to search within specific spaces, folders, or lists
- You need to filter by creation date or due date ranges
- You need results sorted by creation or update time

This tool searches EVERYTHING - it looks inside task names, descriptions, document content, chat messages, file names, and more. Results include highlighted matches and full hierarchy (Space > Folder > List) for context.

Supports advanced filtering by assignees, creators, status, location, asset types, and date ranges (creation date and due date). Date filters accept dates in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format, and use your user timezone. Returns paginated results with a cursor for fetching additional pages.

The results are intelligently formatted for optimal readability, providing a concise overview and structured data for each result.

Note: For specific operations on known items (like updating a task you already identified), use the dedicated tools instead.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| keywords | `str` | No | Search query string. Use specific keywords to find items |
| sort | `list[Any]` | No | Sort criteria for results. Can specify multiple sort fields in priority order |
| filters | `dict[str, Any]` | No | Filters to refine search results by various criteria |
| count | `float` | No | Maximum number of results to return per page (for pagination) |
| cursor | `str` | No | Pagination cursor from previous response. Use to fetch next page of results |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_search(keywords="example", sort="value", filters="value")
```

### clickup_get_workspace_hierarchy

Get workspace hierarchy (spaces, folders, lists) from your authenticated workspace with pagination support. Workspace ID is automatically detected from your session. Returns tree structure with names and IDs for navigation. Supports pagination for large workspaces and depth control to fetch only needed levels. Note: Use this ONLY when you need to see the workspace structure - most tools can resolve names automatically without this lookup.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| cursor | `str` | No | Pagination cursor from previous response. Use to fetch next page of spaces |
| limit | `float` | No | Maximum number of spaces to return per page (default: 10, max: 50) |
| max_depth | `str` | No | Maximum depth of hierarchy to return: 0=spaces only, 1=spaces+folders, 2=spaces+folders+lists (default: 2) |
| space_ids | `list[str]` | No | Filter to return only specific spaces by ID. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_get_workspace_hierarchy(cursor="example", limit=1.0, max_depth=1.0)
```

### clickup_create_task

Create task in a ClickUp list. Requires task name and list_id. ALWAYS ask user which list to use - never guess. Use clickup_get_list to resolve list names to IDs. Supports assignees as array of user IDs, emails, usernames, or "me". Supports task_type to specify the task type by name (e.g., 'Bug', 'Feature').

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | `str` | Yes | Task name. Ask the user what they want to name the task. |
| list_id | `str` | Yes | ID of the list where the task should be created. Use clickup_get_list to find the list ID from a list name if needed. |
| description | `str` | No | Plain text description for the task. |
| markdown_description | `str` | No | Markdown formatted description for the task. If provided, this takes precedence over description. |
| status | `str` | No | Override the default ClickUp status. In most cases, omit this to use ClickUp defaults. |
| priority | `str` | No | Task priority: 'urgent', 'high', 'normal', or 'low'. If not provided, task will have no priority assigned. |
| due_date | `str` | No | Due date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format (e.g., '2025-12-31' or '2025-12-31 14:30') |
| start_date | `str` | No | Start date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format (e.g., '2025-01-01' or '2025-01-01 09:00') |
| parent | `str` | No | ID of the parent task. When specified, this task will be created as a subtask of the specified parent task. |
| tags | `list[str]` | No | Array of tag names to assign to the task. The tags must already exist in the space. |
| custom_fields | `list[Any]` | No | Array of custom field values to set on the task. Each object must have an 'id' and 'value' property. |
| check_required_custom_fields | `bool` | No | Flag to check if all required custom fields are set before saving the task. |
| assignees | `list[str]` | No | Array of assignee user IDs (as strings). Use clickup_resolve_assignees to convert emails, usernames, or "me" to user IDs if needed. |
| task_type | `str` | No | Name of the task type (e.g., 'Bug', 'Feature', 'Milestone'). The type must exist in the workspace. If not specified, the default task type will be used. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_create_task(name="example", list_id="example", description="example")
```

### clickup_get_task

Get task details by task_id (works with regular/custom IDs). Set subtasks=true to include all subtask details.

Response Size Optimization:
- Use detail_level='summary' for lightweight responses when full details aren't needed
- Responses exceeding 50,000 tokens automatically switch to summary format to prevent client issues
- Summary format includes essential fields: id, name, status, description (truncated), assignees, tags, due_date, url

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | `str` | Yes | ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed. |
| subtasks | `bool` | No | Whether to include subtasks in the response. Set to true to retrieve full details of all subtasks. |
| detail_level | `str` | No | Level of detail to return. Use 'summary' for lightweight responses or 'detailed' for full task data. Defaults to 'detailed' but automatically switches to 'summary' if response would be too large. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_get_task(task_id="example", subtasks=True, detail_level="example")
```

### clickup_update_task

Update task properties. Requires task_id and at least one update field. Custom fields supported as array of {id, value}. Supports assignees as array of user IDs, emails, usernames, or "me". Supports task_type to change the task type by name (e.g., 'Bug', 'Feature'), or null to reset to default.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | `str` | Yes | ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed. |
| name | `str` | No | New name for the task. |
| description | `str` | No | New plain text description. Will be ignored if markdown_description is provided. |
| markdown_description | `str` | No | New markdown description. Takes precedence over plain text description. |
| status | `str` | No | New status. Must be valid for the task's current list. |
| priority | `str | None` | No | Task priority: 'urgent', 'high', 'normal', 'low', or null to clear. If not provided, priority will not be changed. |
| due_date | `str | None` | No | Due date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format (e.g., '2025-12-31' or '2025-12-31 14:30'), or null to clear. If not provided, due date will not be changed. |
| start_date | `str | None` | No | Start date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format (e.g., '2025-01-01' or '2025-01-01 09:00'), or null to clear. If not provided, start date will not be changed. |
| time_estimate | `str` | No | Time estimate for the task. For best compatibility with the ClickUp API, use a numeric value in minutes (e.g., '150' for 2h 30m) |
| custom_fields | `list[Any]` | No | Array of custom field values to set on the task. Each object must have an 'id' and 'value' property. |
| assignees | `list[str]` | No | Array of assignee user IDs (as strings). Use clickup_resolve_assignees to convert emails, usernames, or "me" to user IDs if needed. |
| task_type | `str | None` | No | Name of the task type to change to (e.g., 'Bug', 'Feature', 'Milestone'). The type must exist in the workspace. Pass null to revert to the default 'Task' type. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_update_task(task_id="example", name="example", description="example")
```

### clickup_get_task_comments

Get task comments. Use start/start_id params for pagination.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | `str` | Yes | ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed. |
| start | `float` | No | Timestamp (in milliseconds) to start retrieving comments from. Used for pagination. |
| start_id | `str` | No | Comment ID to start from. Used together with start for pagination. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_get_task_comments(task_id="example", start=1.0, start_id="example")
```

### clickup_create_task_comment

Create task comment. Requires task_id and comment_text. Supports notify_all to alert assignees and assignee to assign the comment.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | `str` | Yes | ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed. |
| comment_text | `str` | Yes | Text content of the comment to create. |
| notify_all | `bool` | No | Whether to notify all assignees. Default is false. |
| assignee | `float` | No | User ID to assign the comment to. Use clickup_resolve_assignees to convert email, username, or "me" to user ID if needed. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_create_task_comment(task_id="example", comment_text="example", notify_all=True)
```

### clickup_attach_task_file

Attach file to task. Requires task_id. File sources: 1) base64 + filename, 2) URL (http/https).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | `str` | Yes | ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed. |
| file_name | `str` | No | Name of the file to be attached (include the extension). Required when using file_data. |
| file_data | `str` | No | Base64-encoded content of the file (without the data URL prefix). |
| file_url | `str` | No | URL to download the file from (must start with http:// or https://). |
| auth_header | `str` | No | Authorization header to use when downloading from the web URL. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_attach_task_file(task_id="example", file_name="example", file_data="example")
```

### clickup_get_task_time_entries

Get all time entries for a task with filtering options. Returns all tracked time with user info, descriptions, tags, start/end times, and durations.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | `str` | Yes | ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed. |
| start_date | `str` | No | Start date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format |
| end_date | `str` | No | End date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format |
| is_billable | `bool` | No | Filter by billable status. Set to true to get only billable time entries, false for non-billable entries. Omit to get all entries regardless of billable status. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_get_task_time_entries(task_id="example", start_date="example", end_date="example")
```

### clickup_start_time_tracking

Start time tracking on a task. Supports description, billable status, and tags. Only one timer can be running at a time. For best results, omit extra parameters unless specifically needed.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | `str` | Yes | ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed. |
| description | `str` | No | Description for the time entry. Keep short and simple, or omit for best compatibility. |
| billable | `bool` | No | Whether this time is billable. Default is workspace setting. |
| tags | `list[str]` | No | Array of tag names to assign to the time entry. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_start_time_tracking(task_id="example", description="example", billable=True)
```

### clickup_stop_time_tracking

Stop the currently running time tracker. Supports description and tags. Returns the completed time entry details.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| description | `str` | No | Description to update or add to the time entry. |
| tags | `list[str]` | No | Array of tag names to assign to the time entry. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_stop_time_tracking(description="example", tags="value", workspace_id="example")
```

### clickup_add_time_entry

Add a manual time entry to a task. You can provide either (start + duration) OR (start + end). The tool will calculate missing values. Requires task_id, start time, and either duration or end time. Supports description, billable flag, and tags.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | `str` | Yes | ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed. |
| start | `str` | Yes | Start time in YYYY-MM-DD HH:MM format (e.g., '2025-01-15 09:30'). Time is required for time tracking entries. |
| duration | `str` | No | Duration of the time entry. Format as 'Xh Ym' (e.g., '1h 30m') or just minutes (e.g., '90m'). Either duration or end_time is required. |
| end_time | `str` | No | End time in YYYY-MM-DD HH:MM format (e.g., '2025-01-15 11:00'). Time is required for time tracking entries. |
| description | `str` | No | Description for the time entry. Keep short and simple, or omit for best compatibility. |
| billable | `bool` | No | Whether this time is billable. Default is workspace setting. |
| tags | `list[str]` | No | Array of tag names to assign to the time entry. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_add_time_entry(task_id="example", start="example", duration="example")
```

### clickup_get_current_time_entry

Get the currently running time entry, if any. No parameters needed.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_get_current_time_entry(workspace_id="example")
```

### clickup_create_list

Create a list in a ClickUp space efficiently. The system automatically detects workspace ID and resolves space names. Use space_name (preferred for simplicity) or space_id + list name. Name is required. For lists in folders, use clickup_create_list_in_folder. Supports content, due_date, priority, assignee, and status. Note: No need to look up workspace hierarchy or space IDs first - the system handles space name resolution automatically.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | `str` | Yes | Name of the list. |
| space_id | `str` | No | ID of the space to create the list in. Provide this instead of space_name if you already have the ID. |
| space_name | `str` | No | Name of the space to create the list in. Alternative to space_id; one of them must be provided. |
| content | `str` | No | Description or content of the list. |
| due_date | `str` | No | Due date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format |
| priority | `str` | No | Priority value: 'urgent', 'high', 'normal', or 'low'. |
| assignee | `float` | No | User ID to assign the list to. Use clickup_resolve_assignees to convert email, username, or "me" to user ID if needed. |
| status | `str` | No | Status of the list. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_create_list(name="example", space_id="example", space_name="example")
```

### clickup_create_list_in_folder

Create a list in a ClickUp folder. Requires folder_id and list name. Supports content and status. If you need to get a folder ID from a folder name, use clickup_get_folder first.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | `str` | Yes | Name of the list. |
| folder_id | `str` | Yes | ID of the folder to create the list in. |
| content | `str` | No | Description or content of the list. |
| status | `str` | No | Status of the list (uses folder default if not specified). |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_create_list_in_folder(name="example", folder_id="example", content="example")
```

### clickup_get_list

Get details of a ClickUp list by ID or name. Use this tool to lookup a list ID from a list name before calling other list operations. Returns list details including id, name, content, and space info. Accepts either list_id or list_name.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| list_id | `str` | No | ID of the list to retrieve. |
| list_name | `str` | No | Name of the list to retrieve. The tool will search for a list with this name. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_get_list(list_id="example", list_name="example", workspace_id="example")
```

### clickup_update_list

Update a ClickUp list. Requires list_id + at least one update field (name/content/status). Only specified fields updated. If you need to get a list ID from a list name, use clickup_get_list first.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| list_id | `str` | Yes | ID of the list to update. |
| name | `str` | No | New name for the list. |
| content | `str` | No | New description or content for the list. |
| status | `str` | No | New status for the list. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_update_list(list_id="example", name="example", content="example")
```

### clickup_create_folder

Create folder in ClickUp space. Use space_id (preferred) or space_name + folder name. Supports override_statuses for folder-specific statuses. Use clickup_create_list_in_folder to add lists after creation.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | `str` | Yes | Name of the folder. |
| space_id | `str` | No | ID of the space to create the folder in (preferred). Provide this instead of space_name if you already have it. |
| space_name | `str` | No | Name of the space to create the folder in. Use this when space_id is not available. |
| override_statuses | `bool` | No | Whether to override space statuses with folder-specific statuses. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_create_folder(name="example", space_id="example", space_name="example")
```

### clickup_get_folder

Get details of a ClickUp folder by ID or name. Use this tool to lookup a folder ID from a folder name before calling other folder operations. Returns folder details including id, name, and space info. Accepts either folder_id or folder_name + space info.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| folder_id | `str` | No | ID of the folder to retrieve. |
| folder_name | `str` | No | Name of the folder to retrieve. When using this, you must also provide space_id or space_name. |
| space_id | `str` | No | ID of the space containing the folder (required with folder_name). |
| space_name | `str` | No | Name of the space containing the folder (required with folder_name). |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_get_folder(folder_id="example", folder_name="example", space_id="example")
```

### clickup_update_folder

Update a ClickUp folder. Requires folder_id + at least one update field (name/override_statuses). Only specified fields updated. Changes apply to all lists in folder. If you need to get a folder ID from a folder name, use clickup_get_folder first.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| folder_id | `str` | Yes | ID of the folder to update. |
| name | `str` | No | New name for the folder. |
| override_statuses | `bool` | No | Whether to override space statuses with folder-specific statuses. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_update_folder(folder_id="example", name="example", override_statuses=True)
```

### clickup_add_tag_to_task

Add existing tag to task. Tag must exist in space. Note: Will fail if tag doesn't exist.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | `str` | Yes | ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed. |
| tag_name | `str` | Yes | Name of the tag to add to the task. The tag must already exist in the space. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |

**Example:**
```python
result = await app.clickup_add_tag_to_task(task_id="example", tag_name="example", workspace_id="example")
```

### clickup_remove_tag_from_task

Remove tag from task. Only removes tag-task association, tag remains in space.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | `str` | Yes | ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed. |
| tag_name | `str` | Yes | Name of the tag to remove from the task. |
| workspace_id | `str` | No | The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home'). |


*...additional tools omitted for brevity*
