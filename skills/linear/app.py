"""Application for interacting with Linear via MCP."""
from typing import Any
from fastmcp import Client
from mcp_skill.auth import OAuth
import json

class LinearApp:
    """
    Application for interacting with Linear via MCP.
    Provides tools to interact with tools: get_attachment, create_attachment, delete_attachment, list_comments, save_comment and 26 more.
    """

    def __init__(self, url: str = "https://mcp.linear.app/mcp", auth=None) -> None:
        self.url = url
        self._oauth_auth = auth

    def _get_client(self) -> Client:
        oauth = self._oauth_auth or OAuth()
        return Client(self.url, auth=oauth)

    async def get_attachment(self, id: str) -> dict[str, Any]:
        """
        Retrieve an attachment's content by ID.

        Args:
            id: Attachment ID

        Returns:
            Tool execution result

        Tags:
            attachment
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["id"] = id
            result = await client.call_tool("get_attachment", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def create_attachment(self, base64Content: str, contentType: str, filename: str, issue: str, subtitle: str = None, title: str = None) -> dict[str, Any]:
        """
        Create a new attachment on a specific Linear issue by uploading base64-encoded content.

        Args:
            base64Content: Base64-encoded file content to upload
            contentType: MIME type for the upload (e.g., 'image/png', 'application/pdf')
            filename: Filename for the upload (e.g., 'screenshot.png')
            issue: Issue ID or identifier (e.g., LIN-123)
            subtitle: Optional subtitle for the attachment
            title: Optional title for the attachment

        Returns:
            Tool execution result

        Tags:
            create, attachment
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["base64Content"] = base64Content
            call_args["contentType"] = contentType
            call_args["filename"] = filename
            call_args["issue"] = issue
            if subtitle is not None:
                call_args["subtitle"] = subtitle
            if title is not None:
                call_args["title"] = title
            result = await client.call_tool("create_attachment", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def delete_attachment(self, id: str) -> dict[str, Any]:
        """
        Delete an attachment by ID

        Args:
            id: Attachment ID

        Returns:
            Tool execution result

        Tags:
            delete, attachment
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["id"] = id
            result = await client.call_tool("delete_attachment", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_comments(self, issueId: str) -> dict[str, Any]:
        """
        List comments for a specific Linear issue

        Args:
            issueId: Issue ID

        Returns:
            Tool execution result

        Tags:
            list, comments
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["issueId"] = issueId
            result = await client.call_tool("list_comments", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def save_comment(self, body: str, id: str = None, issueId: str = None, parentId: str = None) -> dict[str, Any]:
        """
        Create or update a comment on a Linear issue. If `id` is provided, updates the existing comment; otherwise creates a new one. When creating, `issueId` and `body` are required.

        Args:
            body: Content as Markdown
            id: Comment ID. If provided, updates the existing comment
            issueId: Issue ID (required when creating)
            parentId: Parent comment ID (for replies, only when creating)

        Returns:
            Tool execution result

        Tags:
            save, comment
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["body"] = body
            if id is not None:
                call_args["id"] = id
            if issueId is not None:
                call_args["issueId"] = issueId
            if parentId is not None:
                call_args["parentId"] = parentId
            result = await client.call_tool("save_comment", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def delete_comment(self, id: str) -> dict[str, Any]:
        """
        Delete a comment from a Linear issue

        Args:
            id: Comment ID

        Returns:
            Tool execution result

        Tags:
            delete, comment
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["id"] = id
            result = await client.call_tool("delete_comment", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_cycles(self, teamId: str, type: str = None) -> dict[str, Any]:
        """
        Retrieve cycles for a specific Linear team

        Args:
            teamId: Team ID
            type: Filter: current, previous, next, or all

        Returns:
            Tool execution result

        Tags:
            list, cycles
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["teamId"] = teamId
            if type is not None:
                call_args["type"] = type
            result = await client.call_tool("list_cycles", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_document(self, id: str) -> dict[str, Any]:
        """
        Retrieve a Linear document by ID or slug

        Args:
            id: Document ID or slug

        Returns:
            Tool execution result

        Tags:
            document
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["id"] = id
            result = await client.call_tool("get_document", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_documents(self, createdAt: str = None, creatorId: str = None, cursor: str = None, includeArchived: bool = None, initiativeId: str = None, limit: float = None, orderBy: str = None, projectId: str = None, query: str = None, updatedAt: str = None) -> dict[str, Any]:
        """
        List documents in the user's Linear workspace

        Args:
            createdAt: Created after: ISO-8601 date/duration (e.g., -P1D)
            creatorId: Filter by creator ID
            cursor: Next page cursor
            includeArchived: Include archived items
            initiativeId: Filter by initiative ID
            limit: Max results (default 50, max 250)
            orderBy: Sort: createdAt | updatedAt
            projectId: Filter by project ID
            query: Search query
            updatedAt: Updated after: ISO-8601 date/duration (e.g., -P1D)

        Returns:
            Tool execution result

        Tags:
            list, documents
        """
        async with self._get_client() as client:
            call_args = {}
            if createdAt is not None:
                call_args["createdAt"] = createdAt
            if creatorId is not None:
                call_args["creatorId"] = creatorId
            if cursor is not None:
                call_args["cursor"] = cursor
            if includeArchived is not None:
                call_args["includeArchived"] = includeArchived
            if initiativeId is not None:
                call_args["initiativeId"] = initiativeId
            if limit is not None:
                call_args["limit"] = limit
            if orderBy is not None:
                call_args["orderBy"] = orderBy
            if projectId is not None:
                call_args["projectId"] = projectId
            if query is not None:
                call_args["query"] = query
            if updatedAt is not None:
                call_args["updatedAt"] = updatedAt
            result = await client.call_tool("list_documents", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def create_document(self, title: str, color: str = None, content: str = None, icon: str = None, issue: str = None, project: str = None) -> dict[str, Any]:
        """
        Create a new document in Linear

        Args:
            title: Document title
            color: Hex color
            content: Content as Markdown
            icon: Icon emoji
            issue: Issue ID or identifier (e.g., LIN-123)
            project: Project name, ID, or slug

        Returns:
            Tool execution result

        Tags:
            create, document
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["title"] = title
            if color is not None:
                call_args["color"] = color
            if content is not None:
                call_args["content"] = content
            if icon is not None:
                call_args["icon"] = icon
            if issue is not None:
                call_args["issue"] = issue
            if project is not None:
                call_args["project"] = project
            result = await client.call_tool("create_document", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def update_document(self, id: str, color: str = None, content: str = None, icon: str = None, project: str = None, title: str = None) -> dict[str, Any]:
        """
        Update an existing Linear document

        Args:
            id: Document ID or slug
            color: Hex color
            content: Content as Markdown
            icon: Icon emoji
            project: Project name, ID, or slug
            title: Document title

        Returns:
            Tool execution result

        Tags:
            update, document
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["id"] = id
            if color is not None:
                call_args["color"] = color
            if content is not None:
                call_args["content"] = content
            if icon is not None:
                call_args["icon"] = icon
            if project is not None:
                call_args["project"] = project
            if title is not None:
                call_args["title"] = title
            result = await client.call_tool("update_document", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def extract_images(self, markdown: str) -> dict[str, Any]:
        """
        Extract and fetch images from markdown content. Use this to view screenshots, diagrams, or other images embedded in Linear issues, comments, or documents. Pass the markdown content (e.g., issue description) and receive the images as viewable data.

        Args:
            markdown: Markdown content containing image references (e.g., issue description, comment body)

        Returns:
            Tool execution result

        Tags:
            extract, images
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["markdown"] = markdown
            result = await client.call_tool("extract_images", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_issue(self, id: str, includeCustomerNeeds: bool = None, includeRelations: bool = None) -> dict[str, Any]:
        """
        Retrieve detailed information about an issue by ID, including attachments and git branch name

        Args:
            id: Issue ID
            includeCustomerNeeds: Include associated customer needs
            includeRelations: Include blocking/related/duplicate relations

        Returns:
            Tool execution result

        Tags:
            issue
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["id"] = id
            if includeCustomerNeeds is not None:
                call_args["includeCustomerNeeds"] = includeCustomerNeeds
            if includeRelations is not None:
                call_args["includeRelations"] = includeRelations
            result = await client.call_tool("get_issue", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_issues(self, assignee: str | None = None, createdAt: str = None, cursor: str = None, cycle: str = None, delegate: str = None, includeArchived: bool = None, label: str = None, limit: float = None, orderBy: str = None, parentId: str = None, priority: float = None, project: str = None, query: str = None, state: str = None, team: str = None, updatedAt: str = None) -> dict[str, Any]:
        """
        List issues in the user's Linear workspace. For my issues, use "me" as the assignee. Use "null" for no assignee.

        Args:
            assignee: User ID, name, email, or "me"
            createdAt: Created after: ISO-8601 date/duration (e.g., -P1D)
            cursor: Next page cursor
            cycle: Cycle name, number, or ID
            delegate: Agent name or ID
            includeArchived: Include archived items
            label: Label name or ID
            limit: Max results (default 50, max 250)
            orderBy: Sort: createdAt | updatedAt
            parentId: Parent issue ID
            priority: 0=None, 1=Urgent, 2=High, 3=Normal, 4=Low
            project: Project name, ID, or slug
            query: Search issue title or description
            state: State type, name, or ID
            team: Team name or ID
            updatedAt: Updated after: ISO-8601 date/duration (e.g., -P1D)

        Returns:
            Tool execution result

        Tags:
            list, issues
        """
        async with self._get_client() as client:
            call_args = {}
            if assignee is not None:
                call_args["assignee"] = assignee
            if createdAt is not None:
                call_args["createdAt"] = createdAt
            if cursor is not None:
                call_args["cursor"] = cursor
            if cycle is not None:
                call_args["cycle"] = cycle
            if delegate is not None:
                call_args["delegate"] = delegate
            if includeArchived is not None:
                call_args["includeArchived"] = includeArchived
            if label is not None:
                call_args["label"] = label
            if limit is not None:
                call_args["limit"] = limit
            if orderBy is not None:
                call_args["orderBy"] = orderBy
            if parentId is not None:
                call_args["parentId"] = parentId
            if priority is not None:
                call_args["priority"] = priority
            if project is not None:
                call_args["project"] = project
            if query is not None:
                call_args["query"] = query
            if state is not None:
                call_args["state"] = state
            if team is not None:
                call_args["team"] = team
            if updatedAt is not None:
                call_args["updatedAt"] = updatedAt
            result = await client.call_tool("list_issues", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def save_issue(self, assignee: str | None = None, blockedBy: list[str] = None, blocks: list[str] = None, cycle: str = None, delegate: str | None = None, description: str = None, dueDate: str = None, duplicateOf: str | None = None, estimate: float = None, id: str = None, labels: list[str] = None, links: list[Any] = None, milestone: str = None, parentId: str | None = None, priority: float = None, project: str = None, relatedTo: list[str] = None, state: str = None, team: str = None, title: str = None) -> dict[str, Any]:
        """
        Create or update a Linear issue. If `id` is provided, updates the existing issue; otherwise creates a new one. When creating, `title` and `team` are required.

        Args:
            assignee: User ID, name, email, or "me". Null to remove
            blockedBy: Issue IDs/identifiers blocking this. Append-only; existing relations are never removed
            blocks: Issue IDs/identifiers this blocks. Append-only; existing relations are never removed
            cycle: Cycle name, number, or ID
            delegate: Agent name or ID. Null to remove
            description: Content as Markdown
            dueDate: Due date (ISO format)
            duplicateOf: Duplicate of issue ID/identifier. Null to remove
            estimate: Issue estimate value
            id: Issue ID. If provided, updates the existing issue
            labels: Label names or IDs
            links: Link attachments to add [{url, title}]. Append-only; existing links are never removed
            milestone: Milestone name or ID
            parentId: Parent issue ID. Null to remove
            priority: 0=None, 1=Urgent, 2=High, 3=Normal, 4=Low
            project: Project name, ID, or slug
            relatedTo: Related issue IDs/identifiers. Append-only; existing relations are never removed
            state: State type, name, or ID
            team: Team name or ID (required when creating)
            title: Issue title (required when creating)

        Returns:
            Tool execution result

        Tags:
            save, issue
        """
        async with self._get_client() as client:
            call_args = {}
            if assignee is not None:
                call_args["assignee"] = assignee
            if blockedBy is not None:
                call_args["blockedBy"] = blockedBy
            if blocks is not None:
                call_args["blocks"] = blocks
            if cycle is not None:
                call_args["cycle"] = cycle
            if delegate is not None:
                call_args["delegate"] = delegate
            if description is not None:
                call_args["description"] = description
            if dueDate is not None:
                call_args["dueDate"] = dueDate
            if duplicateOf is not None:
                call_args["duplicateOf"] = duplicateOf
            if estimate is not None:
                call_args["estimate"] = estimate
            if id is not None:
                call_args["id"] = id
            if labels is not None:
                call_args["labels"] = labels
            if links is not None:
                call_args["links"] = links
            if milestone is not None:
                call_args["milestone"] = milestone
            if parentId is not None:
                call_args["parentId"] = parentId
            if priority is not None:
                call_args["priority"] = priority
            if project is not None:
                call_args["project"] = project
            if relatedTo is not None:
                call_args["relatedTo"] = relatedTo
            if state is not None:
                call_args["state"] = state
            if team is not None:
                call_args["team"] = team
            if title is not None:
                call_args["title"] = title
            result = await client.call_tool("save_issue", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_issue_statuses(self, team: str) -> dict[str, Any]:
        """
        List available issue statuses in a Linear team

        Args:
            team: Team name or ID

        Returns:
            Tool execution result

        Tags:
            list, issue, statuses
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["team"] = team
            result = await client.call_tool("list_issue_statuses", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_issue_status(self, id: str, name: str, team: str) -> dict[str, Any]:
        """
        Retrieve detailed information about an issue status in Linear by name or ID

        Args:
            id: Status ID
            name: Status name
            team: Team name or ID

        Returns:
            Tool execution result

        Tags:
            issue, status
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["id"] = id
            call_args["name"] = name
            call_args["team"] = team
            result = await client.call_tool("get_issue_status", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_issue_labels(self, cursor: str = None, limit: float = None, name: str = None, orderBy: str = None, team: str = None) -> dict[str, Any]:
        """
        List available issue labels in a Linear workspace or team

        Args:
            cursor: Next page cursor
            limit: Max results (default 50, max 250)
            name: Filter by name
            orderBy: Sort: createdAt | updatedAt
            team: Team name or ID

        Returns:
            Tool execution result

        Tags:
            list, issue, labels
        """
        async with self._get_client() as client:
            call_args = {}
            if cursor is not None:
                call_args["cursor"] = cursor
            if limit is not None:
                call_args["limit"] = limit
            if name is not None:
                call_args["name"] = name
            if orderBy is not None:
                call_args["orderBy"] = orderBy
            if team is not None:
                call_args["team"] = team
            result = await client.call_tool("list_issue_labels", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def create_issue_label(self, name: str, color: str = None, description: str = None, isGroup: bool = None, parent: str = None, teamId: str = None) -> dict[str, Any]:
        """
        Create a new Linear issue label

        Args:
            name: Label name
            color: Hex color code
            description: Label description
            isGroup: Is label group (not directly applicable)
            parent: Parent label group name
            teamId: Team UUID (omit for workspace label)

        Returns:
            Tool execution result

        Tags:
            create, issue, label
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["name"] = name
            if color is not None:
                call_args["color"] = color
            if description is not None:
                call_args["description"] = description
            if isGroup is not None:
                call_args["isGroup"] = isGroup
            if parent is not None:
                call_args["parent"] = parent
            if teamId is not None:
                call_args["teamId"] = teamId
            result = await client.call_tool("create_issue_label", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_projects(self, createdAt: str = None, cursor: str = None, includeArchived: bool = None, includeMembers: bool = None, includeMilestones: bool = None, initiative: str = None, label: str = None, limit: float = None, member: str = None, orderBy: str = None, query: str = None, state: str = None, team: str = None, updatedAt: str = None) -> dict[str, Any]:
        """
        List projects in the user's Linear workspace

        Args:
            createdAt: Created after: ISO-8601 date/duration (e.g., -P1D)
            cursor: Next page cursor
            includeArchived: Include archived items
            includeMembers: Include project members
            includeMilestones: Include milestones
            initiative: Initiative name or ID
            label: Label name or ID
            limit: Max results (default 50, max 250)
            member: User ID, name, email, or "me"
            orderBy: Sort: createdAt | updatedAt
            query: Search project name
            state: State type, name, or ID
            team: Team name or ID
            updatedAt: Updated after: ISO-8601 date/duration (e.g., -P1D)

        Returns:
            Tool execution result

        Tags:
            list, projects
        """
        async with self._get_client() as client:
            call_args = {}
            if createdAt is not None:
                call_args["createdAt"] = createdAt
            if cursor is not None:
                call_args["cursor"] = cursor
            if includeArchived is not None:
                call_args["includeArchived"] = includeArchived
            if includeMembers is not None:
                call_args["includeMembers"] = includeMembers
            if includeMilestones is not None:
                call_args["includeMilestones"] = includeMilestones
            if initiative is not None:
                call_args["initiative"] = initiative
            if label is not None:
                call_args["label"] = label
            if limit is not None:
                call_args["limit"] = limit
            if member is not None:
                call_args["member"] = member
            if orderBy is not None:
                call_args["orderBy"] = orderBy
            if query is not None:
                call_args["query"] = query
            if state is not None:
                call_args["state"] = state
            if team is not None:
                call_args["team"] = team
            if updatedAt is not None:
                call_args["updatedAt"] = updatedAt
            result = await client.call_tool("list_projects", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_project(self, query: str, includeMembers: bool = None, includeMilestones: bool = None, includeResources: bool = None) -> dict[str, Any]:
        """
        Retrieve details of a specific project in Linear

        Args:
            query: Project name, ID, or slug
            includeMembers: Include project members
            includeMilestones: Include milestones
            includeResources: Include resources (documents, links, attachments)

        Returns:
            Tool execution result

        Tags:
            project
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["query"] = query
            if includeMembers is not None:
                call_args["includeMembers"] = includeMembers
            if includeMilestones is not None:
                call_args["includeMilestones"] = includeMilestones
            if includeResources is not None:
                call_args["includeResources"] = includeResources
            result = await client.call_tool("get_project", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def save_project(self, addInitiatives: list[str] = None, addTeams: list[str] = None, color: str = None, description: str = None, icon: str = None, id: str = None, labels: list[str] = None, lead: str | None = None, name: str = None, priority: int = None, removeInitiatives: list[str] = None, removeTeams: list[str] = None, setInitiatives: list[str] = None, setTeams: list[str] = None, startDate: str = None, state: str = None, summary: str = None, targetDate: str = None) -> dict[str, Any]:
        """
        Create or update a Linear project. If `id` is provided, updates the existing project; otherwise creates a new one. When creating, `name` and at least one team (via `addTeams` or `setTeams`) are required.

        Args:
            addInitiatives: Initiative names/IDs to add
            addTeams: Team name or ID to add
            color: Hex color
            description: Content as Markdown
            icon: Icon emoji (e.g., :eagle:)
            id: Project ID. If provided, updates the existing project
            labels: Label names or IDs
            lead: User ID, name, email, or "me". Null to remove
            name: Project name (required when creating)
            priority: 0=None, 1=Urgent, 2=High, 3=Medium, 4=Low
            removeInitiatives: Initiative names/IDs to remove
            removeTeams: Team name or ID to remove
            setInitiatives: Replace all initiatives with these. Cannot combine with addInitiatives/removeInitiatives
            setTeams: Replace all teams with these. Cannot combine with addTeams/removeTeams
            startDate: Start date (ISO format)
            state: Project state
            summary: Short summary (max 255 chars)
            targetDate: Target date (ISO format)

        Returns:
            Tool execution result

        Tags:
            save, project
        """
        async with self._get_client() as client:
            call_args = {}
            if addInitiatives is not None:
                call_args["addInitiatives"] = addInitiatives
            if addTeams is not None:
                call_args["addTeams"] = addTeams
            if color is not None:
                call_args["color"] = color
            if description is not None:
                call_args["description"] = description
            if icon is not None:
                call_args["icon"] = icon
            if id is not None:
                call_args["id"] = id
            if labels is not None:
                call_args["labels"] = labels
            if lead is not None:
                call_args["lead"] = lead
            if name is not None:
                call_args["name"] = name
            if priority is not None:
                call_args["priority"] = priority
            if removeInitiatives is not None:
                call_args["removeInitiatives"] = removeInitiatives
            if removeTeams is not None:
                call_args["removeTeams"] = removeTeams
            if setInitiatives is not None:
                call_args["setInitiatives"] = setInitiatives
            if setTeams is not None:
                call_args["setTeams"] = setTeams
            if startDate is not None:
                call_args["startDate"] = startDate
            if state is not None:
                call_args["state"] = state
            if summary is not None:
                call_args["summary"] = summary
            if targetDate is not None:
                call_args["targetDate"] = targetDate
            result = await client.call_tool("save_project", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_project_labels(self, cursor: str = None, limit: float = None, name: str = None, orderBy: str = None) -> dict[str, Any]:
        """
        List available project labels in the Linear workspace

        Args:
            cursor: Next page cursor
            limit: Max results (default 50, max 250)
            name: Filter by name
            orderBy: Sort: createdAt | updatedAt

        Returns:
            Tool execution result

        Tags:
            list, project, labels
        """
        async with self._get_client() as client:
            call_args = {}
            if cursor is not None:
                call_args["cursor"] = cursor
            if limit is not None:
                call_args["limit"] = limit
            if name is not None:
                call_args["name"] = name
            if orderBy is not None:
                call_args["orderBy"] = orderBy
            result = await client.call_tool("list_project_labels", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_milestones(self, project: str) -> dict[str, Any]:
        """
        List all milestones in a Linear project

        Args:
            project: Project name, ID, or slug

        Returns:
            Tool execution result

        Tags:
            list, milestones
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["project"] = project
            result = await client.call_tool("list_milestones", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_milestone(self, project: str, query: str) -> dict[str, Any]:
        """
        Retrieve details of a specific milestone by ID or name

        Args:
            project: Project name, ID, or slug
            query: Milestone name or ID

        Returns:
            Tool execution result

        Tags:
            milestone
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["project"] = project
            call_args["query"] = query
            result = await client.call_tool("get_milestone", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def save_milestone(self, project: str, description: str = None, id: str = None, name: str = None, targetDate: str | None = None) -> dict[str, Any]:
        """
        Create or update a milestone in a Linear project. If `id` is provided, updates the existing milestone; otherwise creates a new one. When creating, `name` is required.

        Args:
            project: Project name, ID, or slug
            description: Milestone description
            id: Milestone name or ID
            name: Milestone name (required when creating)
            targetDate: Target completion date (ISO format, null to remove)

        Returns:
            Tool execution result

        Tags:
            save, milestone
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["project"] = project
            if description is not None:
                call_args["description"] = description
            if id is not None:
                call_args["id"] = id
            if name is not None:
                call_args["name"] = name
            if targetDate is not None:
                call_args["targetDate"] = targetDate
            result = await client.call_tool("save_milestone", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_teams(self, createdAt: str = None, cursor: str = None, includeArchived: bool = None, limit: float = None, orderBy: str = None, query: str = None, updatedAt: str = None) -> dict[str, Any]:
        """
        List teams in the user's Linear workspace

        Args:
            createdAt: Created after: ISO-8601 date/duration (e.g., -P1D)
            cursor: Next page cursor
            includeArchived: Include archived items
            limit: Max results (default 50, max 250)
            orderBy: Sort: createdAt | updatedAt
            query: Search query
            updatedAt: Updated after: ISO-8601 date/duration (e.g., -P1D)

        Returns:
            Tool execution result

        Tags:
            list, teams
        """
        async with self._get_client() as client:
            call_args = {}
            if createdAt is not None:
                call_args["createdAt"] = createdAt
            if cursor is not None:
                call_args["cursor"] = cursor
            if includeArchived is not None:
                call_args["includeArchived"] = includeArchived
            if limit is not None:
                call_args["limit"] = limit
            if orderBy is not None:
                call_args["orderBy"] = orderBy
            if query is not None:
                call_args["query"] = query
            if updatedAt is not None:
                call_args["updatedAt"] = updatedAt
            result = await client.call_tool("list_teams", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_team(self, query: str) -> dict[str, Any]:
        """
        Retrieve details of a specific Linear team

        Args:
            query: Team UUID, key, or name

        Returns:
            Tool execution result

        Tags:
            team
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["query"] = query
            result = await client.call_tool("get_team", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def list_users(self, cursor: str = None, limit: float = None, orderBy: str = None, query: str = None, team: str = None) -> dict[str, Any]:
        """
        Retrieve users in the Linear workspace

        Args:
            cursor: Next page cursor
            limit: Max results (default 50, max 250)
            orderBy: Sort: createdAt | updatedAt
            query: Filter by name or email
            team: Team name or ID

        Returns:
            Tool execution result

        Tags:
            list, users
        """
        async with self._get_client() as client:
            call_args = {}
            if cursor is not None:
                call_args["cursor"] = cursor
            if limit is not None:
                call_args["limit"] = limit
            if orderBy is not None:
                call_args["orderBy"] = orderBy
            if query is not None:
                call_args["query"] = query
            if team is not None:
                call_args["team"] = team
            result = await client.call_tool("list_users", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def get_user(self, query: str) -> dict[str, Any]:
        """
        Retrieve details of a specific Linear user

        Args:
            query: User ID, name, email, or "me"

        Returns:
            Tool execution result

        Tags:
            user
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["query"] = query
            result = await client.call_tool("get_user", call_args)
            texts = []
            for block in result.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
            text = "\n".join(texts)
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return {"result": text}

    async def search_documentation(self, query: str, page: float = None) -> dict[str, Any]:
        """
        Search Linear's documentation to learn about features and usage

        Args:
            query: Search query
            page: Page number

        Returns:
            Tool execution result

        Tags:
            search, documentation
        """
        async with self._get_client() as client:
            call_args = {}
            call_args["query"] = query
            if page is not None:
                call_args["page"] = page
            result = await client.call_tool("search_documentation", call_args)
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
        return [self.get_attachment, self.create_attachment, self.delete_attachment, self.list_comments, self.save_comment, self.delete_comment, self.list_cycles, self.get_document, self.list_documents, self.create_document, self.update_document, self.extract_images, self.get_issue, self.list_issues, self.save_issue, self.list_issue_statuses, self.get_issue_status, self.list_issue_labels, self.create_issue_label, self.list_projects, self.get_project, self.save_project, self.list_project_labels, self.list_milestones, self.get_milestone, self.save_milestone, self.list_teams, self.get_team, self.list_users, self.get_user, self.search_documentation]
