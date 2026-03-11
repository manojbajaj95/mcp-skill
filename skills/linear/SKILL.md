---
name: linear
description: "MCP skill for linear. Provides 31 tools: get_attachment, create_attachment, delete_attachment, list_comments, save_comment, delete_comment, list_cycles, get_document, list_documents, create_document, update_document, extract_images, get_issue, list_issues, save_issue, list_issue_statuses, get_issue_status, list_issue_labels, create_issue_label, list_projects, get_project, save_project, list_project_labels, list_milestones, get_milestone, save_milestone, list_teams, get_team, list_users, get_user, search_documentation"
---

# linear

MCP skill for linear. Provides 31 tools: get_attachment, create_attachment, delete_attachment, list_comments, save_comment, delete_comment, list_cycles, get_document, list_documents, create_document, update_document, extract_images, get_issue, list_issues, save_issue, list_issue_statuses, get_issue_status, list_issue_labels, create_issue_label, list_projects, get_project, save_project, list_project_labels, list_milestones, get_milestone, save_milestone, list_teams, get_team, list_users, get_user, search_documentation

## Authentication

This MCP server uses **OAuth** authentication.
The OAuth flow is handled automatically by the MCP client. Tokens are persisted
to `~/.mcp-skill/auth/` so subsequent runs reuse the same credentials without
re-authenticating.

```python
app = LinearApp()  # uses default OAuth flow
```

To bring your own OAuth provider, pass it via the `auth` argument:

```python
app = LinearApp(auth=my_oauth_provider)
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
from linear.app import LinearApp
```

Or set the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=".agents/skills:$PYTHONPATH"
```

**Preferred: use `uv run`** (handles dependencies automatically):

```bash
PYTHONPATH=.agents/skills uv run --with mcp-skill python -c "
import asyncio
from linear.app import LinearApp

async def main():
    app = LinearApp()
    result = await app.get_attachment(id="example")
    print(result)

asyncio.run(main())
"
```

**Alternative: use `python` directly** (install dependencies first):

```bash
pip install mcp-skill
PYTHONPATH=.agents/skills python -c "
import asyncio
from linear.app import LinearApp

async def main():
    app = LinearApp()
    result = await app.get_attachment(id="example")
    print(result)

asyncio.run(main())
"
```

## Available Tools

### get_attachment

Retrieve an attachment's content by ID.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | Yes | Attachment ID |

**Example:**
```python
result = await app.get_attachment(id="example")
```

### create_attachment

Create a new attachment on a specific Linear issue by uploading base64-encoded content.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| issue | `str` | Yes | Issue ID or identifier (e.g., LIN-123) |
| base64Content | `str` | Yes | Base64-encoded file content to upload |
| filename | `str` | Yes | Filename for the upload (e.g., 'screenshot.png') |
| contentType | `str` | Yes | MIME type for the upload (e.g., 'image/png', 'application/pdf') |
| title | `str` | No | Optional title for the attachment |
| subtitle | `str` | No | Optional subtitle for the attachment |

**Example:**
```python
result = await app.create_attachment(issue="example", base64Content="example", filename="example")
```

### delete_attachment

Delete an attachment by ID

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | Yes | Attachment ID |

**Example:**
```python
result = await app.delete_attachment(id="example")
```

### list_comments

List comments for a specific Linear issue

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| issueId | `str` | Yes | Issue ID |

**Example:**
```python
result = await app.list_comments(issueId="example")
```

### save_comment

Create or update a comment on a Linear issue. If `id` is provided, updates the existing comment; otherwise creates a new one. When creating, `issueId` and `body` are required.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | No | Comment ID. If provided, updates the existing comment |
| issueId | `str` | No | Issue ID (required when creating) |
| parentId | `str` | No | Parent comment ID (for replies, only when creating) |
| body | `str` | Yes | Content as Markdown |

**Example:**
```python
result = await app.save_comment(id="example", issueId="example", parentId="example")
```

### delete_comment

Delete a comment from a Linear issue

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | Yes | Comment ID |

**Example:**
```python
result = await app.delete_comment(id="example")
```

### list_cycles

Retrieve cycles for a specific Linear team

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| teamId | `str` | Yes | Team ID |
| type | `str` | No | Filter: current, previous, next, or all |

**Example:**
```python
result = await app.list_cycles(teamId="example", type="example")
```

### get_document

Retrieve a Linear document by ID or slug

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | Yes | Document ID or slug |

**Example:**
```python
result = await app.get_document(id="example")
```

### list_documents

List documents in the user's Linear workspace

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | `float` | No | Max results (default 50, max 250) |
| cursor | `str` | No | Next page cursor |
| orderBy | `str` | No | Sort: createdAt | updatedAt |
| query | `str` | No | Search query |
| projectId | `str` | No | Filter by project ID |
| initiativeId | `str` | No | Filter by initiative ID |
| creatorId | `str` | No | Filter by creator ID |
| createdAt | `str` | No | Created after: ISO-8601 date/duration (e.g., -P1D) |
| updatedAt | `str` | No | Updated after: ISO-8601 date/duration (e.g., -P1D) |
| includeArchived | `bool` | No | Include archived items |

**Example:**
```python
result = await app.list_documents(limit=1.0, cursor="example", orderBy="example")
```

### create_document

Create a new document in Linear

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | `str` | Yes | Document title |
| content | `str` | No | Content as Markdown |
| project | `str` | No | Project name, ID, or slug |
| issue | `str` | No | Issue ID or identifier (e.g., LIN-123) |
| icon | `str` | No | Icon emoji |
| color | `str` | No | Hex color |

**Example:**
```python
result = await app.create_document(title="example", content="example", project="example")
```

### update_document

Update an existing Linear document

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | Yes | Document ID or slug |
| title | `str` | No | Document title |
| content | `str` | No | Content as Markdown |
| project | `str` | No | Project name, ID, or slug |
| icon | `str` | No | Icon emoji |
| color | `str` | No | Hex color |

**Example:**
```python
result = await app.update_document(id="example", title="example", content="example")
```

### extract_images

Extract and fetch images from markdown content. Use this to view screenshots, diagrams, or other images embedded in Linear issues, comments, or documents. Pass the markdown content (e.g., issue description) and receive the images as viewable data.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| markdown | `str` | Yes | Markdown content containing image references (e.g., issue description, comment body) |

**Example:**
```python
result = await app.extract_images(markdown="example")
```

### get_issue

Retrieve detailed information about an issue by ID, including attachments and git branch name

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | Yes | Issue ID |
| includeRelations | `bool` | No | Include blocking/related/duplicate relations |
| includeCustomerNeeds | `bool` | No | Include associated customer needs |

**Example:**
```python
result = await app.get_issue(id="example", includeRelations=True, includeCustomerNeeds=True)
```

### list_issues

List issues in the user's Linear workspace. For my issues, use "me" as the assignee. Use "null" for no assignee.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | `float` | No | Max results (default 50, max 250) |
| cursor | `str` | No | Next page cursor |
| orderBy | `str` | No | Sort: createdAt | updatedAt |
| query | `str` | No | Search issue title or description |
| team | `str` | No | Team name or ID |
| state | `str` | No | State type, name, or ID |
| cycle | `str` | No | Cycle name, number, or ID |
| label | `str` | No | Label name or ID |
| assignee | `str | None` | No | User ID, name, email, or "me" |
| delegate | `str` | No | Agent name or ID |
| project | `str` | No | Project name, ID, or slug |
| priority | `float` | No | 0=None, 1=Urgent, 2=High, 3=Normal, 4=Low |
| parentId | `str` | No | Parent issue ID |
| createdAt | `str` | No | Created after: ISO-8601 date/duration (e.g., -P1D) |
| updatedAt | `str` | No | Updated after: ISO-8601 date/duration (e.g., -P1D) |
| includeArchived | `bool` | No | Include archived items |

**Example:**
```python
result = await app.list_issues(limit=1.0, cursor="example", orderBy="example")
```

### save_issue

Create or update a Linear issue. If `id` is provided, updates the existing issue; otherwise creates a new one. When creating, `title` and `team` are required.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | No | Issue ID. If provided, updates the existing issue |
| title | `str` | No | Issue title (required when creating) |
| description | `str` | No | Content as Markdown |
| team | `str` | No | Team name or ID (required when creating) |
| cycle | `str` | No | Cycle name, number, or ID |
| milestone | `str` | No | Milestone name or ID |
| priority | `float` | No | 0=None, 1=Urgent, 2=High, 3=Normal, 4=Low |
| project | `str` | No | Project name, ID, or slug |
| state | `str` | No | State type, name, or ID |
| assignee | `str | None` | No | User ID, name, email, or "me". Null to remove |
| delegate | `str | None` | No | Agent name or ID. Null to remove |
| labels | `list[str]` | No | Label names or IDs |
| dueDate | `str` | No | Due date (ISO format) |
| parentId | `str | None` | No | Parent issue ID. Null to remove |
| estimate | `float` | No | Issue estimate value |
| links | `list[Any]` | No | Link attachments to add [{url, title}]. Append-only; existing links are never removed |
| blocks | `list[str]` | No | Issue IDs/identifiers this blocks. Append-only; existing relations are never removed |
| blockedBy | `list[str]` | No | Issue IDs/identifiers blocking this. Append-only; existing relations are never removed |
| relatedTo | `list[str]` | No | Related issue IDs/identifiers. Append-only; existing relations are never removed |
| duplicateOf | `str | None` | No | Duplicate of issue ID/identifier. Null to remove |

**Example:**
```python
result = await app.save_issue(id="example", title="example", description="example")
```

### list_issue_statuses

List available issue statuses in a Linear team

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| team | `str` | Yes | Team name or ID |

**Example:**
```python
result = await app.list_issue_statuses(team="example")
```

### get_issue_status

Retrieve detailed information about an issue status in Linear by name or ID

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | Yes | Status ID |
| name | `str` | Yes | Status name |
| team | `str` | Yes | Team name or ID |

**Example:**
```python
result = await app.get_issue_status(id="example", name="example", team="example")
```

### list_issue_labels

List available issue labels in a Linear workspace or team

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | `float` | No | Max results (default 50, max 250) |
| cursor | `str` | No | Next page cursor |
| orderBy | `str` | No | Sort: createdAt | updatedAt |
| name | `str` | No | Filter by name |
| team | `str` | No | Team name or ID |

**Example:**
```python
result = await app.list_issue_labels(limit=1.0, cursor="example", orderBy="example")
```

### create_issue_label

Create a new Linear issue label

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | `str` | Yes | Label name |
| description | `str` | No | Label description |
| color | `str` | No | Hex color code |
| teamId | `str` | No | Team UUID (omit for workspace label) |
| parent | `str` | No | Parent label group name |
| isGroup | `bool` | No | Is label group (not directly applicable) |

**Example:**
```python
result = await app.create_issue_label(name="example", description="example", color="example")
```

### list_projects

List projects in the user's Linear workspace

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | `float` | No | Max results (default 50, max 250) |
| cursor | `str` | No | Next page cursor |
| orderBy | `str` | No | Sort: createdAt | updatedAt |
| query | `str` | No | Search project name |
| state | `str` | No | State type, name, or ID |
| initiative | `str` | No | Initiative name or ID |
| team | `str` | No | Team name or ID |
| member | `str` | No | User ID, name, email, or "me" |
| label | `str` | No | Label name or ID |
| createdAt | `str` | No | Created after: ISO-8601 date/duration (e.g., -P1D) |
| updatedAt | `str` | No | Updated after: ISO-8601 date/duration (e.g., -P1D) |
| includeMilestones | `bool` | No | Include milestones |
| includeMembers | `bool` | No | Include project members |
| includeArchived | `bool` | No | Include archived items |

**Example:**
```python
result = await app.list_projects(limit=1.0, cursor="example", orderBy="example")
```

### get_project

Retrieve details of a specific project in Linear

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | `str` | Yes | Project name, ID, or slug |
| includeMilestones | `bool` | No | Include milestones |
| includeMembers | `bool` | No | Include project members |
| includeResources | `bool` | No | Include resources (documents, links, attachments) |

**Example:**
```python
result = await app.get_project(query="example", includeMilestones=True, includeMembers=True)
```

### save_project

Create or update a Linear project. If `id` is provided, updates the existing project; otherwise creates a new one. When creating, `name` and at least one team (via `addTeams` or `setTeams`) are required.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | `str` | No | Project ID. If provided, updates the existing project |
| name | `str` | No | Project name (required when creating) |
| icon | `str` | No | Icon emoji (e.g., :eagle:) |
| color | `str` | No | Hex color |
| summary | `str` | No | Short summary (max 255 chars) |
| description | `str` | No | Content as Markdown |
| state | `str` | No | Project state |
| startDate | `str` | No | Start date (ISO format) |
| targetDate | `str` | No | Target date (ISO format) |
| priority | `int` | No | 0=None, 1=Urgent, 2=High, 3=Medium, 4=Low |
| addTeams | `list[str]` | No | Team name or ID to add |
| removeTeams | `list[str]` | No | Team name or ID to remove |
| setTeams | `list[str]` | No | Replace all teams with these. Cannot combine with addTeams/removeTeams |
| labels | `list[str]` | No | Label names or IDs |
| lead | `str | None` | No | User ID, name, email, or "me". Null to remove |
| addInitiatives | `list[str]` | No | Initiative names/IDs to add |
| removeInitiatives | `list[str]` | No | Initiative names/IDs to remove |
| setInitiatives | `list[str]` | No | Replace all initiatives with these. Cannot combine with addInitiatives/removeInitiatives |

**Example:**
```python
result = await app.save_project(id="example", name="example", icon="example")
```

### list_project_labels

List available project labels in the Linear workspace

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | `float` | No | Max results (default 50, max 250) |
| cursor | `str` | No | Next page cursor |
| orderBy | `str` | No | Sort: createdAt | updatedAt |

*...additional tools omitted for brevity*
