"""Application for interacting with Clickup via MCP."""
from typing import Any
from fastmcp import Client
from mcp_skill.auth import OAuth
import json

class ClickupApp:
    """
    Application for interacting with Clickup via MCP.
    Provides tools to interact with tools: clickup_search, clickup_get_workspace_hierarchy, clickup_create_task, clickup_get_task, clickup_update_task and 27 more.
    """

    def __init__(self, url: str = "https://mcp.clickup.com/mcp", auth=None) -> None:
        self.url = url
        self._oauth_auth = auth

    def _get_client(self) -> Client:
        oauth = self._oauth_auth or OAuth()
        return Client(self.url, auth=oauth)

    async def clickup_search(self, count: float = None, cursor: str = None, filters: dict[str, Any] = None, keywords: str = None, sort: list[Any] = None, workspace_id: str = None) -> dict[str, Any]:
        """
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

        Args:
            count: Maximum number of results to return per page (for pagination)
            cursor: Pagination cursor from previous response. Use to fetch next page of results
            filters: Filters to refine search results by various criteria
            keywords: Search query string. Use specific keywords to find items
            sort: Sort criteria for results. Can specify multiple sort fields in priority order
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, search
        """
        async with self._get_client() as client:
            call_args = {}
            if count is not None:
                call_args["count"] = count
            if cursor is not None:
                call_args["cursor"] = cursor
            if filters is not None:
                call_args["filters"] = filters
            if keywords is not None:
                call_args["keywords"] = keywords
            if sort is not None:
                call_args["sort"] = sort
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_search", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_get_workspace_hierarchy(self, cursor: str = None, limit: float = None, max_depth: str = None, space_ids: list[str] = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Get workspace hierarchy (spaces, folders, lists) from your authenticated workspace with pagination support. Workspace ID is automatically detected from your session. Returns tree structure with names and IDs for navigation. Supports pagination for large workspaces and depth control to fetch only needed levels. Note: Use this ONLY when you need to see the workspace structure - most tools can resolve names automatically without this lookup.

        Args:
            cursor: Pagination cursor from previous response. Use to fetch next page of spaces
            limit: Maximum number of spaces to return per page (default: 10, max: 50)
            max_depth: Maximum depth of hierarchy to return: 0=spaces only, 1=spaces+folders, 2=spaces+folders+lists (default: 2)
            space_ids: Filter to return only specific spaces by ID.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, workspace, hierarchy
        """
        async with self._get_client() as client:
            call_args = {}
            if cursor is not None:
                call_args["cursor"] = cursor
            if limit is not None:
                call_args["limit"] = limit
            if max_depth is not None:
                call_args["max_depth"] = max_depth
            if space_ids is not None:
                call_args["space_ids"] = space_ids
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_get_workspace_hierarchy", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_create_task(self, list_id: str, name: str, assignees: list[str] = None, check_required_custom_fields: bool = None, custom_fields: list[Any] = None, description: str = None, due_date: str = None, markdown_description: str = None, parent: str = None, priority: str = None, start_date: str = None, status: str = None, tags: list[str] = None, task_type: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Create task in a ClickUp list. Requires task name and list_id. ALWAYS ask user which list to use - never guess. Use clickup_get_list to resolve list names to IDs. Supports assignees as array of user IDs, emails, usernames, or "me". Supports task_type to specify the task type by name (e.g., 'Bug', 'Feature').

        Args:
            list_id: ID of the list where the task should be created. Use clickup_get_list to find the list ID from a list name if needed.
            name: Task name. Ask the user what they want to name the task.
            assignees: Array of assignee user IDs (as strings). Use clickup_resolve_assignees to convert emails, usernames, or "me" to user IDs if needed.
            check_required_custom_fields: Flag to check if all required custom fields are set before saving the task.
            custom_fields: Array of custom field values to set on the task. Each object must have an 'id' and 'value' property.
            description: Plain text description for the task.
            due_date: Due date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format (e.g., '2025-12-31' or '2025-12-31 14:30')
            markdown_description: Markdown formatted description for the task. If provided, this takes precedence over description.
            parent: ID of the parent task. When specified, this task will be created as a subtask of the specified parent task.
            priority: Task priority: 'urgent', 'high', 'normal', or 'low'. If not provided, task will have no priority assigned.
            start_date: Start date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format (e.g., '2025-01-01' or '2025-01-01 09:00')
            status: Override the default ClickUp status. In most cases, omit this to use ClickUp defaults.
            tags: Array of tag names to assign to the task. The tags must already exist in the space.
            task_type: Name of the task type (e.g., 'Bug', 'Feature', 'Milestone'). The type must exist in the workspace. If not specified, the default task type will be used.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, create, task
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["list_id"] = list_id
            call_args["name"] = name
            if assignees is not None:
                call_args["assignees"] = assignees
            if check_required_custom_fields is not None:
                call_args["check_required_custom_fields"] = check_required_custom_fields
            if custom_fields is not None:
                call_args["custom_fields"] = custom_fields
            if description is not None:
                call_args["description"] = description
            if due_date is not None:
                call_args["due_date"] = due_date
            if markdown_description is not None:
                call_args["markdown_description"] = markdown_description
            if parent is not None:
                call_args["parent"] = parent
            if priority is not None:
                call_args["priority"] = priority
            if start_date is not None:
                call_args["start_date"] = start_date
            if status is not None:
                call_args["status"] = status
            if tags is not None:
                call_args["tags"] = tags
            if task_type is not None:
                call_args["task_type"] = task_type
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_create_task", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_get_task(self, task_id: str, detail_level: str = None, subtasks: bool = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Get task details by task_id (works with regular/custom IDs). Set subtasks=true to include all subtask details.

Response Size Optimization:
- Use detail_level='summary' for lightweight responses when full details aren't needed
- Responses exceeding 50,000 tokens automatically switch to summary format to prevent client issues
- Summary format includes essential fields: id, name, status, description (truncated), assignees, tags, due_date, url

        Args:
            task_id: ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed.
            detail_level: Level of detail to return. Use 'summary' for lightweight responses or 'detailed' for full task data. Defaults to 'detailed' but automatically switches to 'summary' if response would be too large.
            subtasks: Whether to include subtasks in the response. Set to true to retrieve full details of all subtasks.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, task
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["task_id"] = task_id
            if detail_level is not None:
                call_args["detail_level"] = detail_level
            if subtasks is not None:
                call_args["subtasks"] = subtasks
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_get_task", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_update_task(self, task_id: str, assignees: list[str] = None, custom_fields: list[Any] = None, description: str = None, due_date: str | None = None, markdown_description: str = None, name: str = None, priority: str | None = None, start_date: str | None = None, status: str = None, task_type: str | None = None, time_estimate: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Update task properties. Requires task_id and at least one update field. Custom fields supported as array of {id, value}. Supports assignees as array of user IDs, emails, usernames, or "me". Supports task_type to change the task type by name (e.g., 'Bug', 'Feature'), or null to reset to default.

        Args:
            task_id: ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed.
            assignees: Array of assignee user IDs (as strings). Use clickup_resolve_assignees to convert emails, usernames, or "me" to user IDs if needed.
            custom_fields: Array of custom field values to set on the task. Each object must have an 'id' and 'value' property.
            description: New plain text description. Will be ignored if markdown_description is provided.
            due_date: Due date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format (e.g., '2025-12-31' or '2025-12-31 14:30'), or null to clear. If not provided, due date will not be changed.
            markdown_description: New markdown description. Takes precedence over plain text description.
            name: New name for the task.
            priority: Task priority: 'urgent', 'high', 'normal', 'low', or null to clear. If not provided, priority will not be changed.
            start_date: Start date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format (e.g., '2025-01-01' or '2025-01-01 09:00'), or null to clear. If not provided, start date will not be changed.
            status: New status. Must be valid for the task's current list.
            task_type: Name of the task type to change to (e.g., 'Bug', 'Feature', 'Milestone'). The type must exist in the workspace. Pass null to revert to the default 'Task' type.
            time_estimate: Time estimate for the task. For best compatibility with the ClickUp API, use a numeric value in minutes (e.g., '150' for 2h 30m)
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, update, task
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["task_id"] = task_id
            if assignees is not None:
                call_args["assignees"] = assignees
            if custom_fields is not None:
                call_args["custom_fields"] = custom_fields
            if description is not None:
                call_args["description"] = description
            if due_date is not None:
                call_args["due_date"] = due_date
            if markdown_description is not None:
                call_args["markdown_description"] = markdown_description
            if name is not None:
                call_args["name"] = name
            if priority is not None:
                call_args["priority"] = priority
            if start_date is not None:
                call_args["start_date"] = start_date
            if status is not None:
                call_args["status"] = status
            if task_type is not None:
                call_args["task_type"] = task_type
            if time_estimate is not None:
                call_args["time_estimate"] = time_estimate
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_update_task", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_get_task_comments(self, task_id: str, start: float = None, start_id: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Get task comments. Use start/start_id params for pagination.

        Args:
            task_id: ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed.
            start: Timestamp (in milliseconds) to start retrieving comments from. Used for pagination.
            start_id: Comment ID to start from. Used together with start for pagination.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, task, comments
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["task_id"] = task_id
            if start is not None:
                call_args["start"] = start
            if start_id is not None:
                call_args["start_id"] = start_id
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_get_task_comments", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_create_task_comment(self, comment_text: str, task_id: str, assignee: float = None, notify_all: bool = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Create task comment. Requires task_id and comment_text. Supports notify_all to alert assignees and assignee to assign the comment.

        Args:
            comment_text: Text content of the comment to create.
            task_id: ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed.
            assignee: User ID to assign the comment to. Use clickup_resolve_assignees to convert email, username, or "me" to user ID if needed.
            notify_all: Whether to notify all assignees. Default is false.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, create, task, comment
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["comment_text"] = comment_text
            call_args["task_id"] = task_id
            if assignee is not None:
                call_args["assignee"] = assignee
            if notify_all is not None:
                call_args["notify_all"] = notify_all
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_create_task_comment", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_attach_task_file(self, task_id: str, auth_header: str = None, file_data: str = None, file_name: str = None, file_url: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Attach file to task. Requires task_id. File sources: 1) base64 + filename, 2) URL (http/https).

        Args:
            task_id: ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed.
            auth_header: Authorization header to use when downloading from the web URL.
            file_data: Base64-encoded content of the file (without the data URL prefix).
            file_name: Name of the file to be attached (include the extension). Required when using file_data.
            file_url: URL to download the file from (must start with http:// or https://).
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, attach, task, file
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["task_id"] = task_id
            if auth_header is not None:
                call_args["auth_header"] = auth_header
            if file_data is not None:
                call_args["file_data"] = file_data
            if file_name is not None:
                call_args["file_name"] = file_name
            if file_url is not None:
                call_args["file_url"] = file_url
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_attach_task_file", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_get_task_time_entries(self, task_id: str, end_date: str = None, is_billable: bool = None, start_date: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Get all time entries for a task with filtering options. Returns all tracked time with user info, descriptions, tags, start/end times, and durations.

        Args:
            task_id: ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed.
            end_date: End date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format
            is_billable: Filter by billable status. Set to true to get only billable time entries, false for non-billable entries. Omit to get all entries regardless of billable status.
            start_date: Start date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, task, time, entries
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["task_id"] = task_id
            if end_date is not None:
                call_args["end_date"] = end_date
            if is_billable is not None:
                call_args["is_billable"] = is_billable
            if start_date is not None:
                call_args["start_date"] = start_date
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_get_task_time_entries", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_start_time_tracking(self, task_id: str, billable: bool = None, description: str = None, tags: list[str] = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Start time tracking on a task. Supports description, billable status, and tags. Only one timer can be running at a time. For best results, omit extra parameters unless specifically needed.

        Args:
            task_id: ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed.
            billable: Whether this time is billable. Default is workspace setting.
            description: Description for the time entry. Keep short and simple, or omit for best compatibility.
            tags: Array of tag names to assign to the time entry.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, start, time, tracking
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["task_id"] = task_id
            if billable is not None:
                call_args["billable"] = billable
            if description is not None:
                call_args["description"] = description
            if tags is not None:
                call_args["tags"] = tags
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_start_time_tracking", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_stop_time_tracking(self, description: str = None, tags: list[str] = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Stop the currently running time tracker. Supports description and tags. Returns the completed time entry details.

        Args:
            description: Description to update or add to the time entry.
            tags: Array of tag names to assign to the time entry.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, stop, time, tracking
        """
        async with self._get_client() as client:
            call_args = {}
            if description is not None:
                call_args["description"] = description
            if tags is not None:
                call_args["tags"] = tags
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_stop_time_tracking", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_add_time_entry(self, start: str, task_id: str, billable: bool = None, description: str = None, duration: str = None, end_time: str = None, tags: list[str] = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Add a manual time entry to a task. You can provide either (start + duration) OR (start + end). The tool will calculate missing values. Requires task_id, start time, and either duration or end time. Supports description, billable flag, and tags.

        Args:
            start: Start time in YYYY-MM-DD HH:MM format (e.g., '2025-01-15 09:30'). Time is required for time tracking entries.
            task_id: ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed.
            billable: Whether this time is billable. Default is workspace setting.
            description: Description for the time entry. Keep short and simple, or omit for best compatibility.
            duration: Duration of the time entry. Format as 'Xh Ym' (e.g., '1h 30m') or just minutes (e.g., '90m'). Either duration or end_time is required.
            end_time: End time in YYYY-MM-DD HH:MM format (e.g., '2025-01-15 11:00'). Time is required for time tracking entries.
            tags: Array of tag names to assign to the time entry.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, add, time, entry
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["start"] = start
            call_args["task_id"] = task_id
            if billable is not None:
                call_args["billable"] = billable
            if description is not None:
                call_args["description"] = description
            if duration is not None:
                call_args["duration"] = duration
            if end_time is not None:
                call_args["end_time"] = end_time
            if tags is not None:
                call_args["tags"] = tags
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_add_time_entry", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_get_current_time_entry(self, workspace_id: str = None) -> dict[str, Any]:
        """
        Get the currently running time entry, if any. No parameters needed.

        Args:
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, current, time, entry
        """
        async with self._get_client() as client:
            call_args = {}
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_get_current_time_entry", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_create_list(self, name: str, assignee: float = None, content: str = None, due_date: str = None, priority: str = None, space_id: str = None, space_name: str = None, status: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Create a list in a ClickUp space efficiently. The system automatically detects workspace ID and resolves space names. Use space_name (preferred for simplicity) or space_id + list name. Name is required. For lists in folders, use clickup_create_list_in_folder. Supports content, due_date, priority, assignee, and status. Note: No need to look up workspace hierarchy or space IDs first - the system handles space name resolution automatically.

        Args:
            name: Name of the list.
            assignee: User ID to assign the list to. Use clickup_resolve_assignees to convert email, username, or "me" to user ID if needed.
            content: Description or content of the list.
            due_date: Due date in YYYY-MM-DD format or date-time in YYYY-MM-DD HH:MM format
            priority: Priority value: 'urgent', 'high', 'normal', or 'low'.
            space_id: ID of the space to create the list in. Provide this instead of space_name if you already have the ID.
            space_name: Name of the space to create the list in. Alternative to space_id; one of them must be provided.
            status: Status of the list.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, create, list
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["name"] = name
            if assignee is not None:
                call_args["assignee"] = assignee
            if content is not None:
                call_args["content"] = content
            if due_date is not None:
                call_args["due_date"] = due_date
            if priority is not None:
                call_args["priority"] = priority
            if space_id is not None:
                call_args["space_id"] = space_id
            if space_name is not None:
                call_args["space_name"] = space_name
            if status is not None:
                call_args["status"] = status
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_create_list", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_create_list_in_folder(self, folder_id: str, name: str, content: str = None, status: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Create a list in a ClickUp folder. Requires folder_id and list name. Supports content and status. If you need to get a folder ID from a folder name, use clickup_get_folder first.

        Args:
            folder_id: ID of the folder to create the list in.
            name: Name of the list.
            content: Description or content of the list.
            status: Status of the list (uses folder default if not specified).
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, create, list, folder
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["folder_id"] = folder_id
            call_args["name"] = name
            if content is not None:
                call_args["content"] = content
            if status is not None:
                call_args["status"] = status
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_create_list_in_folder", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_get_list(self, list_id: str = None, list_name: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Get details of a ClickUp list by ID or name. Use this tool to lookup a list ID from a list name before calling other list operations. Returns list details including id, name, content, and space info. Accepts either list_id or list_name.

        Args:
            list_id: ID of the list to retrieve.
            list_name: Name of the list to retrieve. The tool will search for a list with this name.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, list
        """
        async with self._get_client() as client:
            call_args = {}
            if list_id is not None:
                call_args["list_id"] = list_id
            if list_name is not None:
                call_args["list_name"] = list_name
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_get_list", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_update_list(self, list_id: str, content: str = None, name: str = None, status: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Update a ClickUp list. Requires list_id + at least one update field (name/content/status). Only specified fields updated. If you need to get a list ID from a list name, use clickup_get_list first.

        Args:
            list_id: ID of the list to update.
            content: New description or content for the list.
            name: New name for the list.
            status: New status for the list.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, update, list
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["list_id"] = list_id
            if content is not None:
                call_args["content"] = content
            if name is not None:
                call_args["name"] = name
            if status is not None:
                call_args["status"] = status
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_update_list", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_create_folder(self, name: str, override_statuses: bool = None, space_id: str = None, space_name: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Create folder in ClickUp space. Use space_id (preferred) or space_name + folder name. Supports override_statuses for folder-specific statuses. Use clickup_create_list_in_folder to add lists after creation.

        Args:
            name: Name of the folder.
            override_statuses: Whether to override space statuses with folder-specific statuses.
            space_id: ID of the space to create the folder in (preferred). Provide this instead of space_name if you already have it.
            space_name: Name of the space to create the folder in. Use this when space_id is not available.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, create, folder
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["name"] = name
            if override_statuses is not None:
                call_args["override_statuses"] = override_statuses
            if space_id is not None:
                call_args["space_id"] = space_id
            if space_name is not None:
                call_args["space_name"] = space_name
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_create_folder", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_get_folder(self, folder_id: str = None, folder_name: str = None, space_id: str = None, space_name: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Get details of a ClickUp folder by ID or name. Use this tool to lookup a folder ID from a folder name before calling other folder operations. Returns folder details including id, name, and space info. Accepts either folder_id or folder_name + space info.

        Args:
            folder_id: ID of the folder to retrieve.
            folder_name: Name of the folder to retrieve. When using this, you must also provide space_id or space_name.
            space_id: ID of the space containing the folder (required with folder_name).
            space_name: Name of the space containing the folder (required with folder_name).
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, folder
        """
        async with self._get_client() as client:
            call_args = {}
            if folder_id is not None:
                call_args["folder_id"] = folder_id
            if folder_name is not None:
                call_args["folder_name"] = folder_name
            if space_id is not None:
                call_args["space_id"] = space_id
            if space_name is not None:
                call_args["space_name"] = space_name
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_get_folder", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_update_folder(self, folder_id: str, name: str = None, override_statuses: bool = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Update a ClickUp folder. Requires folder_id + at least one update field (name/override_statuses). Only specified fields updated. Changes apply to all lists in folder. If you need to get a folder ID from a folder name, use clickup_get_folder first.

        Args:
            folder_id: ID of the folder to update.
            name: New name for the folder.
            override_statuses: Whether to override space statuses with folder-specific statuses.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, update, folder
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["folder_id"] = folder_id
            if name is not None:
                call_args["name"] = name
            if override_statuses is not None:
                call_args["override_statuses"] = override_statuses
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_update_folder", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_add_tag_to_task(self, tag_name: str, task_id: str, workspace_id: str = None) -> dict[str, Any]:
        """
        Add existing tag to task. Tag must exist in space. Note: Will fail if tag doesn't exist.

        Args:
            tag_name: Name of the tag to add to the task. The tag must already exist in the space.
            task_id: ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, add, tag, task
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["tag_name"] = tag_name
            call_args["task_id"] = task_id
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_add_tag_to_task", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_remove_tag_from_task(self, tag_name: str, task_id: str, workspace_id: str = None) -> dict[str, Any]:
        """
        Remove tag from task. Only removes tag-task association, tag remains in space.

        Args:
            tag_name: Name of the tag to remove from the task.
            task_id: ID of task. Works with both regular task IDs and custom IDs (like 'DEV-1234'). Use clickup_search to find task ID by name if needed.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, remove, tag, from, task
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["tag_name"] = tag_name
            call_args["task_id"] = task_id
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_remove_tag_from_task", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_get_workspace_members(self, workspace_id: str = None) -> dict[str, Any]:
        """
        Get all members (users) in the ClickUp workspace/team from your authenticated workspace. No parameters needed - workspace ID is automatically detected. Note: Most tools automatically resolve assignees by name or email without needing this lookup first. Use this ONLY when you need to see all available members.

        Args:
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, workspace, members
        """
        async with self._get_client() as client:
            call_args = {}
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_get_workspace_members", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_find_member_by_name(self, name_or_email: str, workspace_id: str = None) -> dict[str, Any]:
        """
        Get a member in the ClickUp workspace by name or email. Returns the member object if found, or null if not found.

        Args:
            name_or_email: The name or email of the member to find.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, find, member, name
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["name_or_email"] = name_or_email
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_find_member_by_name", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_resolve_assignees(self, assignees: list[str], workspace_id: str = None) -> dict[str, Any]:
        """
        Resolve an array of assignee names or emails to ClickUp user IDs. Returns an array of user IDs, or null for any that cannot be resolved. Note: Most task tools automatically resolve assignees - use this only when you need the user IDs separately.

        Args:
            assignees: Array of assignee names or emails to resolve.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, resolve, assignees
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["assignees"] = assignees
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_resolve_assignees", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_get_chat_channels(self, cursor: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Get chat channels in a workspace. Allows you to see available chat channels including their members, privacy settings, and creation details. Supports pagination using the cursor parameter.

        Args:
            cursor: Cursor for pagination. Use the next_cursor value from the previous response to fetch the next page of results.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, chat, channels
        """
        async with self._get_client() as client:
            call_args = {}
            if cursor is not None:
                call_args["cursor"] = cursor
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_get_chat_channels", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_send_chat_message(self, channel_id: str, content: str, assignee: str = None, content_format: str = None, followers: list[str] = None, group_assignee: str = None, post_subtype_id: str = None, post_title: str = None, type: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Send a message to a specific chat channel in the workspace. Messages can be either simple messages or posts with additional metadata.

        Args:
            channel_id: ID of the chat channel to send the message to.
            content: Message content to send (supports markdown).
            assignee: User ID to assign the message to. Use clickup_resolve_assignees to convert email, username, or "me" to user ID if needed.
            content_format: Format of the message content.
            followers: Array of user IDs to add as followers of the message. Use clickup_resolve_assignees to convert emails, usernames, or "me" to user IDs if needed.
            group_assignee: Group ID to assign the message to.
            post_subtype_id: Subtype ID for the post (required if type is 'post').
            post_title: Title for the post (required if type is 'post').
            type: Type of message to send.
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, send, chat, message
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["channel_id"] = channel_id
            call_args["content"] = content
            if assignee is not None:
                call_args["assignee"] = assignee
            if content_format is not None:
                call_args["content_format"] = content_format
            if followers is not None:
                call_args["followers"] = followers
            if group_assignee is not None:
                call_args["group_assignee"] = group_assignee
            if post_subtype_id is not None:
                call_args["post_subtype_id"] = post_subtype_id
            if post_title is not None:
                call_args["post_title"] = post_title
            if type is not None:
                call_args["type"] = type
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_send_chat_message", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_create_document(self, create_page: bool, name: str, parent: dict[str, Any], visibility: str, workspace_id: str = None) -> dict[str, Any]:
        """
        Create a document in a ClickUp space, folder, or list. Requires name, parent info, visibility and create_page flag.

        Args:
            create_page: Whether to create an initial blank page
            name: Name and Title of the document
            parent: Parent container information
            visibility: Document visibility setting
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, create, document
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["create_page"] = create_page
            call_args["name"] = name
            call_args["parent"] = parent
            call_args["visibility"] = visibility
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_create_document", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_list_document_pages(self, document_id: str, max_page_depth: float = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Get all pages in a document with optional depth control.

        Args:
            document_id: ID of the document to list pages from
            max_page_depth: Maximum depth of pages to retrieve (-1 for unlimited)
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, list, document, pages
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["document_id"] = document_id
            if max_page_depth is not None:
                call_args["max_page_depth"] = max_page_depth
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_list_document_pages", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_get_document_pages(self, document_id: str, page_ids: list[str], content_format: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Get the content of specific pages from a document.

        Args:
            document_id: ID of the document to get pages from
            page_ids: Array of page IDs to retrieve
            content_format: Format of the content to retrieve
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, document, pages
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["document_id"] = document_id
            call_args["page_ids"] = page_ids
            if content_format is not None:
                call_args["content_format"] = content_format
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_get_document_pages", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_create_document_page(self, content: str, document_id: str, name: str, content_format: str = None, parent_page_id: str = None, sub_title: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Create a new page in a ClickUp document.

        Args:
            content: Content of the page
            document_id: ID of the document to create the page in
            name: Name and title of the page
            content_format: The format of the page content
            parent_page_id: ID of the parent page (if this is a sub-page)
            sub_title: Subtitle of the page
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, create, document, page
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["content"] = content
            call_args["document_id"] = document_id
            call_args["name"] = name
            if content_format is not None:
                call_args["content_format"] = content_format
            if parent_page_id is not None:
                call_args["parent_page_id"] = parent_page_id
            if sub_title is not None:
                call_args["sub_title"] = sub_title
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_create_document_page", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def clickup_update_document_page(self, document_id: str, page_id: str, content: str = None, content_edit_mode: str = None, content_format: str = None, name: str = None, sub_title: str = None, workspace_id: str = None) -> dict[str, Any]:
        """
        Update an existing page in a ClickUp document. Supports updating name, subtitle, and content with different edit modes (replace/append/prepend).

        Args:
            document_id: ID of the document containing the page
            page_id: ID of the page to update
            content: New content for the page
            content_edit_mode: How to update the content. Defaults to replace
            content_format: The format of the page content
            name: New name for the page
            sub_title: New subtitle for the page
            workspace_id: The unique identifier for the ClickUp workspace. When not provided, this will be automatically populated with your authenticated workspace ID. Only provide this parameter to override the detected workspace. You can find your Workspace ID in the URL when in your workspace (format: 'xxxxxxxx' in 'https://app.clickup.com/xxxxxxxx/home').

        Returns:
            Tool execution result

        Tags:
            clickup, update, document, page
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["document_id"] = document_id
            call_args["page_id"] = page_id
            if content is not None:
                call_args["content"] = content
            if content_edit_mode is not None:
                call_args["content_edit_mode"] = content_edit_mode
            if content_format is not None:
                call_args["content_format"] = content_format
            if name is not None:
                call_args["name"] = name
            if sub_title is not None:
                call_args["sub_title"] = sub_title
            if workspace_id is not None:
                call_args["workspace_id"] = workspace_id
            result = await client.call_tool("clickup_update_document_page", call_args)
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
        return [self.clickup_search, self.clickup_get_workspace_hierarchy, self.clickup_create_task, self.clickup_get_task, self.clickup_update_task, self.clickup_get_task_comments, self.clickup_create_task_comment, self.clickup_attach_task_file, self.clickup_get_task_time_entries, self.clickup_start_time_tracking, self.clickup_stop_time_tracking, self.clickup_add_time_entry, self.clickup_get_current_time_entry, self.clickup_create_list, self.clickup_create_list_in_folder, self.clickup_get_list, self.clickup_update_list, self.clickup_create_folder, self.clickup_get_folder, self.clickup_update_folder, self.clickup_add_tag_to_task, self.clickup_remove_tag_from_task, self.clickup_get_workspace_members, self.clickup_find_member_by_name, self.clickup_resolve_assignees, self.clickup_get_chat_channels, self.clickup_send_chat_message, self.clickup_create_document, self.clickup_list_document_pages, self.clickup_get_document_pages, self.clickup_create_document_page, self.clickup_update_document_page]
